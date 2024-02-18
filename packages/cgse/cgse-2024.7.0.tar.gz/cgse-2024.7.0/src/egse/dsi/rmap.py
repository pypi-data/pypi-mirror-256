"""
This module provides a Python interface to RMAP command packets.
"""

# Originally, the RMAP functions were wrappers to functions defined in a C library. However, that
# library is not maintained anymore by 4Links, and we have now converted all functionality into
# Python functions. The functions depend heavily on a C structure which we had to re-define using
# the Structure class provided by ctypes. The RMAP Python functions are defined in `egse.rmap`.


import ctypes
import logging
import textwrap
from contextlib import contextmanager
from ctypes import c_int
from dataclasses import dataclass

import rich

import egse.dsi.constants as constants
import egse.rmap
import egse.spw
from egse.dsi.esl import esl_get_product_string
from egse.settings import Settings

rich.print("Loading egse.dsi.rmap package...", flush=True)

LOGGER = logging.getLogger(__name__)

dsi_settings = Settings.load("DSI")

# Maintain a transmit and a receive buffer

rxbuf = ctypes.create_string_buffer(dsi_settings.RX_BUFFER_LENGTH)
txbuf = ctypes.create_string_buffer(dsi_settings.TX_BUFFER_LENGTH)

# Initialize the status variable which is a c pointer that is set by the library routines to
# pass a status.

# status = c_int(0)
# status_p = ctypes.pointer(status)


@dataclass
class ESL_RMAP:
    spw_device = None
    target_key = 0
    target_logical_address = 0xFE
    target_spw_address = 0x00
    target_spw_address_len = 0
    reply_spw_address = 0x00
    reply_spw_address_len = 0
    initiator_logical_address = 0xFE
    transaction_identifier = 99
    ESL_RMAP_error = 0

    def __str__(self):
        return textwrap.dedent(
            f"""\
            spw_device={self.spw_device}
            target_key={self.target_key}
            target_logical_address={self.target_logical_address}
            target_spw_address={self.target_spw_address}
            target_spw_address_len={self.target_spw_address_len}
            reply_spw_address={self.reply_spw_address}
            reply_spw_address_len={self.reply_spw_address_len}
            initiator_logical_address={self.initiator_logical_address}
            transaction_identifier={self.transaction_identifier}
            ESL_RMAP_error={self.ESL_RMAP_error}
            """
        )


@contextmanager
def rmap_connection(esl_link):
    """
    Context manager that opens an RMAP connection on the EtherSpaceLink ESL.

    Args:
        esl_link (ESL): the ESL structure that defines the connection to the DSI

    Returns:
        an RMAP link connection.
    """
    rmap_link = rmap_open_connection(esl_link)
    yield rmap_link

    rmap_close_connection(rmap_link)


def rmap_initialise(esl_link) -> ESL_RMAP:
    """
    Initialise the RMAP structure with predefined settings for PLATO.
    """
    esl_rmap: ESL_RMAP = ESL_RMAP()

    esl_rmap.spw_device = esl_link
    esl_rmap.target_key = 0x00
    esl_rmap.target_logical_address = 0xFE
    esl_rmap.target_spw_address = 0x00
    esl_rmap.target_spw_address_len = 0
    esl_rmap.reply_spw_address = 0x0
    esl_rmap.reply_spw_address_len = 0
    esl_rmap.initiator_logical_address = 0xFE
    esl_rmap.transaction_identifier = 99
    esl_rmap.ESL_RMAP_error = 99

    return esl_rmap


def rmap_open_connection(esl_link):
    """
    Initialises and opens an RMAP connection on an EtherSpaceLink (ESL) connection.

    This requires a valid link to an ESL connection which shall be created with the following
    command:

        esl_link = esl_open_connection(<DSI IP Address>)

    Args:
        esl_link: a connection link to the DSI SpaceWire interface

    Returns:
        The RMAP connection link.

    """

    LOGGER.info(f"Open and setup RMAP connection to {esl_get_product_string(esl_link)}")

    rmap_link = rmap_initialise(esl_link)

    LOGGER.info("RMAP connection opened successfully.")

    return rmap_link


def rmap_close_connection(rmap_link):
    LOGGER.info("RMAP connection closed successfully.")


def rmap_configure(rmap_link: ESL_RMAP, initiator_logical_address,
                   target_key=constants.RMAP_TARGET_KEY,
                   target_logical_address=constants.RMAP_TARGET_LOGICAL_ADDRESS_DEFAULT):
    """
    Configure the RMAP EtherSpaceWire link.

    Args:
        rmap_link: the RMAP link connection
        initiator_logical_address: logical address of the SpaceWire node that starts the transaction
        target_key: the key field used for command authorisation
        target_logical_address: logical address of the target node (default: 0xFE)

    Returns:
        Nothing

    """
    rmap_link.initiator_logical_address = initiator_logical_address
    rmap_link.target_key = target_key
    rmap_link.target_logical_address = target_logical_address
    rmap_link.target_spw_address = 0x0
    rmap_link.target_spw_address_len = 0


# This function is not used anywhere, but I don't want to delete it yet because it was originally converted from
# the C code provided by 4Links and contains the logic that shall be used to process RMAP packets.
# I leave it here for future use or inspection.

def process_rmap_commands(rmap_link: ESL_RMAP):
    # Leave these imports here because they are only used by this function

    from egse.bits import crc_calc
    from egse.dsi import constants
    from egse.dsi.esl import ESLError
    from egse.dsi.esl import esl_flush
    from egse.dsi.esl import esl_get_esl_error
    from egse.dsi.esl import esl_read_packet
    from egse.dsi.esl import esl_write_packet
    from egse.dsi.esl import get_extension_name
    from egse.dsi.esl import get_terminator_name
    from egse.dsi.esl import is_extension_code
    from egse.dsi.esl import is_terminator_code
    from egse.dsi.spw import handle_extension_packet
    from egse.dsi.spw import handle_special_packet
    from egse.rmap import create_rmap_read_request_reply_packet
    from egse.spw import CheckError
    from egse.spw import check_data_crc
    from egse.spw import check_header_crc
    from egse.spw import check_initiator_logical_address
    from egse.spw import check_instruction
    from egse.spw import check_key
    from egse.spw import check_protocol_id
    from egse.spw import check_target_logical_address
    from egse.spw import get_address
    from egse.spw import get_data_length
    from egse.spw import get_instruction_field
    from egse.spw import get_transaction_identifier
    from egse.spw import is_command
    from egse.spw import is_increment
    from egse.spw import is_write

    total_received = 0
    packet = bytes()

    esl_link = rmap_link.spw_device

    terminator, rx_buffer = esl_read_packet(esl_link)
    bytes_received = len(rx_buffer)

    if is_terminator_code(terminator):
        LOGGER.debug(
            f"bytes received={bytes_received}, terminator={terminator} "
            f"[{get_terminator_name(terminator)}]"
        )
    elif is_extension_code(terminator):
        LOGGER.debug(
            f"bytes received={bytes_received}, terminator={terminator} "
            f"[{get_extension_name(terminator)}]"
        )
    else:
        LOGGER.debug(f"bytes received={bytes_received}, terminator={terminator}")

    # TODO:
    #   When the link is closed from the other end (dpusim) just one byte (b'\x08') is received.
    #   So, we should try to restart the link...

    if bytes_received == 1:
        LOGGER.warning("Link was closed from the initiator side, terminating.")
        return

    # First check if we encountered any errors or shutdown,
    # if True then break the main while loop and end the connection
    #
    # FIXME:
    #   We need better handling of exceptional conditions here since the FEE Simulator can never
    #   die.
    #       - what shall we do when a shutdown is received?
    #       - what shall we do when a timeout has occured?
    #       - what shall we do with a buffer overflow? When can this happen?
    #       - some errors are related to the virtual DSI, how do we solve those?

    if bytes_received < 0:
        error = esl_get_esl_error(esl_link)
        if error == constants.ESL_ERROR_TIMEOUT:
            LOGGER.debug("Received a timeout, continuing...")
            return
        # FIXME: We should handle all these cases in a simpler way
        if error == constants.ESL_ERROR_RECEIVER_SHUTDOWN:
            LOGGER.info("Shutdown detected.")
            return
        if error == constants.ESL_ERROR_BUFFER_OVERFLOW:
            # FIXME: Can we recover from this situation?
            LOGGER.error("Insufficient buffer to read full packet, bailing out.")
            return
        if error == constants.ESL_ERROR_RECFILE_WRITE:
            LOGGER.error("Write error on record file, bailing out.")
            return

        LOGGER.error(
            f"read_packet: returned error, "
            f"ESL error = {constants.esl_error_codes[error]} [{error}]"
        )
        return

    # When we receive an unknown terminator we just ignore, log the error and continue...

    if terminator not in (
        constants.ESL_EXTN,
        constants.ESL_SPECIAL,
        constants.ESL_PART_EOP_EEP,
        constants.ESL_PART_EXTN,
        constants.ESL_PART_SPECIAL,
        constants.ESL_EEP,
        constants.ESL_EOP,
    ):
        LOGGER.error(f"Unknown terminator [{terminator}] received.")
        return

    if terminator == constants.ESL_EXTN:
        handle_extension_packet(rx_buffer, bytes_received)

    if terminator == constants.ESL_SPECIAL:
        handle_special_packet(rx_buffer, bytes_received)

    if terminator in (
        constants.ESL_PART_EOP_EEP,
        constants.ESL_PART_EXTN,
        constants.ESL_PART_SPECIAL,
    ):
        LOGGER.debug("Partial Data Packet received.")

        total_received += bytes_received
        packet += rx_buffer[:bytes_received]

        # FIXME:
        #   at this point we need to go for the next part of the packet
        #   continue was used in the while loop before splitting off this code. We now do a
        #   return, but we loose information on the total packet size etc.
        return

    if terminator == constants.ESL_EEP:
        LOGGER.debug("Error End of Packet returned by DSI")

    if terminator == constants.ESL_EOP:
        LOGGER.debug("Normal End of Packet returned by DSI")

        total_received += bytes_received
        packet += rx_buffer[:bytes_received]

        LOGGER.debug(f"total_received={total_received}")
        LOGGER.debug(f"{packet}")

        # Deal with RMAP request packet
        # FIXME: shouldn't this all be checked on packet instead of rx_buffer?

        try:
            # Run a number of checks on the received packet

            check_target_logical_address(rx_buffer, dsi_settings.TARGET_LOGICAL_ADDRESS)
            check_protocol_id(rx_buffer)
            check_instruction(rx_buffer)
            check_key(rx_buffer, rmap_link.target_key)
            check_initiator_logical_address(rx_buffer, dsi_settings.INITIATOR_LOGICAL_ADDRESS)
            check_header_crc(rx_buffer)

            # Extract information from the packet that we need further on

            tid = get_transaction_identifier(rx_buffer)
            address = get_address(rx_buffer)
            data_length = get_data_length(rx_buffer)
        except CheckError as ce:
            LOGGER.error(f"{ce.message}, status = {ce.status}")
            status = ce.status
            # FIXME:
            #   Something is wrong with the packet here, do proper exception handling.
            #   We are not anymore in the while loop after we have split off this code,
            #   so continue doesn't work anymore...
            # continue
            raise ce

        # Do something with the packet received

        instruction_field = get_instruction_field(packet)

        if is_command(instruction_field):

            status = constants.RMAP_SUCCESS

            if (
                not dsi_settings.RMAP_BASE_ADDRESS
                <= address
                < (dsi_settings.RMAP_BASE_ADDRESS + dsi_settings.RMAP_MEMORY_SIZE)
            ):
                LOGGER.error(f"ERROR: Access outside of RMAP memory area, address=0x{address:010X}")
                status = constants.RMAP_GENERAL_ERROR

            # Handling an RMAP Write Command
            #
            # - Send a reply
            # - Check Data CRC before writing
            # - Write the data into memory

            if is_write(instruction_field):

                LOGGER.debug("RMAP write command received, sending reply packet...")

                # FIXME: need some work here!!!!

                # Create the target memory map and fill it with a pattern.
                # This is just to simplify checking the correct write command.
                # TODO: this should be replaced with the RegistryMap

                rmap_target_memory = ctypes.create_string_buffer(
                    bytes([x & 0xFF for x in range(dsi_settings.RMAP_MEMORY_SIZE)])
                )

                tx_buffer = ctypes.create_string_buffer(dsi_settings.TX_BUFFER_LENGTH)

                tx_buffer[7] = crc_calc(tx_buffer, 0, 7)

                result = esl_write_packet(esl_link, tx_buffer, 8, constants.ESL_EOP)

                esl_flush(esl_link)

                # When no errors, then write the data into memory at the given position

                if status == constants.RMAP_SUCCESS:

                    # Check the Data CRC

                    try:
                        check_data_crc(rx_buffer)
                    except CheckError as ce:
                        LOGGER.error(f"{ce}, status = {ce.status}")
                        raise ce

                    # Write the data into the target memory map

                    # FIXME: I do not understand why this is !!!!

                    if is_increment(instruction_field):
                        # change this code to work with RegisterMap
                        # rmap_target_memory[address:address + data_length] = get_data(rx_buffer)
                        pass
                    else:
                        # change this code to work with RegisterMap
                        # Overwrite all the data into the same memory address, why?
                        # for b in get_data(rx_buffer):
                        #    rmap_target_memory[address] = b
                        pass

            # Handling an RMAP Read Command

            else:
                if status:
                    data_length = 0

                LOGGER.warning(
                    "Commented out this code, work needs to be done on RMAP read command"
                )
                # data = self.register_map.get_data(address, data_length)
                data = b"\x00\x01\x02\x03"

                tx_buffer = create_rmap_read_request_reply_packet(instruction_field, tid, status, data, data_length)

                result = esl_write_packet(esl_link, tx_buffer, len(tx_buffer), constants.ESL_EOP)

                result = esl_flush(
                    esl_link
                )  # FIXME: This will mask previous ESL_error if there was one

                if result:
                    raise ESLError(
                        f"Could not write the packet, "
                        f"ESL error code = {constants.esl_error_codes[esl_link.contents.ESL_error]} "
                        f"[{esl_link.contents.ESL_error}]"
                    )

        else:
            LOGGER.warning("The packet is not an RMAP read/write command.")

        total_received = 0
        packet = bytes()

    LOGGER.debug("Going for the next SpaceWire packet...")
