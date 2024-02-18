"""
This probably isn't optimized/the minimum amount of code to do this
Dealing with sockets/EOFs/random drops is a pain, so this stays on the safe side
of validating to make sure sockets aren't left dangling or data isn't
saved, because of a ConnectionRefusedError/BrokenPipe/general OSErrors

logzero logs all the exceptions, in case they're not what I expect
most of the times, mpv will be open for more than 10 minutes, so
the write period periodically writes will at least capture what was
being listened to, even if *somehow* (has only happened
when my computer suffers a random crash/shut-down)
I lose data on what happened
when mpv EOFd/disconnected due to a BrokenPipe.
BrokenPipes are captured in the event_eof function
"""

import os
import atexit
import threading
import signal
from pathlib import Path
from typing import List, Optional, Dict, Any, Type
from time import sleep, time

from python_mpv_jsonipc import MPV  # type: ignore[import]
from logzero import logger, logfile  # type: ignore[import]

from .serialize import dump_json

SCAN_TIME: int = int(os.environ.get("MPV_HISTORY_DAEMON_SCAN_TIME", 10))


KNOWN_EVENTS = set(
    [
        "socket-added",  # custom event, for when the socket was added
        "mpv-quit",
        "playlist-count",
        "is-paused",
        "eof",
        "seek",
        "paused",
        "resumed",
        "metadata",
        "duration",
        "playlist-pos",
        "media-title",
        "path",
        "working-directory",
        "final-write",  # custom event, for when the dead/dangling socket was removed, and file was written
    ]
)


def new_event(event_name: str, event_data: Any = None) -> Dict[str, Any]:
    """
    helper to create an event. validates the event name
    """
    if event_name not in KNOWN_EVENTS:
        logger.warning(f"Unknown event: {event_name}")
    return {event_name: event_data}


# disabled for now
def clean_playlist(mpv_playlist_response: List[Dict]) -> List[str]:
    """
    simplifies the playlist response from mpv
    from:
        {'filename': '01 Donuts (Outro).mp3'}, {'filename': '02 Workinonit.mp3', 'current': True, 'playing': True},...
    to:
        ['01 Donuts (Outro).mp3', ...]
    """
    filenames: List[str] = []
    for pinfo in mpv_playlist_response:
        if "filename" not in pinfo:
            logger.warning(f"No filename in playlist info!: {pinfo}")
        else:
            filenames.append(pinfo["filename"])
    # truncate to 50 filenames
    return filenames[:50]


class SocketData:
    """
    Stores Metadata for a socket with timestamps in memory
    Writes out to the JSON file when the MPV process ends

    Want to save:
        # at mpv launch:
            # playlist-count
            # working-directory
            # is-paused
        # event-based
            # whenever a socket is played/paused
            # whenever a file changes (eof-reached) save metadata about what's being played
                # metadata
                # media-title
                # path
                # playlist-pos
                # duration
    """

    def __init__(
        self,
        socket: MPV,
        socket_loc: str,
        data_dir: str,
        write_period: Optional[int] = None,
    ):
        self.socket = socket
        self.socket_loc = socket_loc
        self.data_dir = data_dir
        self.socket_time = socket_loc.split("/")[-1]
        self.events: Dict[float, Dict] = {}
        self.write_period = write_period if write_period is not None else 600
        # write every 10 minutes, even if mpv doesn't exit
        self.write_at = time() + self.write_period
        # keep track of playlist/playlist-count, so we can use eof to determine
        # whether we should read next metadata
        pcount = self.socket.playlist_count
        assert isinstance(
            pcount, int
        ), f"Playlist count is not an integer {self.socket_loc} {self.socket.playlist_count}"
        self.playlist_count: int = pcount
        playlist_pos = self.socket.playlist_pos
        # incremented at the top of in store_file_metadata
        # technically this is zero-indexed, but have to deal with off-by-one errors
        # because I can't read the playlist position of a dead socket, counting manually
        if playlist_pos is None:
            logger.warning(
                "Couldn't get playlist position in SocketData initialization, defaulting to 0"
            )
            self.playlist_index = 0
        else:
            self.playlist_index = int(playlist_pos)
        self.store_initial_metadata()
        self.store_file_metadata()

    @property
    def event_count(self):
        return len(self.events)

    _repr_attrs = ("socket", "socket_loc", "event_count")

    def __repr__(self) -> str:
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(
                [
                    "=".join([a, str(getattr(self, a))])
                    for a in self.__class__._repr_attrs
                ]
            ),
        )

    __str__ = __repr__

    def write(self) -> None:
        serialized = dump_json(self.events)
        with open(
            os.path.join(self.data_dir, f"{self.socket_time}.json"), "w"
        ) as event_f:
            event_f.write(serialized)

    def nevent(self, event_name: str, event_data: Optional[Any] = None) -> None:
        """add an event"""
        ct = time()
        logger.debug(f"{self.socket_time}|{ct}|{event_name}|{event_data}")
        self.events[ct] = new_event(event_name, event_data)

    def store_initial_metadata(self) -> None:
        self.nevent("socket-added", time())
        self.poll_for_property("working_directory", "working-directory")
        self.poll_for_property("playlist_count", "playlist-count")
        self.poll_for_property("pause", "is-paused")
        # self.nevent("playlist", clean_playlist(self.socket.playlist))

    def poll_for_property(
        self, attr: str, event_name: str, tries: int = 20, create_event: bool = True
    ) -> Any:
        """
        Some properties aren't set when the file starts?
        sleeps for 0.1 of a second between tries (20 * 0.1 = 2 seconds)

        if create_event, once it has a non-None value, it sets the value
        with self.nevent
        """
        for _ in range(tries):
            logger.debug(f"polling for {attr} {event_name}")
            value = getattr(self.socket, attr)
            if value is not None:
                if create_event:
                    self.nevent(event_name, value)
                return value
            sleep(0.1)
        else:
            logger.warning(f"{self.socket_loc} Couldn't poll for {event_name}")

    def store_file_metadata(self) -> None:
        """
        Called when EOF is reached (so, another file starts)
        """

        self.playlist_index += 1
        # (is zero indexed, but incrementing before making any requests out to the socket)
        if self.playlist_index - 1 >= self.playlist_count:
            logger.debug("Reached end of playlist, not reading in next file info...")
            return

        # poll for these in case they're not set for some reason, because
        # the file was just loaded by mpv
        actual_playlist_pos = self.poll_for_property("playlist_pos", "playlist-pos")
        # make sure internal, manually counted playlist index is accurate
        if actual_playlist_pos is not None:
            if actual_playlist_pos + 1 != self.playlist_index:
                self.playlist_index = actual_playlist_pos + 1
        self.poll_for_property("path", "path")
        self.poll_for_property("media_title", "media-title")

        # weird, metadata and duration aren't received at the beginning of the file?
        # poll for duration and metadata
        # maybe these have to be parsed and there done a bit after the file is read
        self.poll_for_property("metadata", "metadata")
        self.poll_for_property("duration", "duration")

    def event_resumed(self) -> None:
        """
        Called when the media is resumed, also save % in file
        """
        self.nevent("resumed", {"percent-pos": self.socket.percent_pos})

    def event_paused(self) -> None:
        """
        Called when the media is paused, also save % in file
        """
        self.nevent("paused", {"percent-pos": self.socket.percent_pos})

    def event_eof(self) -> None:
        """
        Called when the 'eof' event happens. Doesn't necessarily mean mpv exits
        Could be going to the next song in the current playlist
        (This doesn't happen the first time a song is loaded)

        Though, this is also called when mpv exits, so we should wrap the
        possible socket errors
        """
        self.nevent("eof")
        try:
            self.store_file_metadata()  # store info about new file that's playing
        # possible errors thrown: BrokenPipeError, OSError
        except Exception as e:
            logger.warning(f"Ignoring error: {e}")
            if not isinstance(e, (ConnectionRefusedError, TimeoutError)):
                logger.exception(e)

    def event_seeking(self) -> None:
        """
        Called when the user seeks in the file. Could possibly be called when a file is loaded as well
        """
        pos = self.socket.percent_pos
        if pos is not None and pos < 2:
            # logger.debug("ignoring seek because we just EOFd?")
            pass
        else:
            # save what % we seeked to
            self.nevent("seek", {"percent-pos": pos})


class LoopHandler:
    """
    Handles keeping track of currently live mpv instances, attaching handlers,
    the main loop.
    """

    def __init__(
        self,
        socket_dir: str,
        data_dir: str,
        *,
        autostart: bool = True,
        write_period: Optional[int],
        poll_time: Optional[int] = 10,
        socket_data_cls: Type[SocketData] = SocketData,
    ):
        self.data_dir: str = data_dir
        self.socket_dir: str = socket_dir
        self.write_period = write_period
        self._socket_dir_path: Path = Path(socket_dir).expanduser().absolute()
        self.sockets: Dict[str, MPV] = {}
        self.socket_data_cls = socket_data_cls
        self.poll_time = poll_time
        self.socket_data: Dict[str, SocketData] = {}
        self.waiting = threading.Event()
        self.setup_signal_handler()
        if autostart:
            self.run_loop()

    def scan_sockets(self) -> None:
        """
        Look for any new sockets at socket_dir, remove any dead ones
        """
        socket_loc_scoped: Optional[str] = None  # to access this after the try/except
        try:
            # iterate through all files
            for socket_name in os.listdir(self.socket_dir):
                socket_loc: str = os.path.join(self.socket_dir, socket_name)
                socket_loc_scoped = socket_loc
                if socket_loc not in self.sockets:
                    # each of these runs in a separate thread, so the while loop below doesn't block event data
                    # ConnectionRefusedError thrown here
                    new_sock = MPV(
                        start_mpv=False,
                        ipc_socket=socket_loc,
                        quit_callback=lambda: self.remove_socket(socket_loc),
                    )
                    self.sockets[socket_loc] = new_sock
                    # if the socket gets disconnected for some reason, and we're recreating MPV, *never* overwrite data
                    if socket_loc in self.socket_data:
                        self.socket_data[socket_loc].socket = new_sock
                    else:
                        self.socket_data[socket_loc] = self.socket_data_cls(
                            new_sock, socket_loc, self.data_dir, self.write_period
                        )
                    self.attach_observers(socket_loc, new_sock)
                    self.debug_internals()
                else:  # if this socket is already connected, just try to get the path from the socket
                    # may have been a TimeoutError: No response from MPV.
                    # which resulted in the socket remaining in self.sockets, even if its eof'd and exited
                    self.sockets[socket_loc].path
            # iterate through sockets, if file doesn't exist for some reason
            # this is probably unnecessary
            for s_loc, sock_obj in self.sockets.items():
                # update higher scope to allow usage in except block
                socket_loc_scoped = s_loc
                # try to access path to possibly cause ConnectionRefusedError,
                # removing a dead socket
                sock_obj.path
        except (ConnectionRefusedError, BrokenPipeError):
            logger.debug(
                f"Connected refused for socket at {socket_loc_scoped}, removing dead/dangling socket file..."
            )
            # make sure its actually removed from active sockets
            # gets removed from socket_data after 10 seconds
            if socket_loc_scoped is not None and socket_loc_scoped in self.sockets:
                self.remove_socket(socket_loc_scoped)
            # rm -f
            try:
                if socket_loc_scoped:
                    os.remove(socket_loc_scoped)
            except FileNotFoundError:
                pass

    def attach_observers(self, socket_loc: str, sock: MPV) -> None:
        """
        Watch for user pausing, eof-file (file ending)
        """
        # sanity-check
        if hasattr(sock, "_watching_instance"):
            logger.warning("Tried to attach observers twice!")
            return
        setattr(sock, "_watching_instance", None)

        socket_data: SocketData = self.socket_data[socket_loc]

        # keep track of when last EOF was. EOF also happens when
        # a file is loaded, and seeking happens when you load a file,
        # (since its sort of seeking to the beginning)
        # doesn't seem to be deterministic/easy to filter seeks out
        # by EOFs, and might match actual seeking. so, will have
        # to do larger analysis on the dumped data to figure out
        # if EOF next to seek, remove the seek

        @sock.property_observer("pause")
        def on_pause(_, value):
            if value:  # item is now paused
                socket_data.event_paused()
            else:
                socket_data.event_resumed()

        @sock.property_observer("eof-reached")
        def on_eof(_, value):
            # value == False means that eof has not been reached
            if isinstance(value, bool) and not value:
                return
            if value is not None:
                logger.warning(
                    "Seems that this is supposed to be None; just to signify event? not sure why it isn't"
                )
            socket_data.event_eof()

        @sock.property_observer("seeking")
        def on_seek(_, value):
            if isinstance(value, bool) and value:
                socket_data.event_seeking()

    def remove_socket(self, socket_loc: str) -> None:
        if socket_loc in self.sockets:
            logger.debug(f"Removing socket {socket_loc}")
            # write quit event
            try:
                self.socket_data[socket_loc].nevent("mpv-quit", time())
            except KeyError:
                pass
            try:
                del self.sockets[socket_loc]
            except KeyError:
                pass
        else:
            logger.warning(
                "called remove socket, but socket_loc doesn't exist in self.sockets"
            )
        # (doesn't remove the file here, but should find it on the next scan_sockets call and remove it then)

    def debug_internals(self) -> None:
        logger.debug(f"sockets {self.sockets}")
        logger.debug(f"socket_data {self.socket_data}")

    def periodic_write(self) -> None:
        now = time()
        for socket_data in self.socket_data.values():
            if now > socket_data.write_at:
                logger.debug(f"{socket_data.socket_time}|running periodic write")
                socket_data.write()
                socket_data.write_at = now + socket_data.write_period
                self.debug_internals()

    def write_data(self, force: bool = False) -> None:
        """
        Write out any completed SocketData to disk
        """
        # if the /tmp/mpvsockets/ file is no longer in self.sockets
        # but we have socketdata for it from when it was alive, in
        # self.socket_data, write that out to data_dir
        #
        # this runs in the main thread... so errors crash main thread
        for socket_loc in list(self.socket_data):
            if socket_loc not in self.sockets:
                logger.info(f"{socket_loc}: writing to file...")
                self.socket_data[socket_loc].nevent("final-write", time())
                self.socket_data[socket_loc].write()
                del self.socket_data[socket_loc]
                self.debug_internals()
        if force:
            # don't write additional events to the file, just write data
            # for every socket regardless of state. This is used if the program
            # is crashing/etc.
            logger.warning("forcing write to files...")
            self.debug_internals()
            for socket_data in self.socket_data.values():
                socket_data.write()

    def setup_signal_handler(self) -> None:
        # catch the RTMIN signal, which some user defined code might send to this process
        # to tell the daemon that a new socket was added/removed
        # this is never *required*, but its nice as it means we pick up data ASAP
        # instead of waiting for the next scan_sockets call

        signal.signal(signal.SIGRTMIN, self.signal_handler)

    def signal_handler(self, signum: int, frame: Any) -> None:
        signal_name = signal.Signals(signum).name
        logger.debug(f"Caught signal {signum} {signal_name}, interrupting main loop")
        self.waiting.set()

    def run_loop(self) -> None:
        if self.poll_time:
            logger.debug("Starting mpv-history-daemon loop...")
            logger.debug(f"Using socket class {self.socket_data_cls}")
            while True:
                self.scan_sockets()
                self.periodic_write()
                self.write_data()
                was_interrupted = self.waiting.wait(self.poll_time)
                self.waiting.clear()
                if was_interrupted is True:
                    logger.debug(
                        "mpv-history-daemon got interrupt, checking sockets..."
                    )
        else:
            logger.warning(
                "poll time is None, skipping periodic check. You have to manually signal mpv whenever sockets are added or removed or this won't work"
            )
            while True:
                # no timeout, just wait forever till the event is set
                was_interrupted = self.waiting.wait()
                self.waiting.clear()
                if was_interrupted is True:
                    logger.debug(
                        "mpv-history-daemon got interrupt, checking sockets..."
                    )
                    self.scan_sockets()
                    self.periodic_write()
                    self.write_data()


def run(
    socket_dir: str,
    data_dir: str,
    log_file: str,
    write_period: Optional[int],
    socket_data_cls: Type[SocketData],
    poll_time: Optional[int],
) -> None:
    # if the daemon launched before any mpv instances
    if not os.path.exists(socket_dir):
        os.makedirs(socket_dir)
    assert os.path.isdir(socket_dir)
    os.makedirs(data_dir, exist_ok=True)
    assert os.path.isdir(data_dir)
    logfile(log_file, maxBytes=int(1e7), backupCount=1)
    lh = LoopHandler(
        socket_dir,
        data_dir,
        autostart=False,
        write_period=write_period,
        socket_data_cls=socket_data_cls,
        poll_time=poll_time,
    )
    # in case user keyboardinterrupt's or this crashes completely
    # for some reason, write data out to files in-case it hasn't
    # been done recently
    atexit.register(lambda: lh.write_data(force=True))
    lh.run_loop()
