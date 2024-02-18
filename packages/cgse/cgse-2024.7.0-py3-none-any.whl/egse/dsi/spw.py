"""
This module contains functions to handle SpaceWire communication.
"""
from __future__ import annotations

import logging
import socket
import textwrap
from typing import Tuple

import egse.rmap
import egse.spw
from egse.dsi import constants
from egse.dsi.constants import esl_rmap_error_codes
from egse.dsi.esl import ESLError
from egse.dsi.esl import esl_close_connection
from egse.dsi.esl import esl_configure
from egse.dsi.esl import esl_flush
from egse.dsi.esl import esl_get_active_link
from egse.dsi.esl import esl_get_hwa
from egse.dsi.esl import esl_get_manufacturer_string
from egse.dsi.esl import esl_get_number_of_links
from egse.dsi.esl import esl_get_product_string
from egse.dsi.esl import esl_get_serial_number
from egse.dsi.esl import esl_open_connection
from egse.dsi.esl import esl_read_packet
from egse.dsi.esl import esl_send_timecode
from egse.dsi.esl import esl_set_active_link
from egse.dsi.esl import esl_write_packet
from egse.dsi.rmap import rmap_configure
from egse.dsi.rmap import rmap_open_connection
from egse.settings import Settings
from egse.spw import SpaceWireInterface
from egse.spw import SpaceWirePacket
from egse.spw import WriteRequestReply
from egse.spw import ReadRequestReply

LOGGER = logging.getLogger(__name__)

DSI_SETTINGS = Settings.load("DSI")

# Naming conventions:
#
# rx_buffer:
#     is used for any buffer (of type bytes) that is or was received over the SpaceWire interface.
# tx_buffer:
#     is used for any buffer (of type bytes) that will be transmitted over the SpaceWire interface.


def handle_extension_packet(rx_buffer: bytes, bytes_received: int):
    """
    Decide how to handle the extension packet that was received over the SpaceWire.

    The following extension packets are supported:

    * a timecode packet

    Args:
        rx_buffer (bytes): the packet that was received as a bytes object
        bytes_received (int): the length of the rx_buffer (allocated space might be larger)

    Returns:
        Nothing: yet.

    """
    LOGGER.debug("*" * 80)
    LOGGER.debug("Extension Packet returned by DSI")
    LOGGER.debug(
        f"extension packet: {bin(int.from_bytes(rx_buffer, 'big'))} (length={bytes_received})"
    )
    LOGGER.debug("*" * 80)


def handle_special_packet(rx_buffer: bytes, bytes_received: int):
    """
    Decide how to handle a special packet that was received over the SpaceWire interface.

    Args:
        rx_buffer (bytes): the packet that was received as a bytes object
        bytes_received (int): the length of the rx_buffer (allocated space might be larger)

    Returns:
        Nothing: yet.

    """
    LOGGER.debug("*" * 80)
    LOGGER.debug("Special Packet returned by DSI")
    LOGGER.debug(f"Special packet: {rx_buffer} (length={bytes_received})")
    LOGGER.debug("*" * 80)


class SpaceWireOverDSI(SpaceWireInterface):
    """
    The SpaceWireOverDSI implements the SpaceWire communication/transport over a Diagnostic
    SpaceWire Interface (DSI).
    """

    def __init__(self, dsi_address, dsi_port, esl_link=None, rmap_link=None):
        self.dsi_address = dsi_address
        self.dsi_port = dsi_port
        self.esl_link = esl_link
        self.rmap_link = rmap_link
        self.socket = None

    def __str__(self):
        hwa = esl_get_hwa(self.esl_link)
        serial_number = esl_get_serial_number(self.esl_link)

        msg = textwrap.dedent(f"""\
            Info on SpaceWire Interface:
              Manufacturer      {esl_get_manufacturer_string(self.esl_link)}
              Product           {esl_get_product_string(self.esl_link)}
              Number of links   {esl_get_number_of_links(self.esl_link)} [active port={esl_get_active_link(self.esl_link)}]
              Serial number     {serial_number}
              Hardware Address  0x{hwa[0]:02X}-{hwa[1]:02X}-{hwa[2]:02X}-{hwa[3]:02X}-{hwa[4]:02X}-{hwa[5]:02X}
            """
        )

        return msg

    def connect(self):
        if self.esl_link is None:
            self.esl_link = esl_open_connection(self.dsi_address)
        if self.rmap_link is None:
            self.rmap_link = rmap_open_connection(self.esl_link)
        # esl_print_info(self.esl_link)

    def disconnect(self):
        esl_close_connection(self.esl_link)

    def configure(self):
        esl_configure(
            self.esl_link,
            active_link=self.dsi_port,
            speed=DSI_SETTINGS.LINK_SPEED,
            mode=constants.ESL_LINK_MODE_NORMAL,
            report=constants.ESL_ER_REPORT_PARITY_ERROR
            | constants.ESL_ER_REPORT_TIME_CODE
            | constants.ESL_ER_REPORT_ESC_EOP
            | constants.ESL_ER_REPORT_ESC_EEP
            | constants.ESL_ER_REPORT_ESC_ESC
            | constants.ESL_ER_REPORT_TIMEOUT,
        )

        rmap_configure(
            self.rmap_link,
            target_key=constants.RMAP_TARGET_KEY,
            initiator_logical_address=DSI_SETTINGS.INITIATOR_LOGICAL_ADDRESS,
            target_logical_address=DSI_SETTINGS.TARGET_LOGICAL_ADDRESS,
        )

        # esl_print_summary_of_structure(self.esl_link)

    def get_socket(self):
        """
        Returns the TCP socket that is associated with this transport.

        Returns:
            A TCP socket or None when the transport has not been initialized or connected.
        """
        # This 'trick' of getting the socket from the `fileno` works only once, so, if we have already
        # requested the socket for this `fileno`, don't do it again. It will either result in a
        # `OSError: [Errno 9] Bad file descriptor` or I've seen that a new socket created with the same
        # family and type will reuse the same `fileno` down the line...

        if self.socket is None and self.esl_link is not None:
            sock_fd = self.esl_link.contents.sock
            self.socket = socket.socket(fileno=sock_fd)  # This is how to get the socket from the esl_connection.

        return self.socket

    def set_active_link(self, port: int):
        """
        Sets the active SpW port on the DSI.

        Raises:
            An ESLError when an invalid link is provided.

        Returns:
            The return code of the library call.
        """
        rc = esl_set_active_link(self.esl_link, port)
        if rc == constants.ESL_API_INVALID_LINK:  # noqa
            raise ESLError(
                f"Could not set active link {port}, ESL error: Invalid Link selected [-45]."
            )

        return rc

    def get_active_link(self):
        """Return the number of the currently active SpW port on the DSI."""
        return esl_get_active_link(self.esl_link)

    def flush(self):
        esl_flush(self.esl_link)

    def send_timecode(self, timecode: int) -> int:
        return esl_send_timecode(self.esl_link, timecode)

    def read_packet(self, timeout: int = None) -> Tuple[int, bytes]:
        return esl_read_packet(self.esl_link, timeout=timeout)

    def write_packet(self, packet: bytes) -> int:
        return esl_write_packet(self.esl_link, packet, len(packet), constants.ESL_EOP)  # noqa

    def read_register(self, address: int, length: int = 4, strict: bool = True) -> bytes:
        reply_packet = self.rmap_read_request(address, length, strict=strict)

        if reply_packet is None:
            LOGGER.critical(f"read_register() failed: An error occurred in the rmap_read_request() call.")
            return bytes()

        return reply_packet.data

    def write_register(self, address: int, data: bytes) -> int:
        reply_packet = self.rmap_write_request(address, data)

        if reply_packet is None:
            LOGGER.critical(f"write_register() failed: An error occurred in the rmap_write_request() call.")
            return -1

        if reply_packet.status:
            LOGGER.warning(f"write_register() failed: An error occurred in the rmap_write_request() call: "
                           f"{reply_packet.status = }")

        return reply_packet.status

    def read_memory_map(self, address: int, size: int) -> bytes:
        reply_packet = self.rmap_read_request(address, size, strict=False)

        if reply_packet is None:
            LOGGER.critical(f"read_memory_map(): An error occurred in the rmap_read_request() call.")
            return bytes()

        return reply_packet.data

    def rmap_read_request(
            self, address: int, length: int, timeout: int = 1000, strict: bool = True) -> ReadRequestReply | None:
        """
        Read `length` bytes from the remote memory starting at `address`.

        Args:
            address: the start address (32-bit aligned) in the remote memory
            length: the number of bytes to read from the remote memory
            timeout: timeout in milliseconds
            strict: perform strict checking of read areas

        Returns:
            A tuple containing the terminator value and the RMAP Reply packet with the data read from
            the remote memory.

        """
        # TODO:
        #   the timeout parameter is currently not implemented

        self.rmap_link.transaction_identifier = egse.spw.update_transaction_identifier(self.rmap_link.transaction_identifier)

        buffer = egse.rmap.create_rmap_read_request_packet(
            address, length, self.rmap_link.transaction_identifier, strict=strict)

        result = esl_write_packet(self.rmap_link.spw_device, buffer, len(buffer), constants.ESL_EOP)  # noqa
        if result:
            raise egse.rmap.RMAPError(
                f"Couldn't send data within timeout of {timeout} ms, "
                f"ESL RMAP Error Code = {esl_rmap_error_codes[self.rmap_link.ESL_RMAP_error]} ["
                f"{self.rmap_link.ESL_RMAP_error}]")

        result = esl_flush(self.rmap_link.spw_device)
        if result:
            raise egse.rmap.RMAPError(
                f"Couldn't send data or clear buffers, "
                f"ESL RMAP Error Code = {esl_rmap_error_codes[self.rmap_link.ESL_RMAP_error]} ["
                f"{self.rmap_link.ESL_RMAP_error}]")

        # Read the read request reply packet

        _, rx_buffer = esl_read_packet(self.rmap_link.spw_device, timeout=timeout)

        if rx_buffer:
            reply_packet = SpaceWirePacket.create_packet(rx_buffer)
            return reply_packet if isinstance(reply_packet, ReadRequestReply) else None

        return None

    def rmap_write_request(
            self, address: int, data: bytes, length: int = 4, timeout: int = 1000) -> WriteRequestReply | None:
        """
        Sends an RMAP write command over the SpaceWire link.

        Based on the address this function will decided to send a verified or unverified write request.

        TODO: the timeout parameter is currently not implemented.

        Args:
            address: the starting memory address to which the data from buffer will be written
            data: the data that will be written into the targets memory
            length: the number of bytes to write (the buffer maybe longer) [default=4]
            timeout: timeout in milliseconds [default=1000]

        Returns:
            The Write Request Reply packet.

        Raises:
            egse.rmap.RMAPError: when data can not be written on the target.

        """

        self.rmap_link.transaction_identifier = egse.spw.update_transaction_identifier(
            self.rmap_link.transaction_identifier
        )

        if egse.rmap.CRITICAL_AREA_START <= address <= egse.rmap.CRITICAL_AREA_END:
            buffer = egse.rmap.create_rmap_verified_write_packet(
                address, data, self.rmap_link.transaction_identifier)
        else:
            buffer = egse.rmap.create_rmap_unverified_write_packet(
                address, data, length, self.rmap_link.transaction_identifier)

        result = esl_write_packet(self.esl_link, buffer, len(buffer), constants.ESL_EOP)  # noqa
        if result:
            raise egse.rmap.RMAPError(f"Couldn't send data ({len(buffer)} bytes) within timeout of {timeout} ms.")

        result = esl_flush(self.esl_link)
        if result:
            raise egse.rmap.RMAPError(f"Couldn't send data or flush buffers.")

        # Read the write request reply message

        _, rx_buffer = esl_read_packet(self.esl_link)

        if rx_buffer:
            reply_packet = SpaceWirePacket.create_packet(rx_buffer)
            return reply_packet if isinstance(reply_packet, WriteRequestReply) else None

        return None
