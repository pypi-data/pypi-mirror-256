import atexit

from .consts import DEFAULT_OPTIONS
from .event import Event
from .transport import Transport
from .utils import SkipEvent


class Client:
    def __init__(self, *args, **kwargs):
        options = dict(DEFAULT_OPTIONS)
        options.update(*args, **kwargs)
        self.options = options
        self._transport = self.options.pop("transport")
        if self._transport is None:
            self._transport = Transport(
                api_uri=self.options.pop("api_uri"),
            )
            self._transport.start()

        atexit.register(self.close)

    def _prepare_event(self, event):
        return event

    def capture_event(self, event):
        """Captures an event."""
        if self._transport is None:
            return
        if not isinstance(event, Event):
            event = Event(event)
        try:
            event = self._prepare_event(event)
        except SkipEvent:
            return
        self._transport.capture_event(event)

    def drain_events(self, timeout=None):
        if timeout is None:
            timeout = self.options["drain_timeout"]
        if self._transport is not None:
            self._transport.drain_events(timeout)

    def close(self):
        self.drain_events()
        if self._transport is not None:
            self._transport.close()
