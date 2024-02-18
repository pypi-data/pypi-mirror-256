"""
This module defines the level, format and handlers for the root logger and for the special
'egse' logger. The egse_logger will be configured with a special handler which sends all
logging messages to a log control server.

This module is loaded whenever an egse module is loaded, to ensure all log messages are properly
forwarded to the log control server.
"""

import logging
import pickle
import sys
import traceback

import zmq

LOG_FORMAT_FULL = (
    "%(asctime)23s:%(processName)20s:%(levelname)8s:%(lineno)5d:%(name)-20s:%(message)s"
)

# Configure the root logger

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT_FULL)

__all__ = [
    "egse_logger",
    "set_all_logger_levels",
    "ZeroMQHandler",
    "close_all_zmq_handlers",
]


class ZeroMQHandler(logging.Handler):
    def __init__(self, uri=None, socket_type=zmq.PUSH, ctx=None):

        from egse.settings import Settings
        from egse.zmq_ser import connect_address

        ctrl_settings = Settings.load("Logging Control Server")
        uri = uri or connect_address(ctrl_settings.PROTOCOL, ctrl_settings.HOSTNAME,
                                     ctrl_settings.LOGGING_PORT)

        logging.Handler.__init__(self)

        # print(f"ZeroMQHandler.__init__({uri=}, {socket_type=}, {ctx=})")

        self.setLevel(logging.NOTSET)

        self.ctx = ctx or zmq.Context().instance()
        self.socket = zmq.Socket(self.ctx, socket_type)
        self.socket.setsockopt(zmq.SNDHWM, 0)  # never block on sending msg
        self.socket.connect(uri)

    def __del__(self):
        self.close()

    def close(self):
        self.socket.close(linger=0)

    def emit(self, record):
        """
        Emit a record.

        Writes the LogRecord to the queue, preparing it for pickling first.
        """

        # print(f"ZeroMQHandler.emit({record})")

        from egse.system import is_in_ipython

        try:
            if record.exc_info:
                record.exc_text = traceback.format_exc()
                record.exc_info = None  # traceback objects can not be pickled
            if record.processName == "MainProcess" and is_in_ipython():
                record.processName = "IPython"
            data = pickle.dumps(record.__dict__)
            self.socket.send(data, flags=zmq.NOBLOCK)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:
            print(f"ZeroMQHandler: Exception - {exc}", file=sys.stderr)
            self.handleError(record)


def close_all_zmq_handlers():
    """
    Close all the ZeroMQHandlers that are connected to a logger.

    This function is automatically called upon termination of the control servers. For your own
    applications, call this function before exiting the App.
    """

    loggers = logging.Logger.manager.loggerDict

    for name, logger in loggers.items():
        if isinstance(logger, logging.PlaceHolder):
            continue
        for handler in logger.handlers:
            if isinstance(handler, ZeroMQHandler):
                logger.debug(f"Closing handler for logger {name}")
                handler.close()


# Initialize logging as we want it for the Common-EGSE
#
# * The ZeroMQHandler to send all logging messages, i.e. level=DEBUG to the Logging Server
# * The (local) StreamingHandlers to print only INFO messages and higher

logging.disable(logging.NOTSET)
root_logger = logging.getLogger()

for handler in root_logger.handlers:
    handler.setLevel(logging.INFO)


# Define the `egse` logger and add the ZeroMQHandler to this logger

egse_logger = logging.getLogger("egse")
egse_logger.setLevel(logging.DEBUG)

zmq_handler = ZeroMQHandler()
zmq_handler.setLevel(logging.NOTSET)

egse_logger.addHandler(zmq_handler)
egse_logger.setLevel(logging.DEBUG)


def replace_zmq_handler():
    """
    This function will replace the current ZeroMQ Handler with a new instance. Use this function
    in the run() method of a multiprocessing.Process:

        import egse.logger
        egse.logger.replace_zmq_handler()

    Don't use this function in the __init__() method as only the run() method will execute in
    the new Process and replace the handler in the proper environment. The reason for this is
    that the ZeroMQ socket is not thread/Process safe, so a new ZeroMQ socket needs to be created
    in the correct process environment.
    """
    global egse_logger

    this_handler = None
    for handler in egse_logger.handlers:
        if isinstance(handler, ZeroMQHandler):
            this_handler = handler
    if this_handler is not None:
        egse_logger.removeHandler(this_handler)
    egse_logger.addHandler(ZeroMQHandler())


def create_new_zmq_logger(name: str):
    """
    Create a new logger with the given name and add a ZeroMQ Handler to this logger.

    If the logger already has a ZeroMQ handler attached, don't add a second ZeroMQ handler,
    just return the Logger object.

    Args:
        name: the requested name for the logger

    Returns:
        A Logger for the given name with a ZeroMQ handler attached.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # If the ZeroMQ handler already exists for this logger, don't add a second handler

    for handler in logger.handlers:
        if isinstance(handler, ZeroMQHandler):
            return logger

    zmq_handler = ZeroMQHandler()
    zmq_handler.setLevel(logging.NOTSET)

    logger.addHandler(zmq_handler)
    logger.setLevel(logging.DEBUG)

    return logger


# We define a new level that is lower the DEBUG for extreme verbose messages

logging.FLASH_FLOOD = 5
logging.addLevelName(logging.FLASH_FLOOD, "FLASH_FLOOD")


def flash_flood(self, msg, *args, **kwargs):
    if self.isEnabledFor(logging.FLASH_FLOOD):
        self._log(logging.FLASH_FLOOD, msg, args, **kwargs)


logging.flash_flood = flash_flood
logging.Logger.flash_flood = flash_flood


def set_all_logger_levels(level: int):
    global root_logger, egse_logger

    root_logger.level = level
    egse_logger.level = level

    for handler in root_logger.handlers:
        handler.setLevel(level)

    # We don't want to restrict egse_logger levels

    # for handler in egse_logger.handlers:
    #     handler.setLevel(level)


if __name__ == "__main__":

    import egse.logger

    LOGGER = logging.getLogger("egse.0mq-log-test")
    LOGGER.setLevel(logging.FLASH_FLOOD)

    LOGGER.flash_flood("Hello, ZeroMQ logging: This is a FLASH_FLOOD message.")
    LOGGER.debug("Hello, ZeroMQ logging: This is a DEBUG message.")
    LOGGER.info("Hello, ZeroMQ logging: This is an INFO message.")
    LOGGER.warning("Hello, ZeroMQ logging: This is a WARNING message.")
    LOGGER.error("Hello, ZeroMQ logging: This is an ERROR message.")
    LOGGER.critical("Hello, ZeroMQ logging: This is a CRITICAL message.")
    try:
        raise ValueError("A fake ValueError, raised for testing.")
    except ValueError:
        LOGGER.exception("Hello, ZeroMQ logging: This is an EXCEPTION message.")

    LOGGER = logging.getLogger("plain-log-test")

    LOGGER.flash_flood("Vanilla logging: This is a FLASH_FLOOD message.")
    LOGGER.debug("Vanilla logging: This is a DEBUG message.")
    LOGGER.info("Vanilla logging: This is an INFO message.")
    LOGGER.warning("Vanilla logging: This is a WARNING message.")
    LOGGER.error("Vanilla logging: This is an ERROR message.")
    LOGGER.critical("Vanilla logging: This is a CRITICAL message.")
    try:
        raise ValueError("A fake ValueError, raised for testing.")
    except ValueError:
        LOGGER.exception("Vanilla logging: This is an EXCEPTION message.")
