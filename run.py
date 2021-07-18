#!/usr/bin/env python3
import os
import sys
import asyncio
import logging
import typing

from pyhocon import ConfigFactory
from app.server import Server


def log_level_from_string(log_level: typing.Optional[str]):
    log_level = log_level.lower()
    log_levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
    }

    # if log level is debug set flask to debug as well
    if log_level == "debug":
        os.environ['FLASK_ENV'] = "development"

    if log_level in log_levels:
        return log_levels[log_level]
    else:
        return log_levels["info"]


def setup_logging(config: dict):
    logging.basicConfig(
        level=log_level_from_string(config.get("log_level", None)),
        format="[%(asctime)s] [%(levelname)-8s] -- %(message)s",
        stream=sys.stdout
    )


async def main():
    server = Server(config, logging=logging)

    try:
        await server.start()
    except Exception as err:
        logging.error(str(err), exc_info=True)
    finally:
        await server.stop()


if __name__ == "__main__":
    config = ConfigFactory.parse_file("config.conf")
    setup_logging(config)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
