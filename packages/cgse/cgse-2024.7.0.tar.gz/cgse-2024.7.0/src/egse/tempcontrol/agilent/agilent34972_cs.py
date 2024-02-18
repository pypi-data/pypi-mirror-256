#!/usr/bin/env python3
import logging
import multiprocessing

import click
import sys
import zmq
from prometheus_client import start_http_server

multiprocessing.current_process().name = "agilent34972_cs"

from egse.control import ControlServer
from egse.settings import Settings
from egse.tempcontrol.agilent.agilent34972 import Agilent34972Proxy
from egse.tempcontrol.agilent.agilent34972_protocol import Agilent34972Protocol


logging.basicConfig(level=logging.DEBUG, format=Settings.LOG_FORMAT_FULL)

logger = logging.getLogger('__name__')

CTRL_SETTINGS = Settings.load("Agilent 34972 Control Server")


class Agilent34972ControlServer(ControlServer):

    def __init__(self, index):
        self.index = index
        self.name = "DAQ"+str(index)
        super(Agilent34972ControlServer, self).__init__()

        self.device_protocol = Agilent34972Protocol(self, self.index)

        logger.debug(f'Binding ZeroMQ socket to {self.device_protocol.get_bind_address()}')

        self.device_protocol.bind(self.dev_ctrl_cmd_sock)

        self.poller.register(self.dev_ctrl_cmd_sock, zmq.POLLIN)

        self.set_hk_delay(CTRL_SETTINGS.DELAY)

    def get_communication_protocol(self):
        return CTRL_SETTINGS.PROTOCOL

    def get_commanding_port(self):
        return CTRL_SETTINGS[self.name]['COMMANDING_PORT']

    def get_service_port(self):
        return CTRL_SETTINGS[self.name]['SERVICE_PORT']

    def get_monitoring_port(self):
        return CTRL_SETTINGS[self.name]['MONITORING_PORT']

    def get_storage_mnemonic(self):
        try:
            return CTRL_SETTINGS[self.name]['STORAGE_MNEMONIC']
        except:
            return f'Agilent34972_{self.index}'

    def before_serve(self):
        start_http_server(CTRL_SETTINGS[self.name]['METRICS_PORT'])


@click.group()
def cli():
    pass


@cli.command()
@click.option("--simulator", "--sim", is_flag=True, help="Start the Agilent34972 Simulator as the backend.")
@click.argument('index', type=click.IntRange(0, 1))
def start(simulator, index):
    """Start the BeagleBone Control Server."""

    if simulator:
        Settings.set_simulation_mode(True)
    try:
        logger.debug(f'Starting Agilent 34972 {index} Control Server')
        
        multiprocessing.current_process().name = f"agilent34972_cs_{index}"

        control_server = Agilent34972ControlServer(index)
        control_server.serve()

    except KeyboardInterrupt:
        logger.info("Shutdown requested...exiting")

    except SystemExit as exit_code:
        logger.info("System Exit with code {}.".format(exit_code))
        sys.exit(exit_code)

    except Exception:

        logger.exception("Cannot start the Agilent Control Server")
        # The above line does exactly the same as the traceback, but on the logger
        # import traceback
        # traceback.print_exc(file=sys.stdout)

    return 0


@cli.command()
@click.argument('index', type=click.IntRange(0, 1))
def stop(index):
    """Send a 'quit_server' command to the Control Server."""

    with Agilent34972Proxy(index) as proxy:

        sp = proxy.get_service_proxy()
        sp.quit_server()


if __name__ == "__main__":

    sys.exit(cli())
