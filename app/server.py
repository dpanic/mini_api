import queue
import threading
from flask import Flask
from flask import request

import app.worker as worker


class Server():
    def __init__(self, config: dict, logging):
        self.config = config
        self.logging = logging

        self.queue = queue.Queue(maxsize=int(self.config.server.queue_size))
        self.worker = worker.Worker(config, logging, self.queue)

        self.logging.debug("initialized server with config %s" % (self.config))
        self.app = Flask(__name__)

    def gracefoul_shutdown(self):
        for _ in range(0, int(self.config.server.workers)):
            self.queue.put_nowait(False)

    def get(self) -> str:
        url = request.args.get('url')
        self.logging.debug(
            f"received url {url} for processing, total in queue {self.queue.qsize()}/{self.queue.maxsize}")

        try:
            self.queue.put_nowait(url)
            return 'get %s!' % url
        except BaseException:
            self.logging.debug(f"rejected {url} because our systems are busy")
            return 'our systems are currently busy'

    async def start(self):
        # add routes
        self.app.add_url_rule('/get', view_func=self.get)

        # creating workers
        for it in range(0, int(self.config.server.workers)):
            self.logging.debug(f"starting worker #{it+1}")
            t = threading.Thread(target=self.worker.run, args=(it,)).start()

        t = threading.Thread(target=self.app.run, kwargs={'host': '0.0.0.0', 'use_reloader': False})
        t.start()

    async def stop(self):
        pass
