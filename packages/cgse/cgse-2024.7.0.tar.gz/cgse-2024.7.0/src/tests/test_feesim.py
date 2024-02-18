"""
Testing the FEE Simulator:

Pre-requisites:

* core services must be running

"""
import logging
import time
import timeit
from contextlib import contextmanager

import pytest

import egse.dsi.constants
import egse.dsi.esl
from egse.dsi.esl import esl_connection
from egse.dsi.rmap import rmap_connection
from egse.dsi.spw import SpaceWireOverDSI
from egse.process import SubProcess
from egse.process import is_process_running
from egse.settings import Settings
from egse.spw import HousekeepingPacket
from egse.spw import SpaceWirePacket
from egse.spw import TimecodePacket
from egse.system import ping
from egse.system import waiting_for

logger = logging.getLogger("egse.test_feesim")

TIMEOUT_MS = 1000  # Timeout in milliseconds

dsi_settings = Settings.load("DSI")

dsi_available = True if ping(dsi_settings.DSI_FEE_IP_ADDRESS) else False


@contextmanager
def fee_simulator(endpoint: str = None, port: int = 1):
    """
    Context manager that starts the FEE Simulator in a sub-process.
    """

    if endpoint is None:
        cmd_args = ["--zeromq"]
    else:
        cmd_args = [f"-a {endpoint}", f"-p {port}"]

    if is_process_running(items=["feesim", "start"]):
        pytest.xfail("FEESIM is already running")

    feesim = SubProcess("N-FEE Simulator", ["feesim", "start"], cmd_args)
    feesim.execute()

    try:
        waiting_for(is_process_running, ["feesim", "start"], interval=1.0, timeout=5.0)
    except TimeoutError as exc:
        raise RuntimeError("Couldn't start the N-FEE Simulator within the given time of 5s.") from exc

    time.sleep(2.0)  # give the process time to initialize

    try:
        yield feesim
    finally:
        feesim.quit()


@pytest.mark.skipif(not dsi_available,
                    reason="requires DSI to be connected")
def test_mode_setting():

    with fee_simulator(endpoint='192.168.0.18:4949') as feesim:
        logger.info(f'FEE Simulator PID: {feesim.pid}')

        dsi_address = "192.168.0.19"
        dsi_port = 1

        rxbuf = bytearray(dsi_settings.RX_BUFFER_LENGTH)
        txbuf = bytearray(dsi_settings.TX_BUFFER_LENGTH)

        with esl_connection(dsi_address) as esl_link, rmap_connection(esl_link) as rmap_link:

            transport = SpaceWireOverDSI(dsi_address, dsi_port, esl_link, rmap_link)
            transport.configure()

            # The following code is now replaced by the transport.configure() method:
            # status = egse.dsi.esl.esl_set_active_link(esl_link, 1)
            # logger.info(f"esl_set_active_link(esl_link, 1) -> {status=}")
            # status = egse.dsi.esl.esl_set_speed(esl_link, dsi_settings.LINK_SPEED)
            # logger.info(f"esl_set_speed(esl_link, {dsi_settings.LINK_SPEED}) -> {status=}")
            # status = egse.dsi.esl.esl_set_mode(esl_link, egse.dsi.constants.ESL_LINK_MODE_NORMAL)
            # logger.info(f"esl_set_mode(esl_link, {egse.dsi.constants.ESL_LINK_MODE_NORMAL}) -> {status=}")
            # status = egse.dsi.esl.esl_flush(esl_link)
            # logger.info(f"esl_flush(esl_link) -> {status=}")
            #
            # logger.info(f'Receive Timeout = {egse.dsi.esl.esl_get_rx_timeout(esl_link)} ms')
            # egse.dsi.esl.esl_set_rx_timeout(esl_link, TIMEOUT_MS)
            # logger.info(f'Receive Timeout = {egse.dsi.esl.esl_get_rx_timeout(esl_link)} ms')

            wait_for_hk_packet(transport)

            # The following lines will run the read_write test count times.
            # I commented out the print statements so that the terminal output doesn't slow down the process.
            # Be careful also to set the logging level to INFO instead of DEBUG in the different parts.
            #
            # timeit (number=1000) returned about 16 sec to run over an ssh tunnel and about 14s without ssh tunneling
            # 05/02/2024 — test at home with P-DSI2 — timeit(number=1000) returned after 1.6s

            count = 1000
            wrapped = wrapper(do_read_write_test, transport, rxbuf, txbuf)
            logger.info("{} runs took {} seconds".format(count, timeit.timeit(wrapped, number=count)))

            logger.info(f'Receive Timeout = {egse.dsi.esl.esl_get_rx_timeout(esl_link)} ms')

        # time.sleep(5.0)


def wait_for_hk_packet(transport):
    packet_type = TimecodePacket
    while True:
        terminator, data = transport.read_packet(timeout=1000)
        if data is None or len(data) in (0, 1):
            continue
        packet = SpaceWirePacket.create_packet(data)
        logger.info(packet)
        if isinstance(packet, packet_type):
            if packet_type is HousekeepingPacket:
                break
            else:
                packet_type = HousekeepingPacket
                continue


def do_read_write_test(transport: SpaceWireOverDSI, rxbuf, txbuf):

    try:
        reply_packet = transport.rmap_read_request(0, 16, TIMEOUT_MS, strict=False)
        # logger.info(f"{reply_packet = }")

        # Change the 8 bytes [2:10] of the buffer and send an RMAP write command
        rxbuf[2:10] = [0xFF - i for i in range(8)]
        reply_packet = transport.rmap_write_request(0, rxbuf, 8, TIMEOUT_MS)
        # logger.info(f"{reply_packet = }")

        reply_packet = transport.rmap_read_request(0, 8, TIMEOUT_MS, strict=False)
        # logger.info(f"{reply_packet = }")

        # Clear the buffers

        rxbuf[:20] = [0 for i in range(20)]
        txbuf[:20] = [0 for i in range(20)]

        reply_packet = transport.rmap_write_request(0, rxbuf, 8, TIMEOUT_MS)
        # logger.info(f"{reply_packet = }")

    except Exception as exc:
        logger.error(exc, exc_info=True)


def wrapper(func, *args, **kwargs):
    """Allows a function to run with timeit."""
    def wrapped():
        return func(*args, **kwargs)
    return wrapped
