"""
Unit Tests for the RMAP module.
"""

import pytest

from egse.rmap import RMAPError
from egse.rmap import check_address_and_data_length
from egse.rmap import create_rmap_read_request_packet
from egse.rmap import create_rmap_read_request_reply_packet
from egse.rmap import create_rmap_unverified_write_packet
from egse.rmap import create_rmap_verified_write_packet
from egse.rmap import create_rmap_write_request_reply_packet
from egse.settings import Settings
from egse.spw import SpaceWirePacket
from egse.spw import check_data_crc
from egse.spw import check_header_crc
from egse.spw import get_address
from egse.spw import get_data
from egse.spw import get_data_length
from egse.spw import get_initiator_logical_address
from egse.spw import get_instruction_field
from egse.spw import get_key_field
from egse.spw import get_reply_address_field_length
from egse.spw import get_target_logical_address
from egse.spw import get_transaction_identifier
from egse.spw import is_read
from egse.spw import is_reply
from egse.system import ping

dsi_settings = Settings.load("DSI")

dsi_available = True if ping(dsi_settings.DSI_DPU_IP_ADDRESS) else False


def test_check_data_length():

    print()

    # When you want to check on the exceptions, use:
    # print(exc_info.value)

    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0000_0000, 3)
    print(exc_info.value)

    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0000_0001, 4)
    print(exc_info.value)

    # Tests for critical area

    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0000_0000, 0)
    print(exc_info.value)

    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0000_0010, 12)
    print(exc_info.value)

    assert check_address_and_data_length(0x0000_0004, 4) is None
    assert check_address_and_data_length(0x0000_00FC, 4) is None

    # Tests for general area

    assert check_address_and_data_length(0x0000_0100,  12) is None
    assert check_address_and_data_length(0x0000_01F0,  20) is None

    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0000_01F0, 300)
    print(exc_info.value)

    assert check_address_and_data_length(0x0000_06FC, 4) is None
    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0000_06FC, 8)
    print(exc_info.value)

    # Tests for housekeeping area

    assert check_address_and_data_length(0x0000_0700,  12) is None
    assert check_address_and_data_length(0x0000_07AC,  20) is None
    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0000_07FC, 260) is None
    print(exc_info.value)

    assert check_address_and_data_length(0x0000_07FC, 4) is None
    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0000_07FC, 8) is None
    print(exc_info.value)

    # Tests for windowing area

    assert check_address_and_data_length(0x0080_0000, 12) is None
    assert check_address_and_data_length(0x0090_0000, 20) is None
    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0090_0000, 5000) is None
    print(exc_info.value)

    assert check_address_and_data_length(0x00FF_FFFC, 4) is None
    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x00FF_FFFC, 8) is None
    print(exc_info.value)

    # Tests out of any area

    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0FFF_0000, 4) is None
    print(exc_info.value)
    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0000_1000, 4) is None
    print(exc_info.value)
    with pytest.raises(RMAPError) as exc_info:
        assert check_address_and_data_length(0x0011_0000, 4) is None
    print(exc_info.value)


def test_create_read_request():

    print()

    packet = create_rmap_read_request_packet(0x0000_0024, length=4, tid=17, strict=True)

    assert get_address(packet) == 0x24

    instruction_field = get_instruction_field(packet)
    assert is_read(instruction_field)
    assert not is_reply(instruction_field)

    with pytest.raises(ValueError) as exc_info:
        assert int.from_bytes(get_data(packet), 'big') == 0x0101_0101
    print(exc_info.value)

    assert get_data_length(packet) == 4

    check_header_crc(packet)

    print()
    print(SpaceWirePacket.create_packet(packet))


def test_create_read_request_with_wrong_arguments(caplog):

    print()

    with pytest.raises(RMAPError) as exc_info:
        _ = create_rmap_read_request_packet(0x0000_0047, length=4, tid=17, strict=True)
    assert "The address shall be a multiple of 4 bytes." in exc_info.value.args

    with pytest.raises(RMAPError) as exc_info:
        _ = create_rmap_read_request_packet(0x0000_0048, length=6, tid=17, strict=True)
    assert "The requested data length shall be a multiple of 4 bytes." in exc_info.value.args

    with pytest.raises(RMAPError) as exc_info:
        _ = create_rmap_read_request_packet(0x0000_0048, length=8, tid=17, strict=True)
    print(exc_info.value.args)
    assert "Read requests to the critical area have a fixed data length of 4 bytes." in exc_info.value.args

    caplog.clear()

    # Reset the warning count on this function, otherwise the log message might not contain the expected string.
    check_address_and_data_length.warning_count = 0

    packet = create_rmap_read_request_packet(0x0000_0000, length=8, tid=17, strict=False)
    assert "Address and data length checks have been disabled" in caplog.text

    packet = create_rmap_read_request_packet(0x0000_0048, length=6, tid=17, strict=False)

    assert check_header_crc(packet) is None
    assert get_address(packet) == 0x0048
    assert get_data_length(packet) == 6
    assert get_transaction_identifier(packet) == 18  # is incremented before creation
    assert get_target_logical_address(packet) == 0x51
    assert SpaceWirePacket.create_packet(packet).logical_address == 0x51
    assert get_initiator_logical_address(packet) == 0x50
    assert SpaceWirePacket.create_packet(packet).initiator_address == 0x50

    assert get_reply_address_field_length(packet) == 0
    assert get_key_field(packet) == 0xD1


def test_create_read_request_reply():

    packet = create_rmap_read_request_packet(0x0000_0024, 4, 17, strict=True)
    reply_packet = create_rmap_read_request_reply_packet(
        get_instruction_field(packet), get_transaction_identifier(packet), 3, b'abcd', 4
    )

    assert int.from_bytes(get_data(reply_packet), 'big') == 0x61_62_63_64
    assert get_transaction_identifier(packet) == get_transaction_identifier(reply_packet) == 18
    assert get_instruction_field(packet) & 0b0100_0000
    assert not get_instruction_field(reply_packet) & 0b0100_0000
    assert get_initiator_logical_address(reply_packet) == 0x50
    assert SpaceWirePacket.create_packet(reply_packet).logical_address == 0x50
    assert get_target_logical_address(reply_packet) == 0x51
    assert SpaceWirePacket.create_packet(reply_packet).target_address == 0x51

    assert SpaceWirePacket.create_packet(reply_packet).status == 3

    check_header_crc(reply_packet)
    check_data_crc(reply_packet)

    print()
    print(SpaceWirePacket.create_packet(packet))
    print(SpaceWirePacket.create_packet(reply_packet))


def test_create_verified_write_request():

    packet = create_rmap_verified_write_packet(
        0x0000_0042, int.to_bytes(0x0101_0101, 4, byteorder='big'), tid=42
    )

    assert get_address(packet) == 0x42
    assert int.from_bytes(get_data(packet), 'big') == 0x0101_0101
    assert get_data_length(packet) == 4
    assert get_initiator_logical_address(packet) == 0x50
    assert SpaceWirePacket.create_packet(packet).initiator_address == 0x50
    assert get_target_logical_address(packet) == 0x51
    assert SpaceWirePacket.create_packet(packet).logical_address == 0x51

    check_header_crc(packet)
    check_data_crc(packet)

    print()
    print(SpaceWirePacket.create_packet(packet))


def test_create_unverified_write_request():

    buffer = b'abcdefghijklmnopqrstuvwxyz'

    packet = create_rmap_unverified_write_packet(0x0000_0142, buffer, len(buffer), tid=23)

    print()
    print(SpaceWirePacket.create_packet(packet))

    assert get_address(packet) == 0x142
    assert get_data(packet) == buffer
    assert get_data_length(packet) == 26

    check_header_crc(packet)
    check_data_crc(packet)


def test_create_write_request_reply():
    buffer = b'abcdefghijklmnopqrstuvwxyz'
    packet = create_rmap_unverified_write_packet(0x0000_0142, buffer, len(buffer), tid=23)
    reply_packet = create_rmap_write_request_reply_packet(get_instruction_field(packet), tid=23, status=5)

    print()
    print(SpaceWirePacket.create_packet(packet))
    print(SpaceWirePacket.create_packet(reply_packet))
