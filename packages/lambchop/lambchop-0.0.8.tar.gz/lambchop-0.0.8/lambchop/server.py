import importlib
import sys
from pathlib import Path

from http.server import HTTPServer, BaseHTTPRequestHandler
from queue import Queue
import threading

import dill
import json

from lambchop.datastructures import Task


def get_fun(task: Task) -> None:
    f = Path(task.file)
    sys.path.append(str(f.parent))
    module = importlib.import_module(f.stem)
    return getattr(module, task.func)


def execute(task):
    func = get_fun(task)
    args = task.args
    kwargs = task.kwargs
    func(*args, **kwargs)


class Handler(BaseHTTPRequestHandler):
    """Handler recieves jobs and adds them to a queue."""
    def __init__(self, request, client_address, server, q: Queue):
        self.q=q
        super().__init__(request, client_address, server)

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
    
    def _deserialize(msg: bytes) -> Task:
        msg = json.loads(msg)
        msg = bytes.fromhex(msg)
        msg = dill.loads( msg )
        return msg
    
    def do_GET(self):
        self._set_response()
        msg = json.dumps('PONG').encode('utf-8')
        self.wfile.write(msg)

    def do_POST(self):
        """Sends a task to the queue."""
        content_length = int(self.headers['Content-Length'])
        msg = self.rfile.read(content_length)
        task = self._deserialize(msg)
        
        t = threading.Thread(target=execute, args=(task,))
        t.start()
        self.q.append(t)

        self._set_response()
        msg = json.dumps('TASK QUEUED.').encode('utf-8')
        self.wfile.write(msg)


class Server(HTTPServer):
    def __init__(self, port: int = 1956) -> None:
        addr = ("0.0.0.0", port)
        self.q = []
        
        def handler(*args):
            Handler(*args, q=self.q)

        self.server = HTTPServer(addr, handler)

    def serve(self):
        print("Starting server...", flush=True)
        self.server.serve_forever()
        print("Server stopped.", flush=True)


if __name__=="__main__":
    from datastructures import Task
    
    s = Server()
    s.serve()