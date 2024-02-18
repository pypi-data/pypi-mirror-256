"""
This module defines the abstract class for any control server and some convenience functions.
"""
import abc
import datetime
import logging
import pickle
import threading
import time
from functools import partial
from typing import Any
from typing import Callable
from typing import Type

import zmq

from egse.decorators import retry
from egse.listener import Listeners
from egse.logger import close_all_zmq_handlers
from egse.process import ProcessStatus
from egse.settings import Settings
from egse.system import do_every
from egse.system import get_average_execution_time
from egse.system import get_average_execution_times
from egse.system import get_full_classname
from egse.system import get_host_ip
from egse.system import save_average_execution_time

MODULE_LOGGER = logging.getLogger(__name__)
PROCESS_SETTINGS = Settings.load("PROCESS")


def time_in_ms():
    """Returns the current time in milliseconds since the Epoch."""
    return int(round(time.time() * 1000))


def time_in_s():
    """Returns the current time in seconds since the Epoch."""
    return time.time()


def is_control_server_active(endpoint: str = None, timeout: float = 0.5) -> bool:
    """
    Check if the control server is running. This function sends a *Ping* message to the
    control server and expects a *Pong* answer back within the timeout period.

    Args:
        endpoint (str): the endpoint to connect to, i.e. <protocol>://<address>:<port>
        timeout (float): timeout when waiting for a reply [seconds, default=0.5]
    Returns:
        True if the Control Server is running and replied with the expected answer.
    """
    ctx = zmq.Context.instance()

    return_code = False

    try:
        socket = ctx.socket(zmq.REQ)
        socket.connect(endpoint)
        data = pickle.dumps("Ping")
        socket.send(data)
        rlist, _, _ = zmq.select([socket], [], [], timeout=timeout)
        if socket in rlist:
            data = socket.recv()
            response = pickle.loads(data)
            return_code = response == "Pong"
        socket.close(linger=0)
    except Exception as exc:
        MODULE_LOGGER.warning(f"Caught an exception while pinging a control server at {endpoint}: {exc}.")

    return return_code


class Response:
    """Base class for any reply or response between client-server communication.

    The idea is that the response is encapsulated in one of the subclasses depending
    on the type of response.
    """

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message

    @property
    def successful(self):
        """Returns True if the Response is not an Exception."""
        return not isinstance(self, Exception)


class Failure(Response, Exception):
    """A failure response indicating something went wrong at the other side.

    This class is used to encapsulate an Exception that was caught and needs to be
    passed to the client. So, the intended use is like this:
    ```
    try:
        # perform some useful action that might raise an Exception
    except SomeException as exc:
        return Failure("Our action failed", exc)
    ```
    The client can inspect the Exception that was originally raised, in this case `SomeException`
    with the `cause` variable.

    Since a Failure is also an Exception, the property `successful` will return False.
    So, the calling method can test for this easily.

    ```
    rc: Response = function_that_returns_a_response()

    if not rc.successful:
        # handle the failure
    else:
        # handle success
    ```

    """

    def __init__(self, message: str, cause: Exception = None):
        msg = f"{message}: {cause}" if cause is not None else message
        super().__init__(msg)
        self.cause = cause


class Success(Response):
    """A success response for the client.

    The return code from any action or function that needs to be returned to the
    client shall be added.

    Since `Success` doesn't inherit from `Exception`, the property `successful` will return True.
    """

    def __init__(self, message: str, return_code: Any = None):
        msg = f"{message}: {return_code}" if return_code is not None else message
        super().__init__(msg)
        self.return_code = return_code


class Message(Response):
    """A message response from the client.

    Send a Message when there is no Failure, but also no return code. This is the alternative of
    returning a None.

    Message returns True for the property successful since it doesn't inherit from Exception.
    """

    pass


class ControlServer(metaclass=abc.ABCMeta):
    """
    The base class for all device control servers and for the Storage Manager and Configuration
    Manager. A Control Server reads commands from a ZeroMQ socket and executes these commands by
    calling the `execute()` method of the commanding protocol class.

    The sub-class shall define the following:

    * Define the device protocol class -> `self.device_protocol`
    * Bind the command socket to the device protocol -> `self.dev_ctrl_cmd_sock`
    * Register the command socket in the poll set -> `self.poller`

    """

    def __init__(self):
        from egse.monitoring import MonitoringProtocol
        from egse.services import ServiceProtocol

        self._process_status = ProcessStatus()

        self._timer_thread = threading.Thread(
            target=do_every, args=(PROCESS_SETTINGS.METRICS_INTERVAL, self._process_status.update))
        self._timer_thread.daemon = True
        self._timer_thread.start()

        # The logger will be overwritten by the sub-class, if not, then we use this logger
        # with the name of the sub-class. That will help us to identify which sub-class did not
        # overwrite the logger attribute.

        self.logger = logging.getLogger(get_full_classname(self))

        self.listeners = Listeners()
        self.scheduled_tasks = []

        self.interrupted = False
        self.delay = 1000  # delay between publish status information [milliseconds]
        self.hk_delay = 1000  # delay between saving housekeeping information [milliseconds]

        self.zcontext = zmq.Context.instance()
        self.poller = zmq.Poller()

        self.device_protocol = None  # This will be set in the sub-class
        self.service_protocol = ServiceProtocol(self)
        self.monitoring_protocol = MonitoringProtocol(self)

        # Setup the control server waiting for service requests

        self.dev_ctrl_service_sock = self.zcontext.socket(zmq.REP)
        self.service_protocol.bind(self.dev_ctrl_service_sock)

        # Setup the control server for sending monitoring info

        self.dev_ctrl_mon_sock = self.zcontext.socket(zmq.PUB)
        self.monitoring_protocol.bind(self.dev_ctrl_mon_sock)

        # Setup the control server waiting for device commands.
        # The device protocol shall bind the socket in the sub-class

        self.dev_ctrl_cmd_sock = self.zcontext.socket(zmq.REP)

        # Initialize the poll set

        self.poller.register(self.dev_ctrl_service_sock, zmq.POLLIN)
        self.poller.register(self.dev_ctrl_mon_sock, zmq.POLLIN)

    @abc.abstractmethod
    def get_communication_protocol(self):
        pass

    @abc.abstractmethod
    def get_commanding_port(self):
        pass

    @abc.abstractmethod
    def get_service_port(self):
        pass

    @abc.abstractmethod
    def get_monitoring_port(self):
        pass

    def get_ip_address(self):
        return get_host_ip()

    def get_storage_mnemonic(self):
        return self.__class__.__name__

    def get_process_status(self):
        return self._process_status.as_dict()

    def get_average_execution_times(self):
        return get_average_execution_times()

    def set_delay(self, seconds: float) -> float:
        """
        Sets the delay time for monitoring. The delay time is the time between two successive executions of the
        `get_status()` function of the device protocol.

        It might happen that the delay time that is set is longer than what you requested. That is the case when
        the execution of the `get_status()` function takes longer than the requested delay time. That should
        prevent the server from blocking when a too short delay time is requested.

        Args:
            seconds: the number of seconds between the monitoring calls.
        Returns:
            The delay that was set in milliseconds.
        """
        execution_time = get_average_execution_time(self.device_protocol.get_status)
        self.delay = max(seconds * 1000, (execution_time + 0.2) * 1000)
        return self.delay

    def set_hk_delay(self, seconds) -> float:
        """
        Sets the delay time for housekeeping. The delay time is the time between two successive executions of the
        `get_housekeeping()` function of the device protocol.

        It might happen that the delay time that is set is longer than what you requested. That is the case when
        the execution of the `get_housekeeping()` function takes longer than the requested delay time. That should
        prevent the server from blocking when a too short delay time is requested.

        Args:
            seconds: the number of seconds between the housekeeping calls.
        Returns:
            The delay that was set in milliseconds.
        """
        execution_time = get_average_execution_time(self.device_protocol.get_housekeeping)
        self.hk_delay = max(seconds * 1000, (execution_time + 0.2) * 1000)
        return self.hk_delay

    def set_logging_level(self, level):
        self.logger.setLevel(level=level)

    def quit(self):
        self.interrupted = True

    def before_serve(self):
        pass

    def after_serve(self):
        pass

    def handle_scheduled_tasks(self):
        """
        Executes or reschedules tasks in the `serve()` event loop.
        """
        self.scheduled_tasks.reverse()
        rescheduled_tasks = []
        while self.scheduled_tasks:
            task_info = self.scheduled_tasks.pop()
            task = task_info["task"]
            task_name = task_info.get("name")

            at = task_info.get("after")
            if at and at > datetime.datetime.now(tz=datetime.timezone.utc):
                rescheduled_tasks.append(task_info)
                continue

            condition = task_info.get("condition")
            if condition and not condition():
                rescheduled_tasks.append(task_info)
                continue

            self.logger.debug(f"Running scheduled task: {task_name}")
            try:
                task()
            except Exception as exc:
                self.logger.exception(exc, exc_info=True, stack_info=True)
                self.logger.warning(f"Task {task_name} has failed: {exc!r}")
            else:
                self.logger.debug(f"Scheduled task finished: {task_name}")

        if self.scheduled_tasks:
            self.logger.warning(f"There are still {len(self.scheduled_tasks)} scheduled tasks.")

        if rescheduled_tasks:
            self.scheduled_tasks.append(*rescheduled_tasks)

    def schedule_task(self, callback: Callable, after: float = 0.0, when: Callable = None):
        """
        Schedules a task to run in the control server event loop.

        The `callback` function will be executed as soon as possible in the `serve()` event loop.

        Some simple scheduling options are available:

        * after: the task will only execute 'x' seconds after the time of scheduling. I.e.
          the task will be rescheduled until time > scheduled time + 'x' seconds.
        * when: the task will only execute when the condition is True.

        The `after` and the `when` arguments can be combined.

        Note:
            * This function is intended to be used in order to prevent a deadlock.
            * Since the `callback` function is executed in the `serve()` event loop, it shall not block!

        """
        try:
            name = callback.func.__name__ if isinstance(callback, partial) else callback.__name__
        except AttributeError:
            name = "unknown"

        current_time = datetime.datetime.now(tz=datetime.timezone.utc)
        scheduled_time = current_time + datetime.timedelta(seconds=after)

        self.logger.info(f"Task {name} scheduled")

        self.scheduled_tasks.append({'task': callback, "name": name, "after": scheduled_time, "when": when})

    def serve(self):

        self.before_serve()

        # check if Storage Manager is available

        from egse.storage import is_storage_manager_active

        storage_manager = is_storage_manager_active(timeout=0.1)

        storage_manager and self.register_to_storage_manager()

        # This approach is very simplistic and not time efficient
        # We probably want to use a Timer that executes the monitoring and saving actions at
        # dedicated times in the background.

        last_time = time_in_ms()
        last_time_hk = time_in_ms()

        while True:
            try:
                socks = dict(self.poller.poll(50))  # timeout in milliseconds, do not block
            except KeyboardInterrupt:
                self.logger.warning("Keyboard interrupt caught!")
                self.logger.warning(
                    "The ControlServer can not be interrupted with CTRL-C, "
                    "send a quit command to the server."
                )
                continue

            if self.dev_ctrl_cmd_sock in socks:
                self.device_protocol.execute()

            if self.dev_ctrl_service_sock in socks:
                self.service_protocol.execute()

            # Now handle the periodic sending out of status information. A dictionary with the
            # status or HK info is sent out periodically based on the DELAY time that is in the
            # YAML config file.

            if time_in_ms() - last_time >= self.delay:
                last_time = time_in_ms()
                # self.logger.debug("Sending status to monitoring processes.")
                self.monitoring_protocol.send_status(
                    save_average_execution_time(self.device_protocol.get_status)
                )

            if time_in_ms() - last_time_hk >= self.hk_delay:
                last_time_hk = time_in_ms()
                if storage_manager:
                    # self.logger.debug("Sending housekeeping information to Storage.")
                    self.store_housekeeping_information(
                        save_average_execution_time(self.device_protocol.get_housekeeping)
                    )

            # Handle scheduled tasks/callback functions

            self.handle_scheduled_tasks()

            if self.interrupted:
                self.logger.info(
                    f"Quit command received, closing down the {self.__class__.__name__}."
                )
                break

            # Some device protocol sub-classes might start a number of threads or processes to
            # support the commanding. Check if these threads/processes are still alive and
            # terminate gracefully if they are not.

            if not self.device_protocol.is_alive():
                self.logger.error(
                    "Some Thread or sub-process that was started by Protocol has "
                    "died, terminating..."
                )
                break

        storage_manager and self.unregister_from_storage_manager()

        self.after_serve()

        self.device_protocol.quit()

        self.dev_ctrl_mon_sock.close()
        self.dev_ctrl_service_sock.close()
        self.dev_ctrl_cmd_sock.close()

        close_all_zmq_handlers()

        self.zcontext.term()

    def store_housekeeping_information(self, data):
        """Send housekeeping information to the Storage manager."""

        from egse.storage.storage_cs import StorageControlServer
        from egse.storage import StorageProxy

        if isinstance(self, StorageControlServer):
            self.logger.log(0, f"{self.__class__.__name__} doesn't store housekeeping information.")
            return

        self.logger.log(0, "Sending housekeeping to storage manager.")

        try:
            with StorageProxy() as proxy:
                rc = proxy.save({"origin": self.get_storage_mnemonic(), "data": data})
                if not rc.successful:
                    self.logger.warning(
                        f"Couldn't save data to the Storage manager: {data}, cause: {rc}"
                    )
        except ConnectionError as exc:
            self.logger.warning(
                f"Couldn't connect to the Storage manager to store housekeeping: {exc}"
            )

    def register_to_storage_manager(self):
        """Register this ControlServer to the Storage manager."""

        from egse.storage.storage_cs import StorageControlServer
        from egse.storage import StorageProxy
        from egse.storage.persistence import CSV

        if isinstance(self, StorageControlServer):
            return

        try:
            with StorageProxy() as proxy:
                rc = proxy.register(
                    {
                        "origin": self.get_storage_mnemonic(),
                        "persistence_class": CSV,
                        "prep": {
                            "column_names": list(self.device_protocol.get_housekeeping().keys()),
                            "mode": "a",
                        },
                    }
                )
                if not rc.successful:
                    self.logger.warning(f"Couldn't register to the Storage manager: {rc}")
        except ConnectionError as exc:
            self.logger.warning(f"Couldn't connect to the Storage manager for registration: {exc}")

    def unregister_from_storage_manager(self):
        """Unregister this ControlServer from the Storage manager."""

        from egse.storage.storage_cs import StorageControlServer
        from egse.storage import StorageProxy

        if isinstance(self, StorageControlServer):
            return

        try:
            with StorageProxy() as proxy:
                rc = proxy.unregister({"origin": self.get_storage_mnemonic()})
                if not rc.successful:
                    self.logger.warning(f"Couldn't unregister from the Storage manager: {rc}")

        except ConnectionError as exc:
            self.logger.warning(
                f"Couldn't connect to the Storage manager for de-registration: {exc}"
            )

    def notify_listeners(self, event_id: int = 0, context: dict = None):
        """
        Notifies registered listeners about an event.

        This function creates an Event object with the provided `event_id` and `context`
        and notifies all registered listeners with the created event.

        Args:
            event_id (int, optional): The identifier for the event. Defaults to 0.
            context (dict, optional): Additional context information associated with the event.
                Defaults to None.

        Note:
            The notification is performed by the `notify_listeners` method of the `listeners` object
            associated with this instance.
            The notification is executed in a daemon thread to avoid blocking the commanding
            chain.

        """
        from egse.listener import Event, EVENT_ID

        self.logger.info(f"Notifying listeners for {EVENT_ID(event_id).name}")

        retry_thread = threading.Thread(target=self.listeners.notify_listeners,
                                        args=(Event(event_id=event_id, context=context),))
        retry_thread.daemon = True
        retry_thread.start()

    def get_listener_names(self):
        return self.listeners.get_listener_names()

    def register_as_listener(self, proxy: Type, listener: dict):
        """
        Registers a listener with the specified proxy.

        This function attempts to add the provided listener to the specified proxy.
        It employs a retry mechanism to handle potential ConnectionError exceptions,
        making up to 5 attempts to add the listener.

        Args:
            proxy: A callable object representing the proxy to which the listener will be added.
            listener (dict): The listener to be registered. Should be a dictionary containing
                listener details.

        Raises:
            ConnectionError: If the connection to the proxy encounters issues even after
                multiple retry attempts.

        Note:
            The function runs in a separate daemon thread to avoid blocking the main thread.

        """
        @retry(times=5, exceptions=[ConnectionError])
        def _add_listener(proxy, listener):
            with proxy() as x, x.get_service_proxy() as srv:
                rc = srv.add_listener(listener)
                MODULE_LOGGER.debug(f"Response from service add_listener: {rc}")

        MODULE_LOGGER.info(f"Registering {self.__class__.__name__} to {proxy}")

        retry_thread = threading.Thread(target=_add_listener, args=(proxy, listener))
        retry_thread.daemon = True
        retry_thread.start()

    def unregister_as_listener(self, proxy: Type, listener: dict):
        """
        Removes a registered listener from the specified proxy.

        This function attempts to remove the provided listener from the specified proxy.
        It employs a retry mechanism to handle potential ConnectionError exceptions,
        making up to 5 attempts to add the listener.

        Args:
            proxy: A callable object representing the proxy from which the listener will be removed.
            listener (dict): The listener to be removed. Should be a dictionary containing
                listener details.

        Raises:
            ConnectionError: If the connection to the proxy encounters issues even after
                multiple retry attempts.

        Note:
            The function runs in a separate thread but will block until the de-registration is finished.
            The reason being that this method is usually called in a `after_serve` block so it needs to
            finish before the ZeroMQ context is destroyed.

        """
        @retry(times=5, exceptions=[ConnectionError])
        def _remove_listener(proxy, listener):
            with proxy() as x, x.get_service_proxy() as srv:
                rc = srv.remove_listener(listener)

        endpoint = proxy().get_endpoint()
        if not is_control_server_active(endpoint, timeout=0.5):
            MODULE_LOGGER.warning(f"The {endpoint} endpoint is not responding, {listener['name']} not un-registered.")
            return

        MODULE_LOGGER.info(f"Removing {self.__class__.__name__} from {proxy}")

        retry_thread = threading.Thread(target=_remove_listener, args=(proxy, listener))
        retry_thread.daemon = False
        retry_thread.start()

        # Block until the listener has been removed. This is needed because this unregister function will usually
        # be called in the `after_server()` method of the control server (which is the listener) and if we do not
        # wait until the thread is finished the ZeroMQ Context will be destroyed before the reply can be sent.
        # Note: we could probably do without the thread, and directly call the `_remove_listener()` function.

        retry_thread.join()
