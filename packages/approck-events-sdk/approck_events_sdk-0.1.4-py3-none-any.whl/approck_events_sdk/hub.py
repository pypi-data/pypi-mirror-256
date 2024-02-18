from contextvars import ContextVar


_local = ContextVar("events_current_hub")


class HubMeta(type):
    @property
    def current(cls):
        rv = _local.get(None)
        if rv is None:
            rv = Hub(GLOBAL_HUB)
            _local.set(rv)
        return rv

    @property
    def main(cls):
        return GLOBAL_HUB


class _HubManager(object):
    def __init__(self, hub):
        self._old = Hub.current
        _local.set(hub)

    def __exit__(self, exc_type, exc_value, tb):
        _local.set(self._old)


class Hub(metaclass=HubMeta):
    def __init__(self, client_or_hub=None):
        if isinstance(client_or_hub, Hub):
            hub = client_or_hub
            client = hub.client
        else:
            client = client_or_hub
        self.client = client

    def __enter__(self):
        return _HubManager(self)

    def run(self, callback):
        """Runs a callback in the context of the hub.  Alternatively the
        with statement can be used on the hub directly.
        """
        with self:
            callback()

    def bind_client(self, new):
        """Binds a new client to the hub."""
        self.client = new

    def capture_event(self, event):
        """Captures an event."""
        if self.client is not None:
            self.client.capture_event(event)


GLOBAL_HUB = Hub()
