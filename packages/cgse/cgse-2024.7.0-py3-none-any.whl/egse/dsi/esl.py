"""
This module provides Python wrapper functions to (most of) the library functions from
the C library `EtherSpaceLink.c`.

Basic Usage

For accessing the EtherSpaceLink interface, use the context manager to get an ESL connection:

    with esl_connection(dsi_address) as esl_link:
        # do your configuration and commanding here

For special cases it might be useful to open and close the ESL connection yourself. Be careful
however to close the connection with every exception that is thrown.

        try:
            esl_link = esl_open_connection(dsi_address)
            # do your configuration and commanding
        finally:
            if esl_link:
                esl_close_connection(esl_link)

It should be clear that using the context manager is preferred and should be considered the normal usage.

We use one single Exception (`ESLError`) specific for these wrapper functions.
An `ESLError` is thrown whenever the C function returns an error from which we can not recover.
This allows to cascade the python functions in a `try: except:` clause making
the code much more readable.

Developer Info

The C interface depends heavily on a C structure which we had to re-define using
the Structure class provided by ctypes.

"""
import ctypes
import logging
import time
import typing
from contextlib import contextmanager
from ctypes import c_char_p
from ctypes import c_int
from typing import Tuple

import egse
from egse.dsi import constants
from egse.dsi.constants import esl_error_codes
from egse.dsi.constants import esl_extension_codes
from egse.dsi.constants import esl_link_mode
from egse.dsi.constants import esl_terminator_codes
from egse.settings import Settings

if typing.TYPE_CHECKING:
    from egse.dsi._libesl import ESL

logger = logging.getLogger(__name__)

dsi_settings = Settings.load("DSI")

# Create and initialize a memory buffer for transmissions

rx_buffer = ctypes.create_string_buffer(dsi_settings.RX_BUFFER_LENGTH)
tx_buffer = ctypes.create_string_buffer(dsi_settings.TX_BUFFER_LENGTH)


class ESLError(Exception):
    pass


def esl_read_packet(esl_link: 'ESL', timeout: int = None) -> Tuple[int, bytes]:
    """
    Reads a full packet from the SpaceWire link.

    .. note:: since this function returns a packet as a bytes object, the content of the packet can not be changed.

    Args:
        esl_link (ESL): the ESL structure that defines the connection to the DSI
        timeout (int): the maximum timeout that read_packet() will wait for data before returning [milliseconds]

    Returns:
        A tuple with the terminator value and a bytes object containing the packet.
        When an error occurred, the first value in the tuple will be negative and contains the error number,
        the second item in the tuple will then be an empty buffer.

    """
    terminator = c_int(0)
    terminator_p = ctypes.pointer(terminator)

    bytes_received = esl_read_packet_full(
        esl_link, rx_buffer, dsi_settings.RX_BUFFER_LENGTH, terminator_p,
        constants.ESL_RETURN_EXTENSION_DATA | constants.ESL_RETURN_SPECIAL_DATA, timeout=timeout)

    # logger.debug(f"Number of bytes received: {bytes_received}")

    if bytes_received < 0:
        return bytes_received, bytes()

    return terminator.value, rx_buffer[:bytes_received]


@contextmanager
def esl_connection(dsi_address: str) -> 'ESL':
    """
    Context Manager that opens a EtherSpaceLink connection with the DSI (Diagnostic SpaceWire Interface).

    Args:
        dsi_address (str): the IP address of the DSI

    Returns:
        a pointer to the ESL structure
    """
    esl_link = None
    try:
        esl_link = esl_open_connection(dsi_address)
        yield esl_link
    finally:
        if esl_link:
            esl_close_connection(esl_link)


def esl_open_connection(dsi_address: str) -> 'ESL':
    """
    Open a connection to the EtherSpaceLink DSI on the given IP address.
    This function will keep trying to connect for 10 seconds before aborting
    and throwing an `ESLError`.

    Args:
        dsi_address (str): the IP address of the DSI

    Returns:
        a pointer to the ESL structure

    """
    logger.info(f"Open and setup EtherSpaceLink connection on {dsi_address}.")

    retry = 20  # number of retries before failing to open connection
    esl_link = None

    while retry:
        esl_link = egse.dsi._libesl.libesl_open(c_char_p(dsi_address.encode()))
        if esl_link:
            break
        else:
            time.sleep(0.5)  # wait half a second before trying again
            logger.info(f"Trying to connect to {dsi_address}, {retry / 2.0} sec before shutdown.")
            retry -= 1

    if not esl_link:
        raise ESLError(f"Couldn't open connection to DSI on {dsi_address}.")

    logger.info(f"EtherSpaceLink connection to {dsi_address} opened successfully.")

    return esl_link


def esl_close_connection(esl_link):
    """
    Close the connection to the EtherSpaceLink DSI.

    This also flushes and closes the log and record files if they were used.

    Args:
        esl_link (ESL): the ESL structure that defines the connection to the DSI

    Returns:
        Nothing
    """
    egse.dsi._libesl.libesl_close(esl_link)
    logger.info("EtherSpaceLink connection closed successfully.")


def esl_flush(esl_link) -> int:
    """
    Flush all outstanding data to the destination. This function puts queued data onto the wire.

    Args:
        esl_link (ESL): the ESL structure that defines the connection to the DSI

    Returns:
        0 on success, !0 otherwise
    """
    result = egse.dsi._libesl.libesl_flush(esl_link)
    # We don't want this to raise an exception, the result value should be checked by the caller instead.
    # if result:
    #     raise ESLError(
    #         f"Could not flush/send transmit buffer, "
    #         f"ESL error code={esl_error_codes[esl_link.contents.ESL_error]} [{esl_link.contents.ESL_error}]"
    #     )
    return result


def esl_configure(esl_link: 'ESL',
                  active_link: int = 1, speed: int = 50, mode: int = constants.ESL_LINK_MODE_NORMAL,
                  report: int = 0):
    """
    Configure the `esl_link` EtherSpaceWire link to the DSI.

    The reporting parameter is used to enable reporting for the following events:

        ESL_ER_REPORT_PARITY_ERROR
        ESL_ER_REPORT_TIME_CODE
        ESL_ER_REPORT_ESC_EOP
        ESL_ER_REPORT_ESC_EEP
        ESL_ER_REPORT_ESC_ESC
        ESL_ER_REPORT_TIMEOUT

    Args:
        esl_link (ESL): the ESL structure that defines the connection to the DSI
        active_link: the port number on the DSI where the SpW link shall be activated (default=1)
        speed: the speed in Mbps
        mode: the link mode [DISABLED, NORMAL, LEGACY or MASTER]
        report: enable reporting [default=0]

    Returns:
        Nothing
    """
    status = esl_set_active_link(esl_link, active_link)
    logger.info(f"esl_set_active_link({active_link}) -> {status = }")
    status = esl_set_speed(esl_link, speed)
    logger.info(f"esl_set_speed({speed}) -> {status = }")

    if report:
        status = esl_er_enable_reporting(esl_link, report)
        logger.info(f"esl_er_enable_reporting(0b{report:b}) -> {status = }")

    status = esl_set_mode(esl_link, mode)
    logger.info(f"esl_set_mode({esl_link_mode[mode]}={mode}) -> {status = }")

    status = esl_flush(esl_link)
    logger.info(f"esl_flush() -> {status = }")


def esl_set_active_link(esl_link, active_link):
    return egse.dsi._libesl.libesl_set_active_link(esl_link, active_link)


def esl_get_active_link(esl_link):
    return esl_link.contents.current_port


def esl_is_link_connected(esl_link):
    return egse.dsi._libesl.libesl_link_connected(esl_link)


def esl_set_speed(esl_link, speed):
    result = egse.dsi._libesl.libesl_set_speed(esl_link, speed)
    if result:
        raise ESLError("Could not set speed to {}, ESL error code={} [{}]".format(speed, esl_error_codes[
            esl_link.contents.ESL_error], esl_link.contents.ESL_error))
    return result


def esl_set_mode(esl_link: 'ESL', mode: int) -> int:
    """
    Set the operating mode of the currently active SpaceWire link.

    After opening a connection, the link is disabled; it must then
    be enabled into one of its operational modes before data can
    be transferred.

    Args:
        esl_link (ESL): the ESL structure that defines the connection to the DSI
        mode (int): the link mode [DISABLED, NORMAL, LEGACY or MASTER]

    Returns:
        0 if the request has been queued, not 0 if not.

    """
    result = egse.dsi._libesl.libesl_set_mode(esl_link, mode)
    if result:
        raise ESLError(f"Could not set mode {esl_link_mode[mode]}.")

    return result


def esl_send_timecode(esl_link: 'ESL', timecode: int) -> int:
    """
    Send a timecode over the SpaceWire link.

    The 8-bit timecode argument contains six-bit of system time (time-field) and two control flags.

    Args:
        esl_link (ESL): the ESL structure that defines the connection to the DSI
        timecode (int): an 8-bit timecode field

    Returns:
        0 if the request has been queued, not 0 if not.

    """
    result = egse.dsi._libesl.libesl_send_timecode(esl_link, timecode)

    if result:
        raise ESLError(
            f"Could not send timecode, ESL error code={esl_error_codes[esl_link.contents.ESL_error]} "
            f"[{esl_link.contents.ESL_error}]"
        )

    result = egse.dsi._libesl.libesl_flush(esl_link)

    return result


def esl_get_rx_timeout(esl_link):
    return esl_link.contents.rx_timeout


def esl_set_rx_timeout(esl_link, timeout: int):
    esl_link.contents.rx_timeout = timeout


def esl_get_receive_speed(esl_link: 'ESL') -> int:
    """
    Gets the receive speed of the currently active link.

    Note that this function has the ability to cause frames to be dropped and the esl_request_rx_speed() function
    should be used instead.

    Args:
        esl_link (ESL): the ESL structure that defines the connection to the DSI

    Returns:
        the speed of the active link in Mbits/s. In case of an error a value < 0 will be returned.
    """
    return egse.dsi._libesl.libesl_get_receive_speed(esl_link)


def esl_set_log_file(esl_link, filename):
    result = egse.dsi._libesl.libesl_set_log_file(esl_link, c_char_p(filename.encode()))
    if result:
        raise ESLError(f"Could not write to or open log file {filename}.")
    return result


def esl_set_record_file(esl_link, filename):
    result = egse.dsi._libesl.libesl_set_record_file(esl_link, c_char_p(filename.encode()))
    if result:
        raise ESLError(f"Could not write to or open record file {filename}.")
    return result


def esl_get_manufacturer_string(esl_link):
    return egse.dsi._libesl.libesl_get_manufacturer_string(esl_link).decode()


def esl_get_product_string(esl_link):
    return egse.dsi._libesl.libesl_get_product_string(esl_link).decode()


def esl_get_esl_error(esl_link):
    return egse.dsi._libesl.libesl_get_esl_error(esl_link)


def esl_get_hwa(esl_link):
    hwa = b'012345'  # Pre-allocate the character buffer
    egse.dsi._libesl.libesl_get_hwa(esl_link, hwa)
    return hwa


def esl_get_serial_number(esl_link):
    hwa = esl_get_hwa(esl_link)
    return egse.dsi._libesl.libesl_hwa_to_serial_number_string(hwa)


def esl_get_number_of_links(esl_link):
    return egse.dsi._libesl.libesl_get_number_of_links(esl_link)


def esl_read_packet_full(esl_link, buffer, buffer_length, rx_terminator, special_data_action, timeout: int = None):

    if timeout:
        saved_timeout = esl_get_rx_timeout(esl_link)
        egse.dsi._libesl.libesl_set_rx_timeout(esl_link, timeout)

    result = egse.dsi._libesl.libesl_read_packet_full(esl_link, buffer, buffer_length, rx_terminator, special_data_action)

    if timeout:
        egse.dsi._libesl.libesl_set_rx_timeout(esl_link, saved_timeout)

    # This error handling is (or should be) done in the calling application, see for example egse.feesim.py
    # if result == -1:
    #     raise ESLError(
    #         f"Could not read full packet, "
    #         f"ESL error code = {esl_error_codes[esl_link.contents.ESL_error]} [{esl_link.contents.ESL_error}]"
    #     )

    return result


def esl_write_packet(esl_link: 'ESL', buffer, buffer_length: int, tx_terminator: int) -> int:
    """
    Queue data for transmission over the SpaceWire cable. If there is no room left in the buffer,
    the buffer is transmitted.

    Note, that even when the queued data is transmitted, the data added to it may not be.
    To guarantee transmission of this data you need to call the esl_flush() function.

    Args:
        esl_link (ESL): the ESL structure that defines the connection to the DSI
        buffer: the data to send
        buffer_length: the size of the buffer to send (the actual buffer size might be longer)
        tx_terminator: additional metadata about the frame we are transmitting (EOP, EEP, PART_EOP_EEP, EXTN)

    Returns:
        return_code: 0 on success, < 0 when an error occurred.
    """

    result = egse.dsi._libesl.libesl_write_packet(esl_link, buffer, buffer_length, tx_terminator)

    return result


def esl_er_enable_reporting(esl_link, flags):
    result = egse.dsi._libesl.libesl_er_enable_reporting(esl_link, flags)
    if result:
        raise ESLError(
            f"Could not enable error reporting, "
            f"ESL error code = {esl_error_codes[esl_link.contents.ESL_error]} [{esl_link.contents.ESL_error}]"
        )
    return result


def esl_print_info(esl_link: 'ESL') -> None:
    """
    Prints information about the connected device to the console.

    Args:
        esl_link (ESL): the ESL structure that defines the connection to the DSI

    Returns:
        nothing
    """
    print(f"Manufacturer        {esl_get_manufacturer_string(esl_link)}")
    print(f"Product             {esl_get_product_string(esl_link)}")
    print(f"Number of links     {esl_get_number_of_links(esl_link)} [active port={esl_get_active_link(esl_link)}]")

    hwa = esl_get_hwa(esl_link)
    serial_number = esl_get_serial_number(esl_link)

    print(f"Serial number       {serial_number}")
    print(f"Hardware Address    0x{hwa[0]:02X}-{hwa[1]:02X}-{hwa[2]:02X}-{hwa[3]:02X}-{hwa[4]:02X}-{hwa[5]:02X}")


def esl_print_summary_of_structure(esl):
    print("EtherSpaceLink structure:")
    print("sock                {}".format(esl.contents.sock))
    print("tx_buffer_length    {}".format(esl.contents.tx_buffer_length))
    print("tx_buffer_content   {}".format(esl.contents.tx_buffer_content))
    print("rx_buffer_length    {}".format(esl.contents.rx_buffer_length))
    print("rx_buffer_content   {}".format(esl.contents.rx_buffer_content))
    print("rx_state            {}".format(esl.contents.rx_state))
    print("rx_count            {}".format(esl.contents.rx_count))
    print("rx_param            {}".format(esl.contents.rx_param))
    #print("rx_size             {}".format(esl.contents.rx_size))
    print("rx_timeout          {}".format(esl.contents.rx_timeout))
    #print("rx_final_terminator {}".format(esl.contents.rx_final_terminator))
    print("extn_count          {}".format(esl.contents.extn_count))
    print("number_of_slots     {}".format(esl.contents.number_of_slots))
    #print("id                  {}".format(esl.contents.id))


# Helper Functions ---------------------------------------------------------------------------------


def is_terminator_code(code):
    return True if code in esl_terminator_codes else False


def get_terminator_name(code):
    if code in esl_terminator_codes:
        return esl_terminator_codes[code]
    else:
        return None


def is_extension_code(code):
    return True if code in esl_extension_codes else False


def get_extension_name(code):
    if code in esl_extension_codes:
        return esl_extension_codes[code]
    else:
        return None


def get_protocol_id(packet) -> int:
    if isinstance(packet[1], bytes):
        value = int.from_bytes(packet[1], byteorder='big')
    else:
        value = packet[1]  # value assumed to be of type 'int'
    return value


def is_timecode(packet) -> bool:
    """Returns True if the packet is a timecode reported as an extension from the DSI."""
    return packet[0] == 0x91


RMAP_PROTOCOL_ID = 0x01
CCSDS_PROTOCOL_ID = 0x02
DATA_HK_PROTOCOL_ID = 0xF0


def pretty_print_read_request_packet(packet):
    msg = (
        f"RMAP Read Request  ({len(packet)} bytes)\n"
        f"Logical address:   0x{packet[0]:0x}\n"
        f"Protocol ID:       0x{packet[1]:0x}\n"
        f"Instruction:       0x{packet[2]:0x}\n"
        f"Key:               0x{packet[3]:0x}\n"
        f"Initiator address: 0x{packet[4]:0x}\n"
        f"Transaction ID:    0x{packet[5:7].hex()}\n"
        f"Extended address:  0x{packet[7]:0x}\n"
        f"Address Field:     0x{packet[8:12].hex()}\n"
        f"Data Length:       0x{packet[12:15].hex()}\n"
        f"Header CRC:        0x{packet[15]:0x}\n"
    )
    return msg


def pretty_print_read_request_reply_packet(packet):
    data_length = int.from_bytes(packet[8:11], byteorder='big')
    msg = (
        f"RMAP Read Request Reply ({len(packet)} bytes)\n"
        f"Logical address:   0x{packet[0]:0x}\n"
        f"Protocol ID:       0x{packet[1]:0x}\n"
        f"Instruction:       0x{packet[2]:0x}\n"
        f"Status:            0x{packet[3]:0x}\n"
        f"Target address:    0x{packet[4]:0x}\n"
        f"Transaction ID:    0x{packet[5:7].hex()}\n"
        f"Reserved:          0x{packet[7]:0x}\n"
        f"Data Length:       {data_length}\n"
        f"Header CRC:        0x{packet[11]:0x}\n"
        f"data:              0x{packet[12:12 + min(32, data_length)].hex()}\n"
        f"                   note: maximum 32 bytes will be printed for the data.\n"
        f"Data CRC:          0x{packet[-1]:0x}\n"
    )
    return msg


def pretty_print_write_request_reply_packet(packet):
    data_length = int.from_bytes(packet[8:11], byteorder='big')
    msg = (
        f"RMAP Write Request Reply ({len(packet)} bytes)\n"
        f"Logical address:   0x{packet[0]:0x}\n"
        f"Protocol ID:       0x{packet[1]:0x}\n"
        f"Instruction:       0x{packet[2]:0x}\n"
        f"Status:            0x{packet[3]:0x}\n"
        f"Target address:    0x{packet[4]:0x}\n"
        f"Transaction ID:    0x{packet[5:7].hex()}\n"
        f"Header CRC:        0x{packet[7]:0x}\n"
    )
    return msg


def pretty_print_verified_write_request_packet(packet):
    msg = (
        f"RMAP Verified Write Request ({len(packet)} bytes)\n"
        f"Logical address:   0x{packet[0]:02x}\n"
        f"Protocol ID:       0x{packet[1]:02x}\n"
        f"Instruction:       0x{packet[2]:02x}\n"
        f"Key:               0x{packet[3]:02x}\n"
        f"Initiator address: 0x{packet[4]:02x}\n"
        f"Transaction ID:    0x{packet[5:7].hex()}\n"
        f"Address:           0x{packet[7:12].hex()}\n"
        f"Data Length:       0x04\n"
        f"Header CRC:        0x{packet[15]:02x}\n"
        f"data:              0x{packet[16:20].hex()}\n"
        f"Data CRC:          0x{packet[20]:02x}\n"
    )
    return msg


def pretty_print_unverified_write_request_packet(packet):
    data_length = int.from_bytes(packet[12:15], byteorder='big')
    msg = (
        f"RMAP Unverified Write Request ({len(packet)} bytes)\n"
        f"Logical address:   0x{packet[0]:02x}\n"
        f"Protocol ID:       0x{packet[1]:02x}\n"
        f"Instruction:       0x{packet[2]:02x}\n"
        f"Key:               0x{packet[3]:02x}\n"
        f"Initiator address: 0x{packet[4]:02x}\n"
        f"Transaction ID:    0x{packet[5:7].hex()}\n"
        f"Address:           0x{packet[7:12].hex()}\n"
        f"Data Length:       {data_length}\n"
        f"Header CRC:        0x{packet[15]:02x}\n"
        f"data:              {packet[16:16 + min(32, data_length)]}\n"
        f"                   note: maximum 32 bytes will be printed for the data.\n"
        f"Data CRC:          0x{packet[-1]:0x}\n"
    )
    return msg


def pp_packet(packet) -> str:
    """
    Returns a one-line representation of a SpW packet.

    Args:
        packet (bytes): the raw packet

    Returns:
        a one-line representation of a SpW packet
    """
    RMAP_PROTOCOL_ID = 0x01
    CCSDS_PROTOCOL_ID = 0x02

    if hasattr(packet, 'raw'):
        packet = packet.raw

    if get_protocol_id(packet) == RMAP_PROTOCOL_ID:
        msg = (
            f"RMAP: "
            f"0x{packet[0]:0x}:"
            f"0x{packet[1]:0x}:"
            f"0x{packet[2]:0x}:"
            f"0x{packet[3]:0x}:"
            f"0x{packet[4]:0x}:"
            f"0x{packet[5:7].hex()}:"
            f"0x{packet[7]:0x}:"
            f"0x{packet[8:12].hex()}:"
            f"0x{packet[12:15].hex()}:"
            f"0x{packet[15]:0x}"
        )
    elif get_protocol_id(packet) == CCSDS_PROTOCOL_ID:
        msg = (
            "CCSDS Packet"
        )
    else:
        msg = "Extended Protocol Identifier is not supported"

    return msg
