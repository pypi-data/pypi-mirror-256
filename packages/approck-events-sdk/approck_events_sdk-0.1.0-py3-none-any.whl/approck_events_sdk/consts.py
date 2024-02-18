import socket


DEFAULT_SERVER_NAME = socket.gethostname() if hasattr(socket, "gethostname") else None

DEFAULT_OPTIONS = {
    "drain_timeout": 2.0,
    "api_uri": f"http://{DEFAULT_SERVER_NAME}/v1/event",
    "sample_rate": 1.0,
    "transport": None,
}
