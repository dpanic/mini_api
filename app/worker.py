import requests
import hashlib as hash

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Worker():
    running: bool

    def __init__(self, config: dict, logging, queue):
        self.config = config
        self.logging = logging

        self.timeout = self.config.request.timeout
        self.max_size = self.config.request.max_size

        self.queue = queue

    def run(self, it):
        while True:
            url = self.queue.get()

            if not url:
                self.logging.info(f"[worker #{it}] going for a shutdown")
                # do some cleanup
                return

            res = requests.get(url, timeout=self.timeout, allow_redirects=True, verify=False, stream=True)

            sha = hash.sha256()
            chunk_size = 1024
            total_size = 0
            for chunk in res.iter_content(chunk_size):
                total_size += len(chunk)
                if total_size >= self.max_size:
                    self.logging.info(
                        f"[worker #{it}] downloaded {url} {total_size} bytes from maximum allowed {self.max_size/1000} Mb. stopping here.")
                    break
                sha.update(chunk)

            self.logging.info(f"[worker #{it}] for url {url}, calculated sha256 sum is {sha.hexdigest()}")
            self.queue.task_done()
