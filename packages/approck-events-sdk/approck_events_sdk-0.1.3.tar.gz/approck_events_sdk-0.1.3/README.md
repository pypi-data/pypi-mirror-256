# approck-events-sdk - Approck Events SDK for Python

## Getting started

### Install

```
pip install --upgrade approck-events-sdk
```

### Configuration

```python
import approck_events_sdk
approck_events_sdk.init(api_uri="https://api.events.uprock.pro")
```

In your testing and development environment you still might want to run that
code without sending any events. In that case, simply call `init` without a
DSN:

```python
approck_events_sdk.init()
```

### Usage:

```python
from approck_events_sdk.event import capture_event, Event
capture_event(Event(event_name="test"))
```

## Concurrency

- `approck-events-sdk` currently does not support gevent-based setups.
- On `init`, Sentry-Python spawns a thread on its own. That means if you use
  `uwsgi`, you currently need to enable threads.
