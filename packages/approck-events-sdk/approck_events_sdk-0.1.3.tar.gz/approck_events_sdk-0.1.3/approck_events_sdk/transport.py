from __future__ import print_function

import dataclasses
import datetime
import gzip
import io
import json
import logging
import queue
import sys
import threading
import traceback

import certifi
import urllib3

logger = logging.getLogger(__name__)


def _json_serializer(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} is not serializable")


def _make_pool():
    opts = {"num_pools": 2, "cert_reqs": "CERT_REQUIRED", "ca_certs": certifi.where()}

    return urllib3.PoolManager(**opts)


_SHUTDOWN = object()
_retry = urllib3.util.Retry()


def send_event(pool, event, store_api_url):
    event_d = dataclasses.asdict(event)
    # Filter out private properties
    event_d = {k: v for k, v in event_d.items() if not k.startswith("_")}

    body = io.BytesIO()
    with gzip.GzipFile(fileobj=body, mode="w") as f:
        f.write(json.dumps(event_d, default=_json_serializer).encode("utf-8"))

    response = pool.request(
        "POST",
        str(store_api_url),
        body=body.getvalue(),
        headers={
            "Content-Type": "application/json",
            "Content-Encoding": "gzip",
        },
    )
    try:
        if response.status == 429:
            return datetime.datetime.utcnow() + datetime.timedelta(seconds=_retry.get_retry_after(response))
    finally:
        response.close()


def spawn_thread(transport):
    def thread():
        disabled_until = None
        while 1:
            item = transport.queue.get()
            if item is _SHUTDOWN:
                transport.queue.task_done()
                break

            if disabled_until is not None:
                if datetime.datetime.utcnow() < disabled_until:
                    transport.queue.task_done()
                    continue
                disabled_until = None

            try:
                disabled_until = send_event(transport.pool, item, transport.api_uri)
            except Exception:
                print("Could not send approck event", file=sys.stderr)
                print(traceback.format_exc(), file=sys.stderr)
            finally:
                transport.queue.task_done()

    t = threading.Thread(target=thread)
    t.daemon = True
    t.start()


class Transport:
    def __init__(self, api_uri):
        self.api_uri = api_uri
        self.queue = None
        self.pool = _make_pool()

    def start(self):
        if self.queue is None:
            self.queue = queue.Queue(30)
            spawn_thread(self)

    def capture_event(self, event):
        if self.queue is None:
            raise RuntimeError("Transport shut down")
        try:
            self.queue.put_nowait(event)
        except queue.Full:
            pass

    def close(self):
        if self.queue is not None:
            try:
                self.queue.put_nowait(_SHUTDOWN)
            except queue.Full:
                pass
            self.queue = None

    def drain_events(self, timeout):
        q = self.queue
        if q is not None:
            with q.all_tasks_done:
                while q.unfinished_tasks:
                    q.all_tasks_done.wait(timeout)

    def __del__(self):
        self.close()
