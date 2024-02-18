"""
This module defines classes and functions to work with SpaceWire packets.
"""
import logging
import os
import struct
import textwrap
from enum import IntEnum
from typing import Tuple
from typing import Union

import numpy as np

import egse.rmap
from egse.bits import clear_bit
from egse.bits import crc_calc
from egse.bits import set_bit
from egse.exceptions import Error
from egse.setup import SetupError
from egse.state import GlobalState

MODULE_LOGGER = logging.getLogger(__name__)

try:
    _ = os.environ["PLATO_CAMERA_IS_EM"]
    MODULE_LOGGER.warning(
        textwrap.dedent("""\
        The PLATO_CAMERA_IS_EM environment variable is defined.
            For the EM camera, image data and camera sensor data are interpreted as twos-complement and 
            converted accordingly. If the camera you are testing is not the EM camera, make sure the
            PLATO_CAMERA_IS_EM environment variable is not defined when starting your control servers.  
            """
        )
    )
    TWOS_COMPLEMENT_OFFSET = 32768 if _.capitalize() in ("1", "True", "Yes") else 0
except KeyError:
    TWOS_COMPLEMENT_OFFSET = 0


class CheckError(Error):
    """
    Raised when a check fails, and you want to pass a status values along with the message.
    """

    def __init__(self, message, status):
        self.message = message
        self.status = status


def update_transaction_identifier(tid: int) -> int:
    """
    Updates the transaction identifier and returns the new value.

    This identifier shall be incremented for each RMAP Request. The RMAP Request Reply packets
    shall copy the transaction ID of the RMAP Request packet in their transaction ID field.

    The transaction ID is a 16-bit field which is used to associate replies with the command
    that caused the reply.

    Args:
        tid (int): The current transaction identifier

    Returns:
        the updated transaction identifier (int).
    """
    tid = (tid + 1) & 0xFFFF
    return tid


class PacketType(IntEnum):
    """Enumeration type that defines the SpaceWire packet type."""

    DATA_PACKET = 0
    OVERSCAN_DATA = 1
    HOUSEKEEPING_DATA = 2  # N-FEE
    DEB_HOUSEKEEPING_DATA = 2  # F-FEE
    AEB_HOUSEKEEPING_DATA = 3  # F-FEE


class DataPacketType:
    """
    Defines the Data Packet Field: Type, which is a bit-field of 16 bits.

    Properties:
      * value: returns the data type as an integer
      * packet_type: the type of data packet, defined in PacketType enum.
      * mode: the FEE mode, defined in n_fee_mode and f_fee_mode enum
      * last_packet: flag which defines the last packet of a type in the current readout cycle
      * ccd_side: 0 for E-side (left), 1 for F-side (right), see egse.fee.fee_side
      * ccd_number: CCD number [0, 3]
      * frame_number: the frame number after sync
    """

    def __init__(self, data_type: int = 0):
        self._data_type: int = data_type
        # self.n_fee_side = GlobalState.setup.camera.fee.ccd_sides.enum

    @property
    def value(self) -> int:
        """Returns the data packet type as an int."""
        return self._data_type

    @property
    def packet_type(self):
        """Returns the packet type: 0 = data packet, 1 = overscan data, 2 = housekeeping packet."""
        return self._data_type & 0b0011

    @packet_type.setter
    def packet_type(self, value):
        if not 0 <= value < 3:
            raise ValueError(f"Packet Type can only have the value 0, 1, or 2, {value=} given.")
        x = self._data_type
        for idx, bit in enumerate([0, 1]):
            x = set_bit(x, bit) if value & (1 << idx) else clear_bit(x, bit)
        self._data_type = x

    @property
    def mode(self) -> int:
        return (self._data_type & 0b1111_0000_0000) >> 8

    @mode.setter
    def mode(self, value: int):
        x = self._data_type
        for idx, bit in enumerate([8, 9, 10, 11]):
            x = set_bit(x, bit) if value & (1 << idx) else clear_bit(x, bit)
        self._data_type = x

    @property
    def last_packet(self) -> bool:
        return bool(self._data_type & 0b1000_0000)

    @last_packet.setter
    def last_packet(self, flag: bool):
        self._data_type = set_bit(self._data_type, 7) if flag else clear_bit(self._data_type, 7)

    @property
    def ccd_side(self) -> int:
        return (self._data_type & 0b0100_0000) >> 6

    @ccd_side.setter
    def ccd_side(self, value: int):
        self._data_type = set_bit(self._data_type, 6) if value & 0b0001 else clear_bit(self._data_type, 6)

    @property
    def ccd_number(self) -> int:
        return (self._data_type & 0b0011_0000) >> 4

    @ccd_number.setter
    def ccd_number(self, value):
        x = self._data_type
        for idx, bit in enumerate([4, 5]):
            x = set_bit(x, bit) if value & (1 << idx) else clear_bit(x, bit)
        self._data_type = x

    @property
    def frame_number(self) -> int:
        return (self._data_type & 0b1100) >> 2

    @frame_number.setter
    def frame_number(self, value):
        x = self._data_type
        for idx, bit in enumerate([2, 3]):
            x = set_bit(x, bit) if value & (1 << idx) else clear_bit(x, bit)
        self._data_type = x

    def __str__(self) -> str:
        from egse.fee import n_fee_mode
        n_fee_side = GlobalState.setup.camera.fee.ccd_sides.enum

        return (
            f"mode:{n_fee_mode(self.mode).name}, last_packet:{self.last_packet}, "
            f"CCD side:{n_fee_side(self.ccd_side).name}, CCD number:{self.ccd_number}, "
            f"Frame number:{self.frame_number}, Packet Type:{PacketType(self.packet_type).name}"
        )


def to_string(data: Union[DataPacketType]) -> str:
    """Returns a 'user-oriented' string representation of the SpW DataPacketType.

    The purpose of this function is to represent the N-FEE information in a user-oriented way.
    That means for certain values that they will be converted into the form the a user understands
    and that may be different or reverse from the original N-FEE definition. An example is the
    CCD number which is different from the user perspective with respect to the N-FEE.

    If any other object type is passed, the data.__str__() method will be returned without
    processing or conversion.

    Args:
        data: a DataPacketType
    """
    from egse.fee import n_fee_mode
    n_fee_side = GlobalState.setup.camera.fee.ccd_sides.enum

    if isinstance(data, DataPacketType):
        try:
            ccd_bin_to_id = GlobalState.setup.camera.fee.ccd_numbering.CCD_BIN_TO_ID
        except AttributeError:
            raise SetupError("No entry in the setup for camera.fee.ccd_numbering.CCD_BIN_TO_ID")
        return (
            f"mode:{n_fee_mode(data.mode).name}, last_packet:{data.last_packet}, "
            f"CCD side:{n_fee_side(data.ccd_side).name}, CCD number:"
            f"{ccd_bin_to_id[data.ccd_number]}, "
            f"Frame number:{data.frame_number}, Packet Type:{PacketType(data.packet_type).name}"
        )
    else:
        return data.__str__()


class DataPacketHeader:
    """
    Defines the header of a data packet.

    The full header can be retrieved as a bytes object with the `data_as_bytes()` method.

    Properties:
      * logical_address: fixed value of  0x50
      * protocol_id: fixed value of 0xF0
      * length: length of the data part of the packet, i.e. the packet length - size of the header
      * type: data packet type as defined by DataPacketType
      * frame_counter:
      * sequence_counter: a packet sequence counter per CCD
    """
    def __init__(self, header_data: bytes = None):
        self.header_data = bytearray(
            header_data or bytes([0x50, 0xF0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))

        if len(self.header_data) != 10:
            raise ValueError(f"The length of the header for a data packet shall be 10 bytes, "
                             f"got {len(self.header_data)}.")

        self.n_fee_side = GlobalState.setup.camera.fee.ccd_sides.enum

    def data_as_bytes(self) -> bytes:
        """Returns the full header as a bytes object."""
        return bytes(self.header_data)

    @property
    def logical_address(self) -> int:
        return self.header_data[0]

    @logical_address.setter
    def logical_address(self, value: int):
        self.header_data[0] = value

    @property
    def protocol_id(self) -> int:
        return self.header_data[1]

    @protocol_id.setter
    def protocol_id(self, value: int):
        self.header_data[1] = value

    @property
    def length(self) -> int:
        return int.from_bytes(self.header_data[2:4], byteorder='big')

    @length.setter
    def length(self, value: int):
        self.header_data[2:4] = value.to_bytes(2, 'big')

    @property
    def type(self):
        return int.from_bytes(self.header_data[4:6], byteorder='big')

    @type.setter
    def type(self, value: Union[int, bytes, DataPacketType]):
        if isinstance(value, bytes):
            self.header_data[4:6] = value
        elif isinstance(value, DataPacketType):
            self.header_data[4:6] = value.value.to_bytes(2, 'big')
        else:
            self.header_data[4:6] = value.to_bytes(2, 'big')

    @property
    def type_as_object(self):
        return DataPacketType(self.type)

    @property
    def packet_type(self):
        return self.type_as_object.packet_type

    @packet_type.setter
    def packet_type(self, value: int):
        type_obj = self.type_as_object
        type_obj.packet_type = value
        self.type = type_obj

    @property
    def last_packet(self):
        return self.type_as_object.last_packet

    @last_packet.setter
    def last_packet(self, flag: bool):
        type_obj = self.type_as_object
        type_obj.last_packet = flag
        self.type = type_obj

    @property
    def frame_counter(self):
        return int.from_bytes(self.header_data[6:8], byteorder='big')

    @frame_counter.setter
    def frame_counter(self, value):
        self.header_data[6:8] = value.to_bytes(2, 'big')

    @property
    def sequence_counter(self):
        return int.from_bytes(self.header_data[8:10], byteorder='big')

    @sequence_counter.setter
    def sequence_counter(self, value):
        self.header_data[8:10] = value.to_bytes(2, 'big')

    def as_dict(self):
        from egse.fee import n_fee_mode

        data_packet_type = DataPacketType(self.type)
        return dict(
            logical_address=f"0x{self.logical_address:02X}",
            protocol_id=f"0x{self.protocol_id:02X}",
            length=self.length,
            type=f"0x{self.type:04X}",
            frame_counter=self.frame_counter,
            sequence_counter=self.sequence_counter,
            packet_type=data_packet_type.packet_type,
            frame_number=data_packet_type.frame_number,
            ccd_number=data_packet_type.ccd_number,
            ccd_side=self.n_fee_side(data_packet_type.ccd_side).name,
            last_packet=data_packet_type.last_packet,
            mode=n_fee_mode(data_packet_type.mode).name,
        )


class SpaceWirePacket:
    """Base class for any packet transmitted over a SpaceWire cable."""

    # these settings are used by this class and its sub-classes to configure the print options
    # for the numpy arrays.

    _threshold = 300  # sys.maxsize
    _edgeitems = 10
    _linewidth = 120

    def __init__(self, data: Union[bytes, np.ndarray]):
        """
        Args:
            data: a bytes object or a numpy array of type np.uint8 (not enforced)
        """
        self._bytes = bytes(data)

    def __repr__(self):
        limit = 25
        data_hex = ' '.join(f"{x:02x}" for x in self._bytes[:limit])
        data_hex += '...' if len(self._bytes) > limit else ''

        msg = (
            f"{self.__class__.__name__}(0x{data_hex})"
        )
        return msg

    def __len__(self):
        return len(self._bytes)

    @property
    def packet_as_bytes(self):
        return self._bytes

    @property
    def packet_as_ndarray(self):
        return np.frombuffer(self._bytes, dtype=np.uint8)

    @property
    def logical_address(self):
        # TODO: what about a timecode, that has no logical address?
        return self._bytes[0]

    @property
    def protocol_id(self):
        # TODO: what about a timecode, that has no protocol id?
        return self._bytes[1]

    def header_as_bytes(self) -> bytes:
        # TODO: what about timecode, this has no header, except maybe the first byte: 0x91
        raise NotImplementedError

    @staticmethod
    def create_packet(data: Union[bytes, np.ndarray]):
        """
        Factory method that returns a SpaceWire packet of the correct type based on the information
        in the header.
        """
        # MODULE_LOGGER.info(f"{len(data) = }")

        if TimecodePacket.is_timecode_packet(data):
            return TimecodePacket(data)
        if HousekeepingPacket.is_housekeeping_packet(data):
            return HousekeepingPacket(data)
        if DataDataPacket.is_data_data_packet(data):
            return DataDataPacket(data)
        if OverscanDataPacket.is_overscan_data_packet(data):
            return OverscanDataPacket(data)
        if WriteRequest.is_write_request(data):
            return WriteRequest(data)
        if WriteRequestReply.is_write_reply(data):
            return WriteRequestReply(data)
        if ReadRequest.is_read_request(data):
            return ReadRequest(data)
        if ReadRequestReply.is_read_reply(data):
            return ReadRequestReply(data)
        return SpaceWirePacket(data)


class ExtensionPacket:
    def __init__(self):
        pass


class DataPacket(SpaceWirePacket):
    """
    Base class for proprietary SpaceWire data packets that are exchanged between FEE and DPU.

    .. note::
        This class should not be instantiated directly. Use the SpaceWirePacket.create_packet()
        factory method or the constructors of one of the sub-classes of this DataPacket class.
    """

    DATA_HEADER_LENGTH = 10

    def __init__(self, data: Union[bytes, np.ndarray]):
        """
        Args:
            data: a bytes object or a numpy array
        """
        if not self.is_data_packet(data):
            raise ValueError(
                f"Can not create a DataPacket from the given data {[f'0x{x:02x}' for x in data]}"
            )

        super().__init__(data)

        if (data[2] == 0x00 and data[3] == 0x00) or len(data) == self.DATA_HEADER_LENGTH:
            MODULE_LOGGER.warning(
                f"SpaceWire data packet without data found, packet={[f'0x{x:02x}' for x in data]}"
            )

        self._length = (data[2] << 8) + data[3]

        if len(data) != self._length + self.DATA_HEADER_LENGTH:
            MODULE_LOGGER.warning(
                f"The length of the data argument ({len(data)}) given to "
                f"the constructor of {self.__class__.__name__} (or sub-classes) is inconsistent "
                f"with the length data field ({self._length} + 10) in the packet header."
            )
            raise ValueError(
                f"{self.__class__.__name__} header: data-length field ({self._length}) not "
                f"consistent with packet length ({len(data)}). Difference should be "
                f"{self.DATA_HEADER_LENGTH}."
            )

        self._type = DataPacketType((data[4] << 8) + data[5])
        self._data = None  # lazy loading of data from self._bytes

    @property
    def length(self) -> int:
        """Returns the data length in bytes.

        .. note:: length == len(data_nd_array) * 2
            This length property returns the length of the data area in bytes. This value is
            taken  from the header of the data packet. If you want to compare this with the size
            of the data_as_ndarray property, multiply the length by 2 because the data is 16-bit
            integers, not bytes.

        Returns:
            the size of the data area of the packet in bytes.
        """
        return self._length

    @property
    def data_as_ndarray(self):
        """
        Returns the data from this data packet as a 16-bit integer Numpy array.

        .. note::
            The data has been converted from the 8-bit packet data into 16-bit integers. That
            means the length of this data array will be half the length of the data field the
            packet, i.e. ``len(data) == length // 2``.
            The reason for this is that pixel data has a size of 16-bit.

        .. todo::
            check if the data-length of HK packets should also be a multiple of 16.

        Returns:
            data: Numpy array with the data from this packet (type is np.uint16)

        """

        # We decided to lazy load/construct the data array. The reason is that the packet may be
        # created / transferred without the need to unpack the data field into a 16-bit numpy array.

        if self._data is None:
            # The data is in two's-complement. The most significant bit (msb) shall be inverted
            # according to Sampie Smit. That is done in the following line where the msb in each
            # byte on an even index is inverted.

            # data = [toggle_bit(b, 7) if not idx % 2 else b for idx, b in enumerate(self._bytes)]
            # data = bytearray(data)
            # data_1 = np.frombuffer(data, offset=10, dtype='>u2')

            # Needs further confirmation, but the following line should have the same effect as
            # the previous three lines.
            data_2 = np.frombuffer(self._bytes, offset=10, dtype='>i2') + TWOS_COMPLEMENT_OFFSET

            # Test if the results are identical, left the code in until we are fully confident
            # if diff := np.sum(np.cumsum(data_1 - data_2)):
            #     MODULE_LOGGER.info(f"cumsum={diff}")

            self._data = data_2.astype('uint16')
        return self._data

    @property
    def data(self) -> bytes:
        return self._bytes[10: 10 + self._length]

    @property
    def type(self) -> DataPacketType:
        return self._type

    @property
    def frame_counter(self):
        return (self._bytes[6] << 8) + self._bytes[7]

    @property
    def sequence_counter(self):
        return (self._bytes[8] << 8) + self._bytes[9]

    @property
    def header(self) -> DataPacketHeader:
        return DataPacketHeader(self.header_as_bytes())

    def header_as_bytes(self):
        return self._bytes[:10]

    @classmethod
    def is_data_packet(cls, data: np.ndarray) -> bool:
        if len(data) < 10 or data[0] != 0x50 or data[1] != 0xF0:
            return False
        return True

    def __str__(self):
        options = np.get_printoptions()
        np.set_printoptions(
            formatter={"int": lambda x: f"0x{x:04x}"},
            threshold=super()._threshold,
            edgeitems=super()._edgeitems,
            linewidth=super()._linewidth,
        )
        limit = 50
        header_hex = ' '.join(f'{byte:02X}' for byte in self.header_as_bytes()[:limit])
        data_hex = ' '.join(f'{byte:02X}' for byte in self.data[:limit])
        data_ascii = ''.join((chr(byte) if 32 <= byte <= 126 else '.') for byte in self.data[:limit])

        msg = (
            f"{self.__class__.__name__}:\n"
            f"  Logical Address = 0x{self.logical_address:02X}\n"
            f"  Protocol ID = 0x{self.protocol_id:02X}\n"
            f"  Length = {self.length}\n"
            f"  Type = {self._type}\n"
            f"  Frame Counter = {self.frame_counter}\n"
            f"  Sequence Counter = {self.sequence_counter}\n"
            f"  Header = {header_hex}\n"
            f"  Data HEX = {data_hex}\n"
            f"  Data ASC = {data_ascii}\n"
        )
        np.set_printoptions(**options)
        return msg


class DataDataPacket(DataPacket):
    """Proprietary Data Packet for N-FEE and F-FEE CCD image data."""

    @classmethod
    def is_data_data_packet(cls, data: Union[bytes, np.ndarray]) -> bool:
        if len(data) <= 10:
            return False
        if data[0] != 0x50:
            return False
        if data[1] != 0xF0:
            return False
        type_ = DataPacketType((data[4] << 8) + data[5])
        if type_.packet_type == PacketType.DATA_PACKET:
            return True
        return False


class OverscanDataPacket(DataPacket):
    """Proprietary Overscan Data Packet for N-FEE and F-FEE CCD image data."""

    @classmethod
    def is_overscan_data_packet(cls, data: Union[bytes, np.ndarray]) -> bool:
        if len(data) <= 10:
            return False
        if data[0] != 0x50:
            return False
        if data[1] != 0xF0:
            return False
        type_ = DataPacketType((data[4] << 8) + data[5])
        if type_.packet_type == PacketType.OVERSCAN_DATA:
            return True
        return False


class HousekeepingPacket(DataPacket):
    """Proprietary Housekeeping data packet for the N-FEE and F-FEE."""

    def __init__(self, data: Union[bytes, np.ndarray]):
        """
        Args:
            data: a numpy array of type np.uint8 (not enforced)
        """
        if not self.is_housekeeping_packet(data):
            raise ValueError(f"Can not create a HousekeepingPacket from the given data {data}")

        # The __init__ method of DataPacket already checks e.g. data-length against packet length,
        # so there is no need for these tests here.

        super().__init__(data)

    @classmethod
    def is_housekeeping_packet(cls, data: Union[bytes, np.ndarray]) -> bool:
        if len(data) <= 10:
            return False
        if data[0] != 0x50:
            return False
        if data[1] != 0xF0:
            return False
        type_ = DataPacketType((data[4] << 8) + data[5])
        if type_.packet_type == PacketType.HOUSEKEEPING_DATA:
            return True
        return False


class TimecodePacket(SpaceWirePacket):
    """A Timecode Packet.

    This packet really is an extended packet which is generated by the Diagnostic SpaceWire
    Interface (DSI) to forward a SpaceWire timecode over the Ethernet connection.
    """

    def __init__(self, data: Union[bytes, np.ndarray]):
        super().__init__(data)

    @property
    def timecode(self) -> int:
        return self._bytes[1] & 0x3F

    def header_as_bytes(self) -> bytes:
        return self._bytes[0:1]

    @classmethod
    def is_timecode_packet(cls, data: Union[bytes, np.ndarray]) -> bool:
        return data[0] == 0x91

    def __str__(self):
        return f"Timecode Packet: timecode = 0x{self.timecode:02x} ({self.timecode:2d})"


class RMAPRequestMixin(SpaceWirePacket):
    @property
    def key(self):
        """Returns the key field."""
        return get_key_field(self._bytes)

    @property
    def initiator_address(self):
        """Returns the initiator logical address."""
        return self._bytes[4]

    @property
    def data_length(self):
        return get_data_length(self._bytes)

    @property
    def address(self):
        return get_address(self._bytes)


class RMAPRequestReplyMixin(SpaceWirePacket):
    @property
    def target_address(self):
        """Returns the target logical address."""
        return self._bytes[4]

    @property
    def status(self):
        """Returns the status field."""
        return self._bytes[3]


class RMAPPacket(SpaceWirePacket):
    """Base class for RMAP SpaceWire packets."""

    def __init__(self, data: Union[bytes, np.ndarray]):
        if not self.is_rmap_packet(data):
            raise ValueError(f"Can not create a RMAPPacket from the given data {data}")
        super().__init__(data)

    def __str__(self):
        msg = (
            f"RMAP Base Packet ({len(self)} bytes)\n"
            f"Logical address:    0x{self.logical_address:02x}\n"
            f"Protocol ID:        0x{self.protocol_id:02x}\n"
            f"Instruction:        0x{self.instruction:02x} (0o{self.instruction:08b})\n"
            f"Transaction ID:     0x{self.transaction_id:04x} ({self.transaction_id})\n"
            f"Data = {self._bytes}\n"
        )
        return msg

    @property
    def instruction(self):
        return get_instruction_field(self._bytes)

    @property
    def transaction_id(self):
        return get_transaction_identifier(self._bytes)

    @property
    def header_crc(self):
        return get_header_crc(self._bytes)

    @property
    def data_crc(self):
        return get_data_crc(self._bytes)

    @classmethod
    def is_rmap_packet(cls, data: Union[bytes, np.ndarray]):
        if data[1] == 0x01:  # Protocol ID
            return True
        return False


class WriteRequest(RMAPPacket, RMAPRequestMixin):
    """A Write Request SpaceWire RMAP Packet."""

    def __init__(self, data: Union[bytes, np.ndarray]):
        super().__init__(data)

    def is_verified(self):
        return self._bytes[2] == 0x7C

    def is_unverified(self):
        return self._bytes[2] == 0x6C

    @property
    def data_length(self):
        return get_data_length(self._bytes)

    @property
    def data(self) -> bytes:
        return get_data(self._bytes)

    @classmethod
    def is_write_request(cls, data: Union[bytes, np.ndarray]):
        if not RMAPPacket.is_rmap_packet(data):
            return False
        if data[0] != 0x51:
            return False
        if (data[2] == 0x7C or data[2] == 0x6C) and data[3] == 0xD1:
            return True
        return False

    def __str__(self):
        prefix = "Verified" if self.is_verified() else "Unverified"
        limit = 32
        data_hex = ' '.join(f'{x:02X}' for x in self.data[:limit])
        data_hex += ' ...' if len(self.data) > limit else ''
        data_asc = ''.join((chr(byte) if 32 <= byte <= 126 else '.') for byte in self.data[:limit])
        data_asc += ' ...' if len(self.data) > limit else ''

        packet = self.packet_as_bytes
        msg = (
            f"RMAP {prefix} Write Request ({len(packet)} bytes)\n"
            f"Target address:     0x{self.logical_address:02x}\n"
            f"Protocol ID:        0x{self.protocol_id:02x}\n"
            f"Instruction:        0x{self.instruction:02x} (0o{self.instruction:08b})\n"
            f"Key:                0x{self.key:02x}\n"
            f"Initiator address:  0x{self.initiator_address:02x}\n"
            f"Transaction ID:     0x{self.transaction_id:04x} ({self.transaction_id})\n"
            f"Address:            0x{self.address:08x}\n"
            f"Data Length:        {self.data_length}\n"
            f"Header CRC:         0x{self.header_crc:02x}\n"
            f"data (hex):         0x{data_hex}\n"
            f"data (ascii):       {data_asc}\n"
            f"Data CRC:           0x{self.data_crc:02x}\n"
        )
        return msg


class WriteRequestReply(RMAPPacket, RMAPRequestReplyMixin):
    """An RMAP Reply packet to a Write Request."""

    def __init__(self, data: Union[bytes, np.ndarray]):
        super().__init__(data)

    @classmethod
    def is_write_reply(cls, data: Union[bytes, np.ndarray]):
        if not RMAPPacket.is_rmap_packet(data):
            return False
        if data[0] != 0x50:
            return False
        if (data[2] == 0x3C or data[2] == 0x2C) and data[4] == 0x51:
            return True

    def __str__(self):
        msg = (
            f"Write Request Reply ({len(self)} bytes)\n"
            f"Initiator address:  0x{self.logical_address:02x}\n"
            f"Protocol ID:        0x{self.protocol_id:02x}\n"
            f"Instruction:        0x{self.instruction:02x} (0o{self.instruction:08b})\n"
            f"Status:             0x{self.status:02x}\n"
            f"target address:     0x{self.target_address:02x}\n"
            f"transaction ID:     0x{self.transaction_id:02x} ({self.transaction_id})\n"
            f"Header CRC:         0x{self.header_crc:02x}\n"
        )

        return msg


class ReadRequest(RMAPPacket, RMAPRequestMixin):
    """A Read Request SpaceWire RMAP Packet."""

    def __init__(self, data: Union[bytes, np.ndarray]):
        super().__init__(data)

    @classmethod
    def is_read_request(cls, data: Union[bytes, np.ndarray]):
        if not RMAPPacket.is_rmap_packet(data):
            return False
        if data[0] != 0x51:
            return False
        if data[2] == 0x4C and data[3] == 0xD1:
            return True
        return False

    def __str__(self):
        msg = (
            f"RMAP Read Request ({len(self)} bytes)\n"
            f"Target address:     0x{self.logical_address:02x}\n"
            f"Protocol ID:        0x{self.protocol_id:02x}\n"
            f"Instruction:        0x{self.instruction:02x} (0o{self.instruction:08b})\n"
            f"Key:                0x{self.key:02x}\n"
            f"Initiator address:  0x{self.initiator_address:02x}\n"
            f"Transaction ID:     0x{self.transaction_id:04x} ({self.transaction_id})\n"
            f"(Extended) Address: 0x{self.address:08x}\n"
            f"Data Length:        {self.data_length}\n"
            f"Header CRC:         0x{self.header_crc:02x}\n"
        )

        return msg


class ReadRequestReply(RMAPPacket, RMAPRequestReplyMixin):
    """An RMAP Reply packet to a Read Request."""

    def __init__(self, data: Union[bytes, np.ndarray]):
        super().__init__(data)

    @classmethod
    def is_read_reply(cls, data: Union[bytes, np.ndarray]):
        if not RMAPPacket.is_rmap_packet(data):
            return False
        if data[0] != 0x50:
            return False
        if data[2] == 0x0C and data[4] == 0x51:
            return True

    @property
    def data(self) -> bytes:
        return get_data(self._bytes)

    @property
    def data_length(self):
        return get_data_length(self._bytes)

    def __str__(self):
        data_length = self.data_length
        limit = 32
        data_hex = ' '.join(f'{x:02X}' for x in self.data[:limit])
        data_hex += ' ...' if len(self.data) > limit else ''
        data_asc = ''.join((chr(byte) if 32 <= byte <= 126 else '.') for byte in self.data[:limit])
        data_asc += ' ...' if len(self.data) > limit else ''

        msg = (
            f"Read Request Reply ({len(self)} bytes)\n"
            f"Initiator address:  0x{self.logical_address:02x}\n"
            f"Protocol ID:        0x{self.protocol_id:02x}\n"
            f"Instruction:        0x{self.instruction:02x} (0o{self.instruction:08b})\n"
            f"Status:             0x{self.status:02x}\n"
            f"target address:     0x{self.target_address:02x}\n"
            f"transaction ID:     0x{self.transaction_id:02x} ({self.transaction_id})\n"
            f"Data Length:        {self.data_length}\n"
            f"Header CRC:         0x{self.header_crc:02x}\n"
            f"Data (hex):         0x{data_hex}\n"
            f"Data (ascii):       {data_asc}\n"
            f"Data CRC:           0x{self.data_crc:02x}\n"
        )

        return msg


class SpaceWireInterface:
    """
    This interface defines methods that are used by the DPU to communicate with the FEE over
    SpaceWire.
    """

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def configure(self):
        raise NotImplementedError

    def flush(self):
        raise NotImplementedError

    def send_timecode(self, timecode: int):
        """Send a timecode over the transport layer."""
        raise NotImplementedError

    def read_packet(self, timeout: int = None) -> Tuple[int, bytes]:
        """
        Read a full packet from the SpaceWire transport layer.

        Args:
            timeout (int): timeout in milliseconds [default=None]
        Returns:
            A tuple with the terminator value and a bytes object containing the packet.
        """
        raise NotImplementedError

    def write_packet(self, packet: bytes):
        """
        Write a full packet to the SpaceWire transport layer.

        Args:
            packet (bytes): a bytes object containing the SpaceWire packet

        Returns:
            None.
        """
        raise NotImplementedError

    def read_register(self, address: int, length: int = 4, strict: bool = True) -> bytes:
        """
        Reads the data for the given register from the FEE memory map.

        This function sends an RMAP read request for the register to the FEE.

        Args:
            address: the start address (32-bit aligned) in the remote memory
            length: the number of bytes to read from the remote memory [default = 4]
            strict: perform strict checking of address and length

        Returns:
            data: the 32-bit data that was read from the FEE.
        """
        raise NotImplementedError

    def write_register(self, address: int, data: bytes):
        """
        Writes the data from the given register to the N-FEE memory map.

        The function reads the data for the registry from the local register map
        and then sends an RMAP write request for the register to the N-FEE.

        .. note:: it is assumed that the local register map is up-to-date.

        Args:
            address: the start address (32-bit aligned) in the remote memory
            data: the data that will be written into the remote memory

        Raises:
            RMAPError: when data can not be written on the target, i.e. the N-FEE.
        """

        raise NotImplementedError

    def read_memory_map(self, address: int, size: int):
        """
        Read (part of) the memory map from the N-FEE.

        Args:
            address: start address
            size: number of bytes to read

        Returns:
            a bytes object containing the requested memory map.
        """

        raise NotImplementedError


# General RMAP helper functions ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_protocol_id(data: bytes) -> int:
    """
    Returns the protocol identifier field. The protocol ID is 1 (0x01) for the RMAP protocol.
    """
    return data[1]


def is_rmap(rx_buffer):
    """
    Returns True if the buffer represents an RMAP packet, False otherwise.
    """
    return get_protocol_id(rx_buffer) == egse.rmap.RMAP_PROTOCOL_ID


def get_reply_address_field_length(rx_buffer) -> int:
    """Returns the size of reply address field.

    This function returns the actual size of the reply address field. It doesn't return
    the content of the reply address length field. If you need that information, use the
    reply_address_length() function that work on the instruction field.

    Returns:
         length: the size of the reply address field.
    """
    instruction = get_instruction_field(rx_buffer)
    return reply_address_length(instruction) * 4


def get_data(rxbuf) -> bytes:
    """
    Return the data from the RMAP packet.

    Raises:
        ValueError: if there is no data section in the packet.
    """
    instruction_field = get_instruction_field(rxbuf)

    if is_write(instruction_field) and is_reply(instruction_field):
        raise ValueError("A WriteRequestReply packet doesn't contain a data section.")
    elif is_read(instruction_field) and is_command(instruction_field):
        raise ValueError("A ReadRequest packet doesn't contain a data section.")

    address_length = get_reply_address_field_length(rxbuf)
    data_length = get_data_length(rxbuf)

    offset = 12 if is_read(instruction_field) else 16

    return rxbuf[offset + address_length:offset + address_length + data_length]


def check_data_crc(rxbuf):
    """
    Verifies that the data CRC that is given in the packet matches the calculated data CRC.

    The only packets that have a data CRC are: WriteRequest, ReadRequestReply, and an F-CAM DataPacket.

    Raises:
        A CheckError when the provide and calculated CRC do not match.
    """
    instruction_field = get_instruction_field(rxbuf)
    address_length = get_reply_address_field_length(rxbuf)
    data_length = get_data_length(rxbuf)

    offset = 12 if is_read(instruction_field) else 16
    idx = offset + address_length

    d_crc = rxbuf[idx + data_length]
    c_crc = crc_calc(rxbuf, idx, data_length) & 0xFF
    if d_crc != c_crc:
        raise CheckError(
            f"Data CRC doesn't match calculated CRC, d_crc=0x{d_crc:02X} & c_crc=0x{c_crc:02X}"
        )


def get_data_crc(rxbuf):
    """
    Returns the data CRC of the RMAP packet.

    The only packets that have a data CRC are: WriteRequest, ReadRequestReply, and an F-CAM DataPacket.
    """
    instruction_field = get_instruction_field(rxbuf)
    address_length = get_reply_address_field_length(rxbuf)
    data_length = get_data_length(rxbuf)

    offset = 12 if is_read(instruction_field) else 16
    idx = offset + address_length

    d_crc = rxbuf[idx + data_length]

    return d_crc


def check_header_crc(rxbuf):
    """
    Verifies that the header CRC that is given in the packet matches the calculated header CRC.

    Only RMAP Request and RequestReply packets have a header CRC, data packets not.

    Raises:
        A CheckError when the provide and calculated CRC do not match.
    """
    instruction_field = get_instruction_field(rxbuf)
    if is_command(instruction_field):
        offset = 15
    elif is_write(instruction_field):
        offset = 7
    else:
        offset = 11

    idx = offset + get_reply_address_field_length(rxbuf)
    h_crc = rxbuf[idx]
    c_crc = crc_calc(rxbuf, 0, idx)
    if h_crc != c_crc:
        raise CheckError(
            f"Header CRC doesn't match calculated CRC, h_crc=0x{h_crc:02X} & c_crc=0x{c_crc:02X}"
        )


def get_header_crc(rxbuf):
    """
    Returns the Header CRC of the RMAP packet.

    Only RMAP Request and RequestReply packets have a header CRC, data packets not.
    """
    instruction_field = get_instruction_field(rxbuf)
    if is_command(instruction_field):
        offset = 15
    elif is_write(instruction_field):
        offset = 7
    else:
        offset = 11

    idx = offset + get_reply_address_field_length(rxbuf)
    h_crc = rxbuf[idx]

    return h_crc


def get_data_length(rxbuf) -> int:
    """
    Returns the length of the data part of an RMAP Request packet. The returned value
    is the number of bytes.

    Raises:
        TypeError: when this method is used on a Write Request Reply packet (which has no
            data length).
    """
    instruction_field = get_instruction_field(rxbuf)

    if not is_command(instruction_field) and is_write(instruction_field):
        raise TypeError("There is no data length field for Write Request Reply packets, "
                        "asking for the data length is an invalid operation.")

    offset = 12 if is_command(instruction_field) else 8
    idx = offset + get_reply_address_field_length(rxbuf)

    # We could use two alternative decoding methods here:

    # data_length = int.from_bytes(rxbuf[idx:idx+3], byteorder='big')  # (timeit=1.166s)
    data_length = struct.unpack('>L', b'\x00' + rxbuf[idx:idx + 3])[0]  # (timeit=0.670s)

    return data_length


def get_address(rxbuf) -> int:
    """
    Returns the address field (including the extended address field if the address is 40-bits).

    Raises:
        TypeError: when this method is used on a Reply packet (which has no address field).
    """
    instruction_field = get_instruction_field(rxbuf)

    if not is_command(instruction_field):
        raise TypeError("There is no address field for Reply packets, asking for the address is "
                        "an invalid operation.")

    idx = 7 + get_reply_address_field_length(rxbuf)
    extended_address = rxbuf[idx]
    idx += 1
    address = struct.unpack('>L', rxbuf[idx:idx + 4])[0]
    if extended_address:
        address = address + (extended_address << 32)
    return address


def get_instruction_field(rxbuf):
    """
    Returns the instruction field of the RMAP packet.
    """
    idx = 2
    return rxbuf[idx]


def get_key_field(rxbuf):
    """
    Returns the 'Key' field of the RMAP packet.
    """
    idx = 3
    return rxbuf[idx]


def check_instruction(rx_buffer) -> None:
    """
    Check the instruction field for inconsistencies and report the values in the LOGGER at DEBUG
    level.


    Args:
        rx_buffer (bytes): The read buffer which contains the SpW packet

    Raises:
        CheckError: when the reserved bit is not zero,

    Returns:
        None.
    """
    from egse.rmap import RMAP_NOT_IMPLEMENTED_AUTHORISED

    # The Instruction Field is the third byte (base=0) of the packet buffer.
    # Description of the Instruction Field can be found in ECSS-E-ST-50-52C.

    instruction = get_instruction_field(rx_buffer)
    if is_reserved(instruction):
        raise CheckError(
            f"Instruction field [{instruction:08b}] reserved bit is not 0x00",
            RMAP_NOT_IMPLEMENTED_AUTHORISED
        )

    msg = "RMAP Instruction Field: "
    msg += "Command; " if is_command(instruction) else "Reply; "
    msg += "write; " if is_write(instruction) else "read; "
    msg += "verify; " if is_verify(instruction) else "don't verify; "
    msg += "reply; " if is_reply_required(instruction) else "don't reply; "
    msg += "increment; " if is_increment(instruction) else "no increment; "

    MODULE_LOGGER.debug(msg)
    if reply_address_length(instruction):
        MODULE_LOGGER.debug(f"Reply address length = {reply_address_length(instruction)} bytes.")


def check_protocol_id(rxbuf):
    from egse.rmap import RMAP_PROTOCOL_ID, RMAP_GENERAL_ERROR

    idx = 1
    protocol_id = rxbuf[idx]
    if protocol_id != RMAP_PROTOCOL_ID:
        raise CheckError(
            f"Protocol id is not the expected value {protocol_id}, expected {RMAP_PROTOCOL_ID}",
            RMAP_GENERAL_ERROR)


def get_target_logical_address(rxbuf: bytes) -> int:
    """
    The target logical address is always the FEE, i.e. 0x50. The location of the target logical
    address is different for Request and RequestReply packets.
    """
    instruction = get_instruction_field(rxbuf)
    offset = 0 if is_command(instruction) else 4
    tla_idx = offset + get_reply_address_field_length(rxbuf)
    tla_rxbuf = rxbuf[tla_idx]
    return tla_rxbuf


def check_target_logical_address(rxbuf, tla):
    from egse.rmap import RMAP_GENERAL_ERROR

    tla_rxbuf = get_target_logical_address(rxbuf)
    if tla != tla_rxbuf:
        raise CheckError(
            f"Target Logical Address doesn't match, tla=0x{tla:02X} & rxbuf[0]=0x{tla_rxbuf:02X}",
            RMAP_GENERAL_ERROR
        )


def get_initiator_logical_address(rxbuf):
    """
    The initiator logical address is always the DPU, i.e. 0x51. The location of the initiator logical
    address is different for Request and RequestReply packets.
    """
    instruction = get_instruction_field(rxbuf)
    offset = 4 if is_command(instruction) else 0
    idx = offset + get_reply_address_field_length(rxbuf)
    ila_rxbuf = rxbuf[idx]
    return ila_rxbuf


def check_initiator_logical_address(rxbuf, ila):
    ila_rxbuf = get_initiator_logical_address(rxbuf)
    if ila != ila_rxbuf:
        raise CheckError(
            f"Initiator Logical Address doesn't match, ila=0x{ila:02X} & ila_rxbuf=0x"
            f"{ila_rxbuf:02X}",
            egse.rmap.RMAP_GENERAL_ERROR
        )


def get_transaction_identifier(rxbuf):
    idx = 5 + get_reply_address_field_length(rxbuf)
    tid = struct.unpack('>h', rxbuf[idx:idx + 2])[0]
    return tid


def check_key(rxbuf, key):
    from egse.rmap import RMAP_INVALID_KEY

    idx = 3
    key_rxbuf = rxbuf[idx]
    if key != key_rxbuf:
        raise CheckError(
            f"Key doesn't match, key={key} & key_rxbuf={key_rxbuf}", RMAP_INVALID_KEY
        )


# Functions to interpret the Instrument Field

def is_reserved(instruction):
    """
    The reserved bit of the 2-bit packet type field from the instruction field.

    For PLATO this bit shall be zero as the 0b10 and 0b11 packet field values are reserved.

    Returns:
        The bit value: 1 or 0.
    """
    return (instruction & 0b10000000) >> 7


def is_command(instruction):
    """Returns True if the RMAP packet is a command packet."""
    return (instruction & 0b01000000) >> 6


def is_reply(instruction):
    """Returns True if the RMAP packet is a reply to a previous command packet."""
    return not is_command(instruction)


def is_write(instruction):
    """Returns True if the RMAP packet is a write request command packet."""
    return (instruction & 0b00100000) >> 5


def is_read(instruction):
    """Returns True if the RMAP packet is a read request command packet."""
    return not is_write(instruction)


def is_verify(instruction):
    """Returns True if the RMAP packet needs to do a verify before write."""
    return (instruction & 0b00010000) >> 4


def is_reply_required(instruction):
    """Returns True if the reply bit is set in the instruction field.

    Args:
        instruction (int): the instruction field of an RMAP packet

    Note: the name of this function might be confusing.

        This function does **not** test if the packet is a reply packet, but it checks
        if the command requests a reply from the target. If you need to test if the
        packet is a command or a reply, use the is_command() or is_reply() function.

    """
    return (instruction & 0b00001000) >> 3


def is_increment(instruction):
    """Returns True if the data is written to sequential memory addresses."""
    return (instruction & 0b00000100) >> 2


def reply_address_length(instruction):
    """Returns the content of the reply address length field.

    The size of the reply address field is then decoded from the following table:

        Address Field Length  |  Size of Address Field
        ----------------------+-----------------------
             0b00             |      0 bytes
             0b01             |      4 bytes
             0b10             |      8 bytes
             0b11             |     12 bytes

    """
    return (instruction & 0b00000011) << 2
