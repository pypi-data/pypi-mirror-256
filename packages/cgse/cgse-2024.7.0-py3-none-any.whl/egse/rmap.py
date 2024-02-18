import logging

from egse.bits import crc_calc
from egse.decorators import static_vars
from egse.exceptions import Error

# RMAP Error Codes and Constants -------------------------------------------------------------------

RMAP_PROTOCOL_ID = 0x01
RMAP_TARGET_LOGICAL_ADDRESS_DEFAULT = 0xFE
RMAP_TARGET_KEY = 0xD1

# Error and Status Codes

RMAP_SUCCESS = 0
RMAP_GENERAL_ERROR = 1
RMAP_UNUSED_PACKET_TYPE_COMMAND_CODE = 2
RMAP_INVALID_KEY = 3
RMAP_INVALID_DATA_CRC = 4
RMAP_EARLY_EOP = 5
RMAP_TOO_MUCH_DATA = 6
RMAP_EEP = 7
RMAP_RESERVED = 8
RMAP_VERIFY_BUFFER_OVERRUN = 9
RMAP_NOT_IMPLEMENTED_AUTHORISED = 10
RMAP_RMW_DATA_LENGTH_ERROR = 11
RMAP_INVALID_TARGET_LOGICAL_ADDRESS = 12

# Memory Map layout --------------------------------------------------------------------------------

# NOTE: These memory areas are currently equal for N-FEE and F-FEE. Don't know if this will
#       change in the future.

CRITICAL_AREA_START = 0x0000_0000
CRITICAL_AREA_END = 0x0000_00FC
GENERAL_AREA_START = 0x0000_0100
GENERAL_AREA_END = 0x0000_06FC
HK_AREA_START = 0x0000_0700
HK_AREA_END = 0x0000_07FC
WINDOWING_AREA_START = 0x0080_0000
WINDOWING_AREA_END = 0x00FF_FFFC


class RMAPError(Error):
    """An RMAP specific Error."""
    pass


_LOGGER = logging.getLogger(__name__)


def create_rmap_read_request_packet(address: int, length: int, tid: int, strict: bool = True) -> bytes:
    """
    Creates an RMAP Read Request SpaceWire packet.

    The read request is an RMAP command that read a number of bytes from the FEE register memory.

    The function returns a ``ctypes`` character array (which is basically a bytes array) that
    can be passed into the EtherSpaceLink library function ``esl_write_packet()``.

    Address shall be within the 0x0000_0000 and 0x00FF_FFFC. The memory map (register) is divided
    in the following areas:

        0x0000_0000 - 0x0000_00FC   Critical Configuration Area (verified write)
        0x0000_0100 - 0x0000_06FC   General Configuration Area (unverified write)
        0x0000_0700 - 0x0000_07FC   Housekeeping area
        0x0000_0800 - 0x007F_FFFC   Not Supported
        0x0080_0000 - 0x00FF_FFFC   Windowing Area (unverified write)
        0x0010_0000 - 0xFFFF_FFFC   Not Supported

    All read requests to the critical area shall have a fixed data length of 4 bytes.
    All read requests to a general area shall have a maximum data length of 256 bytes.
    All read requests to the housekeeping area shall have a maximum data length of 256 bytes.
    All read requests to the windowing area shall have a maximum data length of 4096 bytes.

    The transaction identifier shall be incremented for each read request. This shall be done by
    the calling function!

    Args:
        address (int): the FEE register memory address
        length (int): the data length
        tid (int): transaction identifier
        strict (bool): perform strict checking of address and length

    Returns:
        a bytes object containing the full RMAP Read Request packet.
    """
    from egse.spw import update_transaction_identifier

    check_address_and_data_length(address, length, strict=strict)

    tid = update_transaction_identifier(tid)

    buf = bytearray(16)

    # NOTE: The first bytes would each carry the target SpW address or a destination port,
    #       but this is not used for point-to-point connections, so we're safe.

    buf[0] = 0x51  # Target N-FEE or F-FEE
    buf[1] = 0x01  # RMAP Protocol ID
    buf[2] = 0x4C  # Instruction: 0b1001100, RMAP Request, Read, Incrementing address, reply address
    buf[3] = 0xD1  # Destination Key
    buf[4] = 0x50  # Initiator is always the DPU
    buf[5] = (tid >> 8) & 0xFF  # MSB of the Transition ID
    buf[6] = tid & 0xFF  # LSB of the Transition ID
    buf[7] = 0x00  # Extended address is not used
    buf[8] = (address >> 24) & 0xFF  # address (MSB)
    buf[9] = (address >> 16) & 0xFF  # address
    buf[10] = (address >> 8) & 0xFF  # address
    buf[11] = address & 0xFF  # address (LSB)
    buf[12] = (length >> 16) & 0xFF  # data length (MSB)
    buf[13] = (length >> 8) & 0xFF  # data length
    buf[14] = length & 0xFF  # data length (LSB)
    buf[15] = rmap_crc_check(buf, 0, 15) & 0xFF

    return bytes(buf)


def create_rmap_read_request_reply_packet(
        instruction_field: int, tid: int, status: int, buffer: bytes, buffer_length: int) -> bytes:
    """
    Creates an RMAP Reply to a RMAP Read Request packet.

    The function returns a ``ctypes`` character array (which is basically a bytes array) that
    can be passed into the EtherSpaceLink library function ``esl_write_packet()``.

    Args:
        instruction_field (int): the instruction field of the RMAP read request packet
        tid (int): the transaction identifier of the read request packet
        status (int): shall be 0 if the read request was successful, contain an error code otherwise.
        buffer (bytes): the data that was read as indicated by the read request
        buffer_length (int): the data length

    Returns:
        packet: a bytes object containing the full RMAP Reply packet.
    """

    buf = bytearray(12 + buffer_length + 1)

    buf[0] = 0x50  # Initiator address N-DPU or F-DPU
    buf[1] = 0x01  # RMAP Protocol ID
    buf[2] = instruction_field & 0x3F  # Clear the command bit as this is a reply
    buf[3] = status & 0xFF  # Status field: 0 on success
    buf[4] = 0x51  # Target address is always the N-FEE or F-FEE
    buf[5] = (tid >> 8) & 0xFF  # MSB of the Transition ID
    buf[6] = tid & 0xFF  # LSB of the Transition ID
    buf[7] = 0x00  # Reserved
    buf[8] = (buffer_length >> 16) & 0xFF  # data length (MSB)
    buf[9] = (buffer_length >> 8) & 0xFF  # data length
    buf[10] = buffer_length & 0xFF  # data length (LSB)
    buf[11] = rmap_crc_check(buf, 0, 11) & 0xFF  # Header CRC

    # Note that we assume here that len(buffer) == buffer_length.

    if len(buffer) != buffer_length:
        _LOGGER.warning(
            f"While creating an RMAP read reply packet, the length of the buffer ({len(buffer)}) "
            f"not equals the buffer_length ({buffer_length})"
        )

    for idx, value in enumerate(buffer):
        buf[12 + idx] = value

    buf[12 + buffer_length] = rmap_crc_check(buffer, 0, buffer_length) & 0xFF  # data CRC

    return bytes(buf)


def create_rmap_verified_write_packet(address: int, data: bytes, tid: int) -> bytes:
    """
    Create an RMAP packet for a verified write request on the FEE. The length of the data is
    by convention always 4 bytes and therefore not passed as an argument.

    Args:
        address: the start memory address on the FEE register map
        data: the data to be written in the register map at address [4 bytes]
        tid (int): transaction identifier

    Returns:
        packet: a bytes object containing the SpaceWire packet.
    """
    from egse.spw import update_transaction_identifier

    if len(data) < 4:
        raise ValueError(
            f"The data argument should be at least 4 bytes, but it is only {len(data)} bytes: {data=}.")

    if address > CRITICAL_AREA_END:
        raise ValueError("The address range for critical configuration is [0x00 - 0xFC].")

    tid = update_transaction_identifier(tid)

    # Buffer length is fixed at 24 bytes since the data length is fixed
    # at 4 bytes (32 bit addressing)

    buf = bytearray(21)

    # The values below are taken from the PLATO N-FEE to N-DPU
    # Interface Requirements Document [PLATO-DLR-PL-ICD-0010]

    buf[0] = 0x51  # Logical Address
    buf[1] = 0x01  # Protocol ID
    buf[2] = 0x7C  # Instruction
    buf[3] = 0xD1  # Key
    buf[4] = 0x50  # Initiator Address
    buf[5] = (tid >> 8) & 0xFF  # MSB of the Transition ID
    buf[6] = tid & 0xFF  # LSB of the Transition ID
    buf[7] = 0x00  # Extended address
    buf[8] = (address >> 24) & 0xFF  # address (MSB)
    buf[9] = (address >> 16) & 0xFF  # address
    buf[10] = (address >> 8) & 0xFF  # address
    buf[11] = address & 0xFF  # address (LSB)
    buf[12] = 0x00  # data length (MSB)
    buf[13] = 0x00  # data length
    buf[14] = 0x04  # data length (LSB)
    buf[15] = rmap_crc_check(buf, 0, 15) & 0xFF  # header CRC
    buf[16] = data[0]
    buf[17] = data[1]
    buf[18] = data[2]
    buf[19] = data[3]
    buf[20] = rmap_crc_check(buf, 16, 4) & 0xFF  # data CRC

    return bytes(buf)


def create_rmap_unverified_write_packet(address: int, data: bytes, length: int, tid: int) -> bytes:
    """
    Create an RMAP packet for a unverified write request on the FEE.

    Args:
        address: the start memory address on the FEE register map
        data: the data to be written in the register map at address
        length: the length of the data
        tid (int): transaction identifier

    Returns:
        packet: a bytes object containing the SpaceWire packet.
    """
    from egse.spw import update_transaction_identifier

    # We can only handle data for which the length >= the given length argument.

    if len(data) < length:
        raise ValueError(
            f"The length of the data argument ({len(data)}) is smaller than "
            f"the given length argument ({length})."
        )

    if len(data) > length:
        _LOGGER.warning(
            f"The length of the data argument ({len(data)}) is larger than "
            f"the given length argument ({length}). The data will be truncated "
            f"when copied into the packet."
        )

    if address <= CRITICAL_AREA_END:
        raise ValueError(
            f"The given address (0x{address:08X}) is in the range for critical configuration is "
            f"[0x00 - 0xFC]. Use the verified write function for this."
        )

    tid = update_transaction_identifier(tid)

    # Buffer length is fixed at 24 bytes since the data length
    # is fixed at 4 bytes (32 bit addressing)

    buf = bytearray(16 + length + 1)
    offset = 0

    buf[offset + 0] = 0x51  # Logical Address
    buf[offset + 1] = 0x01  # Protocol ID
    buf[offset + 2] = 0x6C  # Instruction
    buf[offset + 3] = 0xD1  # Key
    buf[offset + 4] = 0x50  # Initiator Address
    buf[offset + 5] = (tid >> 8) & 0xFF  # MSB of the Transition ID
    buf[offset + 6] = tid & 0xFF  # LSB of the Transition ID
    buf[offset + 7] = 0x00  # Extended address
    buf[offset + 8] = (address >> 24) & 0xFF  # address (MSB)
    buf[offset + 9] = (address >> 16) & 0xFF  # address
    buf[offset + 10] = (address >> 8) & 0xFF  # address
    buf[offset + 11] = address & 0xFF  # address (LSB)
    buf[offset + 12] = (length >> 16) & 0xFF  # data length (MSB)
    buf[offset + 13] = (length >> 8) & 0xFF  # data length
    buf[offset + 14] = length & 0xFF  # data length (LSB)
    buf[offset + 15] = rmap_crc_check(buf, 0, 15) & 0xFF  # header CRC

    offset += 16

    for idx, value in enumerate(data):
        buf[offset + idx] = value

    buf[offset + length] = rmap_crc_check(buf, offset, length) & 0xFF  # data CRC

    return bytes(buf)


def create_rmap_write_request_reply_packet(instruction_field: int, tid: int, status: int) -> bytes:
    buf = bytearray(8)

    buf[0] = 0x50  # Initiator address N-DPU or F-DPU
    buf[1] = 0x01  # RMAP Protocol ID
    buf[2] = instruction_field & 0x3F  # Clear the command bit as this is a reply
    buf[3] = status & 0xFF  # Status field: 0 on success
    buf[4] = 0x51  # Target address is always the N-FEE or F-FEE
    buf[5] = (tid >> 8) & 0xFF  # MSB of the Transition ID
    buf[6] = tid & 0xFF  # LSB of the Transition ID
    buf[7] = rmap_crc_check(buf, 0, 7) & 0xFF  # Header CRC

    return bytes(buf)


@static_vars(warning_count=0, stride=100)
def check_address_and_data_length(address: int, length: int, strict: bool = True) -> None:
    """
    Checks the address and length in the range of memory areas used by the FEE.

    The ranges are taken from the PLATO-DLR-PL-ICD-0010 N-FEE to N-DPU IRD.

    Args:
        address (int): the memory address of the FEE Register
        length (int): the number of bytes requested
        strict (bool): strictly apply the rules

    Raises:
        RMAPError: when address + length fall outside any specified area.
    """

    if not strict:
        # All these restrictions have been relaxed on the N-FEE.
        # We are returning here immediately instead of removing or commenting out the code.
        # The reason is that we can then bring back restriction easier and gradually.

        # A warning is sent out

        if not check_address_and_data_length.warning_count % check_address_and_data_length.stride:
            check_address_and_data_length.warning_count = 1
            _LOGGER.warning(
                "Address and data length checks have been disabled, because the N-FEE "
                "does not enforce restrictions in the critical memory area.")

        check_address_and_data_length.warning_count += 1

        return

    if length % 4:
        raise RMAPError(
            "The requested data length shall be a multiple of 4 bytes.", address, length
        )

    if address % 4:
        raise RMAPError("The address shall be a multiple of 4 bytes.", address, length)

    # Note that when checking the given data length, at the defined area end,
    # we can still read 4 bytes.

    if CRITICAL_AREA_START <= address <= CRITICAL_AREA_END:
        if length != 4:
            raise RMAPError(
                "Read requests to the critical area have a fixed data length of 4 bytes.",
                address, length
            )
    elif GENERAL_AREA_START <= address <= GENERAL_AREA_END:
        if length > 256:
            raise RMAPError(
                "Read requests to the general area have a maximum data length of 256 bytes.",
                address, length
            )
        if address + length > GENERAL_AREA_END + 4:
            raise RMAPError(
                "The requested data length for the general area is too large. "
                "The address + length exceeds the general area boundaries.",
                address, length
            )

    elif HK_AREA_START <= address <= HK_AREA_END:
        if length > 256:
            raise RMAPError(
                "Read requests to the housekeeping area have a maximum data length of 256 bytes.",
                address, length
            )
        if address + length > HK_AREA_END + 4:
            raise RMAPError(
                "The requested data length for the housekeeping area is too large. "
                "The address + length exceeds the housekeeping area boundaries.",
                address, length
            )

    elif WINDOWING_AREA_START <= address <= WINDOWING_AREA_END:
        if length > 4096:
            raise RMAPError(
                "Read requests to the windowing area have a maximum data length of 4096 bytes.",
                address, length
            )
        if address + length > WINDOWING_AREA_END + 4:
            raise RMAPError(
                "The requested data length for the windowing area is too large. "
                "The address + length exceeds the windowing area boundaries.", address, length
            )

    else:
        raise RMAPError("Register address for RMAP read requests is invalid.", address, length)


def rmap_crc_check(data, start, length) -> int:
    """Calculate the checksum for the given data."""
    return crc_calc(data, start, length)
