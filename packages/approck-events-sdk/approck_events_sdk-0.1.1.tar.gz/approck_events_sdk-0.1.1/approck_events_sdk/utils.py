class SkipEvent(Exception):
    """Risen from an event processor to indicate that the event should be
    ignored and not be reported."""
