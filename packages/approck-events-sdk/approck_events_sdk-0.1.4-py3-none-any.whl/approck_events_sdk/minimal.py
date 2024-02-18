__all__ = ["Hub"]


def public(f):
    __all__.append(f.__name__)
    return f


@public
def capture_event(event):
    hub = Hub.current
    if hub is not None:
        return hub.capture_event(event)


@public
def get_current_hub():
    return Hub.current


try:
    from approck_events_sdk.hub import Hub
except ImportError:

    class Hub:
        current = main = None
