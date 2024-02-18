"""
PyTest unit test for the `egse.spw` module.
"""
import numpy as np
import pytest

import egse
from egse.rmap import RMAP_NOT_IMPLEMENTED_AUTHORISED
from egse.spw import CheckError
from egse.spw import DataPacket
from egse.spw import DataPacketHeader
from egse.spw import DataPacketType
from egse.spw import HousekeepingPacket
from egse.rmap import RMAPError
from egse.spw import ReadRequest
from egse.spw import ReadRequestReply
from egse.spw import SpaceWirePacket
from egse.spw import TimecodePacket
from egse.rmap import check_address_and_data_length
from egse.rmap import create_rmap_read_request_packet
from egse.rmap import create_rmap_read_request_reply_packet
from egse.spw import check_instruction
from egse.spw import update_transaction_identifier
from egse.system import Timer
from egse.system import env_var

TIMECODE_PACKET = "0x91 0x42"  # Note timecode is [0-63] -> [0-0x3F]

EMPTY_PACKET = "0x50 0xf0 0x00 0x00 0x00 0x0e 0x01 0xd3 0x00 0x00"

FAKE_PACKET = (
    "0x50 0xF0 0x00 0x14 0x00 0x0E 0x01 0xD3 0x00 0x00 "
    "0x00 0x01 0x00 0x02 0x00 0x03 0x00 0x04 0x00 0x05 0x00 0x06 0x00 0x07 0x00 0x08 0x00 0x09 0x00 0x0A"
)

HK_DATA_1 = (
    "0x50 0xf0 0x00 0x90 0x00 0x0e 0x01 0xd3 0x00 0x00 0x80 0x00 0x80 0x00 0x80 0x00 0x80 0x00 0x80 0x00 0x80 0x00 "
    "0x7f 0xff 0x7f 0xff 0x7f 0xff 0x7f 0xff 0x7f 0xff 0x7f 0xff 0x7f 0xff 0x7f 0xff 0x7f 0xff 0x80 0x5f 0x80 0x5d "
    "0x80 0x5c 0x80 0x5c 0x80 0x5c 0x80 0x5c 0x80 0x5c 0x80 0x5c 0x80 0x5c 0x80 0x5c 0x80 0x5b 0x80 0x5c 0x80 0x5c "
    "0x46 0x6f 0x03 0x01 0xf1 0x01 0x80 0x58 0x20 0xa6 0x19 0x6c 0xe5 0x48 0x18 0x40 0xe5 0x6c 0x1a 0x24 0xe0 0x7d "
    "0x1a 0x7a 0x4b 0x43 0x41 0x76 0x05 0x41 0x04 0x4c 0x3e 0x72 0x0c 0x4c 0x0b 0xd9 0x82 0x67 0x80 0x5a 0x2b 0xe1 "
    "0x88 0x5d 0x80 0x58 0x2d 0x3c 0x88 0xcc 0x80 0x58 0x2d 0x28 0x88 0x70 0x80 0x58 0x2d 0x1d 0x88 0xfe 0x80 0x56 "
    "0x80 0x59 0x80 0x59 0x80 0x59 0x00 0x00 0x00 0x01 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0xff 0xff 0xff 0xff"
)

DATA_PACKET_DATA_1 = (
    "0x50 0xf0 0x01 0x56 0x01 0x00 0x01 0xd5 0x01 0xbd 0x03 0x00 0x03 0x01 0x03 0x02 0x03 0x03 0x03 0x04 0x03 0x05 "
    "0x03 0x06 0x03 0x07 0x03 0x08 0x03 0x09 0x03 0x0a 0x03 0x0b 0x03 0x0c 0x03 0x0d 0x03 0x0e 0x03 0x0f 0x03 0x10 "
    "0x03 0x11 0x03 0x12 0x03 0x13 0x03 0x14 0x03 0x15 0x03 0x16 0x03 0x17 0x03 0x18 0x03 0x19 0x03 0x1a 0x03 0x1b "
    "0x03 0x1c 0x03 0x1d 0x03 0x1e 0x03 0x1f 0x03 0x00 0x03 0x01 0x03 0x02 0x03 0x03 0x03 0x04 0x03 0x05 0x03 0x06 "
    "0x03 0x07 0x03 0x08 0x03 0x09 0x03 0x0a 0x03 0x0b 0x03 0x0c 0x03 0x0d 0x03 0x0e 0x03 0x0f 0x03 0x10 0x03 0x11 "
    "0x03 0x12 0x03 0x13 0x03 0x14 0x03 0x15 0x03 0x16 0x03 0x17 0x03 0x18 0x03 0x19 0x03 0x1a 0x03 0x1b 0x03 0x1c "
    "0x03 0x1d 0x03 0x1e 0x03 0x1f 0x03 0x00 0x03 0x01 0x03 0x02 0x03 0x03 0x03 0x04 0x03 0x05 0x03 0x06 0x03 0x07 "
    "0x03 0x08 0x03 0x09 0x03 0x0a 0x03 0x0b 0x03 0x0c 0x03 0x0d 0x03 0x0e 0x03 0x0f 0x03 0x10 0x03 0x11 0x03 0x12 "
    "0x03 0x13 0x03 0x14 0x03 0x15 0x03 0x16 0x03 0x17 0x03 0x18 0x03 0x19 0x03 0x1a 0x03 0x1b 0x03 0x1c 0x03 0x1d "
    "0x03 0x1e 0x03 0x1f 0x03 0x00 0x03 0x01 0x03 0x02 0x03 0x03 0x03 0x04 0x03 0x05 0x03 0x06 0x03 0x07 0x03 0x08 "
    "0x03 0x09 0x03 0x0a 0x03 0x0b 0x03 0x0c 0x03 0x0d 0x03 0x0e 0x03 0x0f 0x03 0x10 0x03 0x11 0x03 0x12 0x03 0x13 "
    "0x03 0x14 0x03 0x15 0x03 0x16 0x03 0x17 0x03 0x18 0x03 0x19 0x03 0x1a 0x03 0x1b 0x03 0x1c 0x03 0x1d 0x03 0x1e "
    "0x03 0x1f 0x03 0x00 0x03 0x01 0x03 0x02 0x03 0x03 0x03 0x04 0x03 0x05 0x03 0x06 0x03 0x07 0x03 0x08 0x03 0x09 "
    "0x03 0x0a 0x03 0x0b 0x03 0x0c 0x03 0x0d 0x03 0x0e 0x03 0x0f 0x03 0x10 0x03 0x11 0x03 0x12 0x03 0x13 0x03 0x14 "
    "0x03 0x15 0x03 0x16 0x03 0x17 0x03 0x18 0x03 0x19 0x03 0x1a 0x03 0x1b 0x03 0x1c 0x03 0x1d 0x03 0x1e 0x03 0x1f "
    "0x03 0x00 0x03 0x01 0x03 0x02 0x03 0x03 0x03 0x04 0x03 0x05 0x03 0x06 0x03 0x07 0x03 0x08 0x03 0x09 0x03 0x0a "
)


def deserialize_packet_data(line):
    """Converts the ascii representation of the packet into a numpy array."""
    return np.array([int(x, 16) for x in line.split()], dtype=np.uint8)


def test_factory_create():
    packet = deserialize_packet_data(HK_DATA_1)
    packet = SpaceWirePacket.create_packet(packet)

    assert isinstance(packet, SpaceWirePacket)
    assert isinstance(packet, HousekeepingPacket)

    packet = deserialize_packet_data(DATA_PACKET_DATA_1)
    packet = SpaceWirePacket.create_packet(packet)

    assert isinstance(packet, SpaceWirePacket)
    assert isinstance(packet, DataPacket)
    assert not isinstance(
        packet, HousekeepingPacket
    )  # because HousekeepingPacket is also a DataPacket

    packet = deserialize_packet_data(TIMECODE_PACKET)
    packet = SpaceWirePacket.create_packet(packet)

    assert isinstance(packet, SpaceWirePacket)
    assert isinstance(packet, TimecodePacket)


def test_str_of_packet():

    print()

    packet = deserialize_packet_data(HK_DATA_1)
    packet = SpaceWirePacket.create_packet(packet)

    print(packet)

    assert "Logical Address = 0x50" in str(packet)
    assert "Type = mode:ON_MODE, last_packet:False" in str(packet)
    assert "Data HEX = 80 00 80 00 80 00 80 00 80 00 80 00 7F" in str(packet)

    print()

    packet = deserialize_packet_data(DATA_PACKET_DATA_1)
    packet = SpaceWirePacket.create_packet(packet)

    print(packet)

    assert "Length = 342" in str(packet)
    assert "Frame Counter = 469" in str(packet)
    assert "Header = 50 F0 01 56 01 00 01 D5 01 BD" in str(packet)
    assert "Data HEX = 03 00 03 01 03 02 03 03 03" in str(packet)

    print()

    packet = deserialize_packet_data(TIMECODE_PACKET)
    packet = SpaceWirePacket.create_packet(packet)

    print(packet)

    assert "Timecode Packet: timecode = 0x02 ( 2)" == str(packet)


def test_data_packet_type_to_string():

    from egse.spw import to_string

    print()

    packet = deserialize_packet_data(DATA_PACKET_DATA_1)
    packet = SpaceWirePacket.create_packet(packet)

    print(to_string(packet))
    print(to_string(packet.header.as_dict()))

    print(packet.type)
    print(to_string(packet.type))

    x = to_string(packet.type)
    assert "mode:FULL_IMAGE_PATTERN_MODE" in x
    assert "last_packet:False" in x
    assert "CCD side:E" in x
    assert "CCD number:1" in x
    assert "Frame number:0" in x
    assert "Packet Type:DATA_PACKET" in x


def test_data_packet_type_construction_and_getters():

    data_packet_type = DataPacketType()
    assert data_packet_type.value == 0

    data_packet_type = DataPacketType(0b0000_0110_0101_1110)
    assert data_packet_type.value == 1630
    assert data_packet_type.packet_type == 2  # Housekeeping packet
    assert data_packet_type.frame_number == 3
    assert data_packet_type.ccd_number == 1
    assert data_packet_type.ccd_side == 1  # right, F-side
    assert data_packet_type.last_packet == 0
    assert data_packet_type.mode == 6  # Windowing mode


def test_data_packet_type_setters():

    data_packet_type = DataPacketType()

    data_packet_type.packet_type = 2  # Housekeeping packet
    data_packet_type.frame_number = 3
    data_packet_type.ccd_number = 1
    data_packet_type.ccd_side = 1  # right, F-side
    data_packet_type.last_packet = 0
    data_packet_type.mode = 6  # Windowing mode

    assert data_packet_type.value == 1630 == 0b0000_0110_0101_1110

    # Test if the setters is also implemented correctly when the value to set is 0

    data_packet_type = DataPacketType(0b11111111_11111111)

    data_packet_type.packet_type = 0
    assert data_packet_type.packet_type == 0
    data_packet_type.frame_number = 0
    assert data_packet_type.frame_number == 0
    data_packet_type.ccd_number = 0
    assert data_packet_type.ccd_number == 0
    data_packet_type.ccd_side = 0
    assert data_packet_type.ccd_side == 0
    data_packet_type.last_packet = 0
    assert data_packet_type.last_packet == 0
    data_packet_type.mode = 0
    assert data_packet_type.mode == 0


def test_data_packet_type_boundaries():
    data_packet_type = DataPacketType()

    with pytest.raises(ValueError):
        data_packet_type.packet_type = 3


def test_properties_of_hk_packet():
    packet = deserialize_packet_data(HK_DATA_1)
    packet = SpaceWirePacket.create_packet(packet)

    assert isinstance(packet, HousekeepingPacket)

    assert len(packet.packet_as_bytes) == 154
    assert packet.length == 144
    # length is in bytes, while the data_as_ndarray is 16-bit integer
    assert len(packet.data_as_ndarray) == packet.length // 2

    assert packet.logical_address == 0x50
    assert packet.protocol_id == 0xF0


def test_data_as_ndarray():

    packet = deserialize_packet_data(FAKE_PACKET)
    packet = SpaceWirePacket.create_packet(packet)

    assert isinstance(packet, HousekeepingPacket)
    assert all(
        x == y
        for x, y in zip(
            packet.data_as_ndarray, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        )
    )


def test_properties_of_timecode_packet():
    packet = deserialize_packet_data(TIMECODE_PACKET)
    packet: TimecodePacket = SpaceWirePacket.create_packet(packet)

    assert packet.timecode == 0x02  # data[1] & 0x3F

    assert "timecode" in str(packet)
    assert repr(packet).startswith("TimecodePacket")


def test_constraints_data_packet(caplog):

    print()

    # When you want to check on the exceptions, use:
    # print(f"{exc_info.value = }")

    # This constructor should raise a warning message

    with pytest.raises(ValueError, match="not consistent") as exc_info:
        packet = DataPacket(np.array([0x50, 0xF0, 2, 3, 4, 5, 6, 7, 8, 9]))  # data length: 0x0203 = 515
    print(f"{exc_info.value = }")

    assert "packet without data" in caplog.text

    caplog.clear()

    packet = DataPacket(np.array([0x50, 0xF0, 0x00, 0x00, 4, 5, 6, 7, 8, 9]))
    assert "packet without data" in caplog.text

    caplog.clear()

    # This should fail because there are five (5) bytes in the data area, but the data-length
    # field says 0x04.

    with pytest.raises(ValueError, match="not consistent") as exc_info:
        packet = DataPacket(
            np.array([0x50, 0xF0, 0x00, 0x04, 4, 5, 6, 7, 8, 9, 0xA, 0xB, 0xC, 0xD, 0x0E])
        )
    print(f"{exc_info.value = }")


def test_repr():
    data = deserialize_packet_data(HK_DATA_1)
    packet = HousekeepingPacket(data)

    assert "HousekeepingPacket" in repr(packet)

    # FIXME: change this code when sub-classes DataPacket are implemented, e.g. WindowingDataPacket.

    data = deserialize_packet_data(DATA_PACKET_DATA_1)
    packet = DataPacket(data)

    assert "DataPacket" in repr(packet)


def test_str():
    print()

    with Timer() as timer:
        data = deserialize_packet_data(HK_DATA_1)
        timer.log_elapsed()
        packet = HousekeepingPacket(data)
        timer.log_elapsed()

        # print(str(packet))
        assert "HousekeepingPacket" in str(packet)  # this takes all the time!
        timer.log_elapsed()

        # FIXME: change this code when sub-classes DataPacket are implemented, e.g. WindowingDataPacket.

        data = deserialize_packet_data(DATA_PACKET_DATA_1)
        timer.log_elapsed()
        packet = DataPacket(data)
        timer.log_elapsed()
        # print(str(packet))
        assert "DataPacket" in str(packet)
        timer.log_elapsed()


def test_data_packet_header():

    header = DataPacketHeader()

    header.packet_type


def test_create_read_request_packet():

    data = create_rmap_read_request_packet(0x000, 4, 41)

    packet: ReadRequest = SpaceWirePacket.create_packet(data)

    assert isinstance(packet, ReadRequest)
    assert packet.logical_address == 0x51
    assert packet.protocol_id == 0x01
    assert packet.data_length == 4
    assert packet.instruction == 0x4C
    assert packet.transaction_id == 42  # transaction ID shall be incremented with every RMAP request

    assert "Transaction ID" in str(packet)


def test_create_rmap_read_request_reply_packet():

    data = create_rmap_read_request_reply_packet(0x4C, 23, 0, b'\x01\x02\x03\x04\x05', 5)

    packet: ReadRequest = SpaceWirePacket.create_packet(data)

    assert isinstance(packet, ReadRequestReply)
    assert packet.logical_address == 0x50
    assert packet.protocol_id == 0x01
    assert packet.data_length == 5
    assert packet.data == b'\x01\x02\x03\x04\x05'
    assert packet.instruction == 0x0C
    assert packet.transaction_id == 23

    assert "Reply" in str(packet)


def test_update_transaction_identifier():

    tid = update_transaction_identifier(0)

    assert tid == 1
    assert (tid := update_transaction_identifier(tid)) == 2
    assert (tid := update_transaction_identifier(tid)) == 3

    assert (tid := update_transaction_identifier(0xFFFE)) == 0xFFFF
    assert (tid := update_transaction_identifier(tid)) == 0x0000
    assert (tid := update_transaction_identifier(tid)) == 0x0001

    assert update_transaction_identifier(65536) == 1
    assert update_transaction_identifier(65537) == 2


def test_check_data_length(caplog):

    print()

    # When you want to check on the exceptions, use:
    # print(f"{exc_info.value = }")

    with pytest.raises(RMAPError,
                       match="The requested data length shall be a multiple of 4 bytes.") as exc_info:
        assert check_address_and_data_length(0x0000_0000, 3)
    print(f"{exc_info.value = }")

    with pytest.raises(RMAPError,
                       match="The address shall be a multiple of 4 bytes.") as exc_info:
        assert check_address_and_data_length(0x0000_0001, 4)
    print(f"{exc_info.value = }")

    # Tests for critical area

    with pytest.raises(
            RMAPError,
            match="Read requests to the critical area have a fixed data length of 4 bytes."):
        assert check_address_and_data_length(0x0000_0000, 0)

    with pytest.raises(
            RMAPError,
            match="Read requests to the critical area have a fixed data length of 4 bytes."):
        assert check_address_and_data_length(0x0000_0010, 12)

    assert check_address_and_data_length(0x0000_0004, 4) is None
    assert check_address_and_data_length(0x0000_00FC, 4) is None

    # Tests for general area

    assert check_address_and_data_length(0x0000_0100,  12) is None
    assert check_address_and_data_length(0x0000_01F0,  20) is None

    with pytest.raises(
            RMAPError,
            match="Read requests to the general area have a maximum data length of 256 bytes."):
        assert check_address_and_data_length(0x0000_01F0, 300)

    assert check_address_and_data_length(0x0000_06FC, 4) is None
    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0000_06FC, 8)
    assert "The address + length exceeds the general area boundaries" in exc_info.value.args[0]

    # Tests for housekeeping area

    assert check_address_and_data_length(0x0000_0700,  12) is None
    assert check_address_and_data_length(0x0000_07AC,  20) is None
    with pytest.raises(
            RMAPError,
            match="Read requests to the housekeeping area have a maximum data length of 256 bytes."):
        assert check_address_and_data_length(0x0000_07FC, 260) is None

    assert check_address_and_data_length(0x0000_07FC, 4) is None
    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0000_07FC, 8) is None
    assert "The address + length exceeds the housekeeping area boundaries." in exc_info.value.args[0]

    # Tests for windowing area

    assert check_address_and_data_length(0x0080_0000, 12) is None
    assert check_address_and_data_length(0x0090_0000, 20) is None
    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0090_0000, 5000) is None

    assert check_address_and_data_length(0x00FF_FFFC, 4) is None
    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x00FF_FFFC, 8) is None

    # Tests out of any area

    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0FFF_0000, 4) is None
    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0000_1000, 4) is None
    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0011_0000, 4) is None

    # Test relaxing the rules

    caplog.clear()

    # Reset the warning count on this function, otherwise the log message might not contain the expected string.
    check_address_and_data_length.warning_count = 0

    assert check_address_and_data_length(0, 3, strict=False) is None
    assert "Address and data length checks have been disabled" in caplog.text

    caplog.clear()


def test_twos_complement_offset(caplog):

    import egse

    from egse.reload import reload_module
    from egse.spw import TWOS_COMPLEMENT_OFFSET
    assert TWOS_COMPLEMENT_OFFSET == 0

    with env_var(PLATO_CAMERA_IS_EM="True"):
        reload_module(egse.spw)

        from egse.spw import TWOS_COMPLEMENT_OFFSET
        assert TWOS_COMPLEMENT_OFFSET == 32768

        assert "WARNING" in caplog.text
        assert "PLATO_CAMERA_IS_EM environment variable is defined" in caplog.text


def test_check_instruction():

    print()

    with pytest.raises(egse.spw.CheckError, match="reserved") as exc_info:
        check_instruction(b'\xFF\xFF\xFF\xFF')

    # print(f"{exc_info=}, {exc_info.value=}, {type(exc_info.value)=}")

    assert "reserved bit is not 0x00" in exc_info.value.message
    assert exc_info.value.status == RMAP_NOT_IMPLEMENTED_AUTHORISED

    check_instruction(b'\x00\x00\x7F')
