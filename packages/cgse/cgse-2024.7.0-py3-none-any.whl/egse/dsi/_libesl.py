import logging
from ctypes import POINTER
from ctypes import Structure
from ctypes import c_char_p
from ctypes import c_int
from ctypes import c_size_t
from ctypes import c_ssize_t
from ctypes import c_uint32
from ctypes import c_uint64
from ctypes import c_uint8
from ctypes import c_void_p
from ctypes import c_void_p as c_int_p
from ctypes import cdll
from pathlib import Path

from egse.config import find_file
from egse.settings import Settings
from egse.system import get_os_name
from egse.system import get_os_version
from egse.system import get_system_architecture

logger = logging.getLogger(__name__)

dsi_settings = Settings.load("DSI")

HERE = Path(__file__).parent

# Depending on the OS, and the OS version, we load the dynamic library from a specific location
# Only some OS/OS-version combinations are supported.
if get_os_name() == 'macos':
    if get_system_architecture() == 'arm64':
        in_dir = 'macOS/arm64'
    else:
        in_dir = 'macOS/x86_64'
elif get_os_name() == 'debian':
    in_dir = 'Debian'
elif get_os_name() == 'centos':
    in_dir = 'CentOS-7' if get_os_version().startswith('7') else 'CentOS-8'
elif get_os_name() == 'ubuntu':
    in_dir = 'Ubuntu-20' if get_os_version().startswith('20') else 'Linux'
else:
    in_dir = None

dylib_filename = Path(dsi_settings.ESL_DYLIB_FILENAME)

logger.debug(f"Locating shared library {dylib_filename} in dir '{in_dir}'")

# Assuming the shared libraries are delivered with the source in 'egse.lib'

shared_libs_root = HERE.parent / 'lib'

dylib_filename = find_file(str(dylib_filename), root=shared_libs_root, in_dir=in_dir)

logger.debug(f"Loading shared library: {dylib_filename}")

if not dylib_filename:
    raise FileNotFoundError(f"Could not find dynamic library: {dylib_filename}")

libesl = cdll.LoadLibrary(str(dylib_filename)) # noqa


class ESL(Structure):
    _fields_ = [
        ("sock", c_int),
        ("tx_buffer", c_char_p),
        ("tx_buffer_length", c_size_t),
        ("tx_buffer_content", c_size_t),
        ("rx_buffer", c_char_p),
        ("rx_buffer_length", c_size_t),
        ("rx_buffer_content", c_ssize_t),
        ("rx_buffer_ptr", c_int),
        ("rx_state", c_int),
        ("rx_count", c_int),
        ("rx_param", c_int),
        ("rx_timeout", c_int),
        ("rx_final_flags", c_int),
        ("extn_count", c_int),
        ("extn_size", c_int),
        ("extn_cmd", c_int),
        ("extn_byte", c_int),
        ("extn_link", c_int),
        ("cmd_buffer", c_char_p),
        ("time_buffer", c_char_p),

        ("special_cb", c_void_p),
        ("extension_cb", c_void_p),

        ("number_of_links", c_int),
        ("number_of_slots", c_int),
        ("slot_content", c_int_p),
        ("record_file", c_void_p),
        ("log_file", c_void_p),
        ("max_length", c_int),
        ("log_rx_port", c_int),
        ("log_tx_port", c_int),

        ("ram_io", c_int),
        ("current_port", c_int),

        ("check_record_writes", c_int),
        ("total_raw_bytes_received", c_uint64),

        ("options", c_char_p),
        ("option", c_int),
        ("ESL_error_errno", c_int),

        ("rx_timeout_returns_error", c_int),

        ("max_dumps", c_uint32),
        ("context", c_void_p),

        ("rxinfo", c_uint32),

        ("read_calls", c_uint64),
        ("read_io_calls", c_uint64),
        ("file", c_int),
        ("filesize", c_uint64),
        ("recordsize", c_uint64),

        ("ram_io_int", c_int),

        ("eintr_enabled", c_int),
        ("timezero", c_size_t),
        ("timedata", c_uint64),
        ("timedata_ns", c_uint32),

        ("partialframesz", c_size_t),
        ("partialframe_offset", c_size_t),
        ("system_type", c_int),
        ("auto_flush", c_int),
        ("live", c_int),

        ("epollfd", c_int),
    ]


esl_p = POINTER(ESL)

libesl_get_version = libesl.EtherSpaceLink_get_version
libesl_get_version.argtypes = []
libesl_get_version.restype = c_char_p

libesl_open = libesl.EtherSpaceLink_open
libesl_open.argtypes = [c_char_p]
libesl_open.restype = esl_p

libesl_close = libesl.EtherSpaceLink_close
libesl_close.argtypes = [esl_p]

libesl_flush = libesl.EtherSpaceLink_flush
libesl_flush.argtypes = [esl_p]

libesl_shutdown = libesl.EtherSpaceLink_shutdown
libesl_shutdown.argtypes = [esl_p]

libesl_link_connected = libesl.EtherSpaceLink_link_connected
libesl_link_connected.argtypes = [esl_p]
libesl_link_connected.restype = c_int

libesl_set_active_link = libesl.EtherSpaceLink_set_active_link
libesl_set_active_link.argtypes = [esl_p, c_int]
libesl_set_active_link.restype = c_int

libesl_set_speed = libesl.EtherSpaceLink_set_speed
libesl_set_speed.argtypes = [esl_p, c_int]
libesl_set_speed.restype = c_int

libesl_set_mode = libesl.EtherSpaceLink_set_mode
libesl_set_mode.argtypes = [esl_p, c_int]
libesl_set_mode.restype = c_int

libesl_send_timecode = libesl.EtherSpaceLink_send_timecode
libesl_set_mode.argtypes = [esl_p, c_uint8]
libesl_set_mode.restype = c_int

libesl_set_rx_timeout = libesl.EtherSpaceLink_set_rx_timeout
libesl_set_rx_timeout.argtypes = [esl_p, c_int]

libesl_set_rx_timeout_action = libesl.EtherSpaceLink_set_rx_timeout_action
libesl_set_rx_timeout_action.argtypes = [esl_p, c_int]

libesl_set_log_file = libesl.EtherSpaceLink_set_log_file
libesl_set_log_file.argtypes = [esl_p, c_char_p]
libesl_set_log_file.restype = c_int

libesl_set_record_file = libesl.EtherSpaceLink_set_record_file
libesl_set_record_file.argtypes = [esl_p, c_char_p]
libesl_set_record_file.restype = c_int

libesl_request_link_status = libesl.EtherSpaceLink_request_link_status
libesl_request_link_status.argtypes = [esl_p]
libesl_request_link_status.restype = c_int

libesl_get_receive_speed = libesl.EtherSpaceLink_get_receive_speed
libesl_get_receive_speed.argtypes = [esl_p]
libesl_get_receive_speed.restype = c_int

libesl_get_esl_error = libesl.EtherSpaceLink_get_error
libesl_get_esl_error.argtypes = [esl_p]
libesl_get_esl_error.restype = c_int

libesl_get_number_of_links = libesl.EtherSpaceLink_get_number_of_links
libesl_get_number_of_links.argtypes = [esl_p]
libesl_get_number_of_links.restype = c_int

libesl_get_manufacturer_string = libesl.EtherSpaceLink_get_manufacturer_string
libesl_get_manufacturer_string.argtypes = [esl_p]
libesl_get_manufacturer_string.restype = c_char_p

libesl_get_product_string = libesl.EtherSpaceLink_get_product_string
libesl_get_product_string.argtypes = [esl_p]
libesl_get_product_string.restype = c_char_p

libesl_get_hwa = libesl.EtherSpaceLink_get_HWA
libesl_get_hwa.argtypes = [esl_p, c_char_p]
libesl_get_hwa.restype = c_int

libesl_hwa_to_serial_number_string = libesl.EtherSpaceLink_HWA_to_serial_number_string
libesl_hwa_to_serial_number_string.argtypes = [c_char_p]
libesl_hwa_to_serial_number_string.restype = c_char_p

libesl_read_packet_full = libesl.EtherSpaceLink_read_packet_full
libesl_read_packet_full.argtypes = [esl_p, c_void_p, c_int, c_int_p, c_int]
libesl_read_packet_full.restype = c_int

libesl_write_packet = libesl.EtherSpaceLink_write_packet
libesl_write_packet.argtypes = [esl_p, c_void_p, c_size_t, c_uint32]
libesl_write_packet.restype = c_int

libesl_er_enable_reporting = libesl.EtherSpaceLink_ER_enable_reporting
libesl_er_enable_reporting.argtypes = [esl_p, c_int]
libesl_er_enable_reporting.restype = c_int
