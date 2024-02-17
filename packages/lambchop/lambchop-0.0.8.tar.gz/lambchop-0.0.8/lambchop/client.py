from typing import Any
import requests
import dill

from .datastructures import Task


class Client:
    def __init__(self, port: int = 1956):
        self.port = port
        self.url = f"http://localhost:{self.port}/"

    def _serialize(self, task: Task) -> bytes:
        """Convert python function and parameters"""
        return dill.dumps(task).hex()

    def _deserialize(self, result: bytes) -> Any:
        return dill.loads(result)

    def ping(self):
        """Send name to TCP server."""
        return requests.get(self.url)

    def send_task(self, task: Task):
        """Send task to TCP server."""
        bt = self._serialize(task)
        r = requests.post(self.url, json=bt)
        print(r.json(), flush=True)