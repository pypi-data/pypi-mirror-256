"""
The Configuration Manager is a server that controls and distributes configuration settings.

The following functionality is provided:

* creation and distribution of observation identifiers
* start and end of observations or tests
* maintain proper Setups and distribute the latest Setup on demand

"""
import logging
import multiprocessing
import sys
from pathlib import Path

import click
import zmq
from prometheus_client import start_http_server

from egse.confman import ConfigurationManagerProtocol
from egse.confman import ConfigurationManagerProxy
from egse.confman import is_configuration_manager_active
from egse.control import ControlServer
from egse.control import Response
from egse.control import Success
from egse.settings import Settings
from egse.system import replace_environment_variable

# Use explicit name here otherwise the logger will probably be called __main__

logger = logging.getLogger(__name__)

CTRL_SETTINGS = Settings.load("Configuration Manager Control Server")


class ConfigurationManagerControlServer(ControlServer):
    def __init__(self):
        super().__init__()

        self.device_protocol = ConfigurationManagerProtocol(self)

        self.logger = logger
        self.logger.debug(f"Binding ZeroMQ socket to {self.device_protocol.get_bind_address()}")

        self.device_protocol.bind(self.dev_ctrl_cmd_sock)

        self.poller.register(self.dev_ctrl_cmd_sock, zmq.POLLIN)

    def get_communication_protocol(self):
        return CTRL_SETTINGS.PROTOCOL

    def get_commanding_port(self):
        return CTRL_SETTINGS.COMMANDING_PORT

    def get_service_port(self):
        return CTRL_SETTINGS.SERVICE_PORT

    def get_monitoring_port(self):
        return CTRL_SETTINGS.MONITORING_PORT

    def get_storage_mnemonic(self):
        try:
            return CTRL_SETTINGS.STORAGE_MNEMONIC
        except AttributeError:
            return "CM"

    def before_serve(self):
        start_http_server(CTRL_SETTINGS.METRICS_PORT)


@click.group()
def cli():
    pass


@cli.command()
def start():
    """
    Starts the Configuration Manager (cm_cs). The cm_cs is a server which handles the
    configuration (aka Setup) of your test system.

    The cm_cs is normally started automatically on egse-server boot.
    """

    multiprocessing.current_process().name = "confman_cs"

    try:
        check_prerequisites()
    except RuntimeError as exc:
        logger.info(exc)
        return 0

    try:
        control_server = ConfigurationManagerControlServer()
        control_server.serve()
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
    except SystemExit as exit_code:
        print("System Exit with code {}.".format(exit_code))
        sys.exit(exit_code)
    except Exception:
        import traceback

        traceback.print_exc(file=sys.stdout)

    return 0


@cli.command()
def stop():
    """Send a 'quit_server' command to the Configuration Manager."""
    with ConfigurationManagerProxy() as cm:
        sp = cm.get_service_proxy()
        sp.quit_server()


@cli.command()
def status():
    """Print the status of the control server."""

    import rich

    rich.print('Configuration manager:')
    if is_configuration_manager_active():
        rich.print('  Status: [green]active')
        with ConfigurationManagerProxy() as cm:
            obsid: Success = cm.get_obsid()
            obsid = obsid.return_code
            setup = cm.get_setup()
            try:
                rich.print(f"  Site ID: {setup.site_id}")
            except AttributeError:
                rich.print('  Site ID: [red]UNKNOWN')

            if obsid:
                rich.print(f"  Running observation: {obsid}")
            else:
                rich.print("  No observation running")

            try:
                if setup.has_private_attribute("_setup_id"):
                    setup_id = setup.get_private_attribute("_setup_id")
                    rich.print(f"  Setup loaded: {setup_id}")
                else:
                    rich.print('  [red]No Setup loaded')
            except Exception as exc:
                rich.print(setup)
                rich.print(exc)

            rich.print(f"  Hostname: {cm.get_ip_address()}")
            rich.print(f"  Monitoring port: {cm.get_monitoring_port()}")
            rich.print(f"  Commanding port: {cm.get_commanding_port()}")
            rich.print(f"  Service port: {cm.get_service_port()}")
            rich.print(f"  Listeners: {', '.join(cm.get_listener_names())}")
    else:
        rich.print('  Status: [red]not active')


@cli.command()
def list_setups(**attr):
    """List available Setups."""

    with ConfigurationManagerProxy() as cm:
        setups = cm.list_setups(**attr)
    if setups:
        # We want to have the most recent (highest id number) last, but keep the site together
        setups = sorted(setups, key=lambda x: (x[1], x[0]))
        print("\n".join(f"{setup}" for setup in setups))


@cli.command()
@click.argument('setup_id', type=int)
def load_setup(setup_id):
    """Load the given Setup on the configuration manager."""

    with ConfigurationManagerProxy() as cm:
        setup = cm.load_setup(setup_id)
    if isinstance(setup, Response):
        print(setup)
        return
    if setup.has_private_attribute("_setup_id"):
        setup_id = setup.get_private_attribute("_setup_id")
        print(f"{setup_id} loaded on configuration manager.")


@cli.command()
def reload_setups():
    """ Clears the cache and re-loads the available setups.

    Note that this does not affect the currently loaded setup.
    """

    with ConfigurationManagerProxy() as pm:
        pm.reload_setups()


def check_prerequisites():
    """Checks if all prerequisites for running the Configuration Manager are met.

    Raises:
        RuntimeError when one or more of the prerequisites is not met.
    """

    fails = 0

    # We need a proper location for storing the configuration data.

    location = CTRL_SETTINGS.FILE_STORAGE_LOCATION
    location = replace_environment_variable(location)

    if not location:
        raise RuntimeError(
            "The environment variable referenced in the Settings.yaml file for the "
            "FILE_STORAGE_LOCATION of the Configuration Manager does not exist, please set "
            "the environment variable."
        )

    location = Path(location)

    if not location.exists():
        logger.error(
            f"The directory {location} does not exist, provide a writable location for "
            f"storing the configuration data."
        )
        fails += 1

    # logger.debug(f"Storage location for configuration data = {location}")

    # now raise the final verdict

    if fails:
        raise RuntimeError(
            "Some of the prerequisites for the Configuration Manager haven't met. "
            "Please check the logs."
        )


if __name__ == "__main__":

    sys.exit(cli())
