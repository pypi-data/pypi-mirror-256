"""
This module provides dummy implementation for classes of the Commanding chain.
"""
import logging
import multiprocessing
import pickle
import random
import sys
import threading
import time
from functools import partial

import click
import zmq

from egse.command import ClientServerCommand
from egse.confman import is_configuration_manager_active
from egse.control import ControlServer
from egse.control import is_control_server_active
from egse.decorators import dynamic_interface
from egse.listener import Event
from egse.listener import EventInterface
from egse.protocol import CommandProtocol
from egse.proxy import Proxy
from egse.settings import Settings
from egse.system import AttributeDict
from egse.system import format_datetime
from egse.zmq_ser import bind_address
from egse.zmq_ser import connect_address

logging.basicConfig(level=logging.DEBUG, format=Settings.LOG_FORMAT_FULL)
LOGGER = logging.getLogger("egse.dummy")

# Especially DummyCommand and DummyController need to be defined in a known module
# because those objects are pickled and when de-pickled at the clients side the class
# definition must be known.

# We use AttributeDict here to define the settings, because that is how the Settings.load() returns
# settings loaded from a YAML file.

ctrl_settings = AttributeDict(
    {
        'HOSTNAME': 'localhost',
        'COMMANDING_PORT': 4443,
        'SERVICE_PORT': 4444,
        'MONITORING_PORT': 4445,
        'PROTOCOL': 'tcp',
        'TIMEOUT': 10,
        'HK_DELAY': 1.0,
    }
)

commands = AttributeDict(
    {
        'info': {
            'description': 'Info on the Dummy Controller',
            'response': 'handle_device_method'
        },
        'response': {
            'description': 'send a command to the device and return it\'s response',
            'device_method': 'response',
            'cmd': '{one} {two} {fake}',
            'response': 'handle_device_method'
        },
        'handle_event': {
            'description': "Notification of an event",
            'device_method': 'handle_event',
            'cmd': '{event}',
            'response': 'handle_device_method'
        },
    }
)

def is_dummy_cs_active():
    return is_control_server_active(
        endpoint=connect_address(ctrl_settings.PROTOCOL, ctrl_settings.HOSTNAME, ctrl_settings.COMMANDING_PORT)
    )


class DummyCommand(ClientServerCommand):
    pass


class DummyInterface:
    @dynamic_interface
    def info(self):
        ...
    @dynamic_interface
    def response(self, *args, **kwargs):
        ...


class DummyProxy(Proxy, DummyInterface, EventInterface):
    def __init__(self,
                 protocol=ctrl_settings.PROTOCOL, hostname=ctrl_settings.HOSTNAME, port=ctrl_settings.COMMANDING_PORT):
        """
        Args:
            protocol: the transport protocol [default is taken from settings file]
            hostname: location of the control server (IP address) [default is taken from settings file]
            port: TCP port on which the control server is listening for commands [default is taken from settings file]
        """
        super().__init__(connect_address(protocol, hostname, port), timeout=ctrl_settings.TIMEOUT)


class DummyController(DummyInterface, EventInterface):
    def __init__(self, control_server):
        self._cs = control_server

    def info(self):
        return "method info() called on DummyController"

    def response(self, *args, **kwargs):
        return f"response({args}, {kwargs})"

    def handle_event(self, event: Event) -> str:

        _exec_in_thread = False

        def _handle_event(event):
            LOGGER.info(f"An event is received, {event=}")
            LOGGER.info(f"CM CS active? {is_configuration_manager_active()}")
            time.sleep(5.0)
            LOGGER.info(f"CM CS active? {is_configuration_manager_active()}")
            LOGGER.info(f"An event is processed, {event=}")

        if _exec_in_thread:
            # We execute this function in a daemon thread so the acknowledgment is
            # sent back immediately (the ACK means 'command received and will be
            # executed).

            retry_thread = threading.Thread(target=_handle_event, args=(event,))
            retry_thread.daemon = True
            retry_thread.start()
        else:
            # An alternative to the daemon thread is to create a scheduled task that will be executed
            # after the event is acknowledged.

            self._cs.schedule_task(partial(_handle_event, event))

        return "ACK"


class DummyProtocol(CommandProtocol):

    def __init__(self, control_server: ControlServer):
        super().__init__()
        self.control_server = control_server

        self.device_controller = DummyController(control_server)

        self.load_commands(commands, DummyCommand, DummyController)

        self.build_device_method_lookup_table(self.device_controller)

        self._count = 0

    def get_bind_address(self):
        return bind_address(self.control_server.get_communication_protocol(), self.control_server.get_commanding_port())

    def get_status(self):
        return super().get_status()

    def get_housekeeping(self) -> dict:

        # LOGGER.debug(f"Executing get_housekeeping function for {self.__class__.__name__}.")

        self._count += 1

        # use the sleep to test the responsiveness of the control server when even this get_housekeeping function takes
        # a lot of time, i.e. up to several minutes in the case of data acquisition devices
        # import time
        # time.sleep(2.0)


        return {
            'timestamp': format_datetime(),
            'COUNT': self._count,
            'PI': 3.14159,  # just to have a constant parameter
            'Random': random.randint(0, 100),  # just to have a variable parameter
        }


class DummyControlServer(ControlServer):
    """
    DummyControlServer - Command and monitor dummy device controllers.

    The sever binds to the following ZeroMQ sockets:

    * a REQ-REP socket that can be used as a command server. Any client can connect and
      send a command to the dummy device controller.

    * a PUB-SUP socket that serves as a monitoring server. It will send out status
      information to all the connected clients every DELAY seconds.

    """

    def __init__(self):
        multiprocessing.current_process().name = "dummy_cs"

        super().__init__()

        self.device_protocol = DummyProtocol(self)

        self.logger.info(f"Binding ZeroMQ socket to {self.device_protocol.get_bind_address()}")

        self.device_protocol.bind(self.dev_ctrl_cmd_sock)

        self.poller.register(self.dev_ctrl_cmd_sock, zmq.POLLIN)

        self.set_hk_delay(ctrl_settings.HK_DELAY)

        from egse.confman import ConfigurationManagerProxy
        from egse.listener import EVENT_ID

        self.register_as_listener(
            proxy=ConfigurationManagerProxy,
            listener={'name': 'Dummy CS', 'proxy': DummyProxy, 'event_id': EVENT_ID.SETUP}
        )


    def get_communication_protocol(self):
        return 'tcp'

    def get_commanding_port(self):
        return ctrl_settings.COMMANDING_PORT

    def get_service_port(self):
        return ctrl_settings.SERVICE_PORT

    def get_monitoring_port(self):
        return ctrl_settings.MONITORING_PORT

    def get_storage_mnemonic(self):
        return "DUMMY-HK"

    def after_serve(self):
        from egse.confman import ConfigurationManagerProxy

        self.unregister_as_listener(proxy=ConfigurationManagerProxy, listener={'name': 'Dummy CS'})


@click.group()
def cli():
    pass

@click.group()
def control_server():
    pass

cli.add_command(control_server)

@control_server.command()
def start():
    """Start the dummy control server on localhost."""
    from egse.dummy import DummyControlServer

    try:
        control_server = DummyControlServer()
        control_server.serve()
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
    except SystemExit as exit_code:
        print("System Exit with code {}.".format(exit_code))
        sys.exit(exit_code)
    except Exception:
        import traceback
        traceback.print_exc(file=sys.stdout)

@control_server.command()
def stop():
    """Send a quit service command to the dummy control server."""
    with DummyProxy() as dummy:
        sp = dummy.get_service_proxy()
        sp.quit_server()


@cli.command()
@click.argument('hostname')
@click.argument('port')
@click.option('--pickle/--no-pickle', 'use_pickle', default=True)
def monitoring(use_pickle: bool, hostname: str = 'localhost', port: int = None):
    """Monitor the status of a control server on hostname.

    The port number shall correspond to the port number on which the server is publishing
    information with the ZeroMQ PUB-SUB protocol.

    The response from the server (the data or string that was published) is logged at INFO level.

    Arguments:

        hostname: the IP address or hostname of the server

        port: the port to connect to (this is the port to which the server binds)

    Options:

        --pickle or --no-pickle: use pickle to de-serialize the response
    """
    context = zmq.Context()

    receiver = context.socket(zmq.SUB)
    receiver.connect(f"tcp://{hostname}:{port}")
    receiver.setsockopt_string(zmq.SUBSCRIBE, "")

    while True:
        try:
            response = receiver.recv()
            if use_pickle:
                response = pickle.loads(response)

            LOGGER.info(response)
        except KeyboardInterrupt:
            LOGGER.info("KeyboardInterrupt caught!")
            break


if __name__ == "__main__":
    cli()
