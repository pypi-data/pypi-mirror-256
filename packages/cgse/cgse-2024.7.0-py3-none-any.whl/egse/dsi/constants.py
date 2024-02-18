"""
This module defines constants in a dictionary (k,v) with 'k' the constant value
and 'v' the constant name. This dict is then inverted into a dictionary (k,v)
where 'k' is now the constant name and 'v' is the constant value.

After that the constant names are defined in the current namespace using setattr().

## Why do we do this?

This way we can just use the ALL_UPPER_CASE constant names in our code, but at
the same time we can decode the values into the constant name for debugging etc.

A few examples to make this clear:

``` python
some_function([10, 20, 30, 40, 50], constants.ESL_EOP)

logger.debug(f"We received an error code {constants.esl_error_codes[err]} [{err}]")
```
The following codes are set up with this two-way construct:

* Terminator Codes
* Extension Codes
* ESL Error Codes
* ESL subsidiary API Error Codes
* RMAP Error Codes


"""
import logging
import sys

logger = logging.getLogger(__name__)

module = sys.modules[__name__]

__all__ = [
    'esl_api_error_codes',
    'esl_error_codes',
    'esl_extension_codes',
    'esl_link_mode',
    'esl_rmap_error_codes',
    'esl_terminator_codes',
]

# ESL Error Codes and Constants --------------------------------------------------------------------

# DSI event bits

ESL_DSI_EEP                   = 0x800000
ESL_DSI_NCHAR                 = 0x400000
ESL_DSI_FIRST_NULL            = 0x200000
ESL_DSI_EXCESS_FCT            = 0x100000
ESL_DSI_EXCESS_DATA           = 0x080000
ESL_DSI_FIRST_BYTE            = 0x040000
ESL_DSI_MID_BYTES             = 0x020000
ESL_DSI_EOP                   = 0x010000
ESL_DSI_TIME_CODE             = 0x008000
ESL_DSI_FCT                   = 0x004000
ESL_DSI_NULL                  = 0x002000
ESL_DSI_PARITY_ERROR          = 0x001000
ESL_DSI_ESC_EOP               = 0x000800
ESL_DSI_ESC_EEP               = 0x000400
ESL_DSI_ESC_ESC               = 0x000200
ESL_DSI_TIMEOUT               = 0x000100

# Link control and status

ESL_LINK_MODE_DISABLED        = 0x01
ESL_LINK_MODE_NORMAL          = 0x02
ESL_LINK_MODE_LEGACY          = 0x04
ESL_LINK_MODE_MASTER          = 0x06

esl_link_mode = {
    0x01: "DISABLED",
    0x02: "NORMAL",
    0x04: "LEGACY",
    0x06: "MASTER"
}

# Error Reporting

ESL_ER_REPORT_PARITY_ERROR    = ESL_DSI_PARITY_ERROR
ESL_ER_REPORT_TIME_CODE       = 0x80 | ESL_DSI_TIME_CODE
ESL_ER_REPORT_ESC_EOP         = ESL_DSI_ESC_EOP
ESL_ER_REPORT_ESC_EEP         = ESL_DSI_ESC_EEP
ESL_ER_REPORT_ESC_ESC         = ESL_DSI_ESC_ESC
ESL_ER_REPORT_TIMEOUT         = ESL_DSI_TIMEOUT

# Flags for Read Packet Full

ESL_DISCARD_SPECIAL_DATA      = 0x00
ESL_REPORT_SPECIAL_DATA       = 0x01
ESL_RETURN_SPECIAL_DATA       = 0x02
ESL_CALLBACK_SPECIAL_DATA     = 0x03
ESL_DISCARD_EXTENSION_DATA    = 0x00
ESL_REPORT_EXTENSION_DATA     = 0x10
ESL_RETURN_EXTENSION_DATA     = 0x20
ESL_CALLBACK_EXTENSION_DATA   = 0x30

# Terminators for read and write packet

esl_terminator_codes = {
    1000 : 'ESL_PART_EOP_EEP',
    1003 : 'ESL_SPECIAL',
    1004 : 'ESL_PART_SPECIAL',
    1005 : 'ESL_EXTN',
    1006 : 'ESL_PART_EXTN',
}

esl_terminator_names = dict([(v, k) for k, v in esl_terminator_codes.items()])

for name, value in esl_terminator_names.items():
    try:
        getattr(module, name)
        logger.error(f"module {__name__} is trying to overwrite the constant {name} with a new value.")
    except AttributeError:
        setattr(module, name, value)

del esl_terminator_names

# Define the ESL Extension Codes

esl_extension_codes = {
    0x100: 'ESL_FCT',
    0x101: 'ESL_EEP',
    0x102: 'ESL_EOP',
    0x103: 'ESL_ESC',
    0x104: 'ESL_ESC_FCT',
    0x105: 'ESL_ESC_EEP',
    0x106: 'ESL_ESC_EOP',
    0x107: 'ESL_ESC_ESC',
    0x108: 'ESL_TIMEOUT',
    0x109: 'ESL_PARITYERROR',
    0x10A: 'ESL_PERROR1',
    0x10B: 'ESL_PERROR2',
    0x10C: 'ESL_STORE',
    0x10D: 'ESL_FORWARD',
    0x10E: 'ESL_ATOM',
    0x10F: 'ESL_MOTA',
    0x110: 'ESL_JOIN',
    0x111: 'ESL_BARRIER',
    0x112: 'ESL_RESIGN',
    0x113: 'ESL_EVENT',
    0x12F: 'ESL_HOLD',
    0x130: 'ESL_DELAY',
    0x140: 'ESL_PORTSELECT',
    0x17F: 'ESL_PORTSELECT_MAX',
    0x188: 'ESL_TIMETAG',
    0x182: 'ESL_TIMETAG_DELTA',
    0x191: 'ESL_TIMECODE',
    0x1A1: 'ESL_TRUNCATE_1',
    0x1A2: 'ESL_TRUNCATE_2',
    0x1B1: 'ESL_REPEAT_1',
    0x1B2: 'ESL_REPEAT_2',
    0x1B3: 'ESL_REPEAT_3',
    0x1C8: 'ESL_YEAR'
}

esl_extension_names = dict([(v, k) for k, v in esl_extension_codes.items()])

for name, value in esl_extension_names.items():
    try:
        getattr(module, name)
        logger.error(f"module {__name__} is trying to overwrite the constant {name} with a new value.")
    except AttributeError:
        setattr(module, name, value)

del esl_extension_names

# Define the ESL Error Codes

esl_error_codes = {
    1:   'ESL_ERROR_RECFILE_OPEN',
    2:   'ESL_ERROR_RECFILE_WRITE',
    3:   'ESL_ERROR_LOGFILE_OPEN',
    4:   'ESL_ERROR_LOGFILE_WRITE',
    10:  'ESL_ERROR_TIMEOUT',
    980: 'ESL_ERROR_SET_SPEED',
    989: 'ESL_ERROR_RECEIVER_SHUTDOWN',
    998: 'ESL_ERROR_FLUSH_SEND_BUFFER',
    999: 'ESL_ERROR_BUFFER_OVERFLOW'
}

esl_error_names = dict([(v, k) for k, v in esl_error_codes.items()])

for name, value in esl_error_names.items():
    try:
        getattr(module, name)
        logger.error(f"module {__name__} is trying to overwrite the constant {name} with a new value.")
    except AttributeError:
        setattr(module, name, value)

del esl_error_names

# Define subsidiary ESL API error codes

esl_api_error_codes = {
    -1: "ESL_API_ERROR_RECFILE_OPEN",              # Couldn't open recording file
    -2: "ESL_API_ERROR_RECFILE_WRITE",             # record_file write failed
    -3: "ESL_API_ERROR_LOGFILE_OPEN",              # Couldn't open logging file
    -4: "ESL_API_ERROR_LOGFILE_WRITE",             # log_file write failed
   -10: "ESL_API_ERROR_RECEIVER_TIMEOUT",          # we have a network timeout
   -11: "ESL_API_ERROR_RECEIVER_SHUTDOWN",         # peer has performed an orderly shutdown
   -12: "ESL_API_ERROR_IO_ERROR",                  # we have an IO error
   -15: "ESL_API_ERROR_SAVEBUF_OVERFLOW_SAVE",     # Saving the read_packet_full() save_buffer failed
   -16: "ESL_API_ERROR_SAVEBUF_OVERFLOW_RESTORE",  # Restoring the read_packet_full() save_buffer failed
   -17: "ESL_API_ERROR_FUNCTION_NOT_SUPPORTED",    # Device does not support the requested function
   -18: "ESL_API_NETWORK",                         # Error reading / writing to/from the device
   -19: "ESL_API_NETWORK_FORMAT_ERROR",            # Error understanding received packet
   -20: "ESL_API_REQUEST_TOO_LARGE",               # The I/O request can't be fulfilled by the hardware
   -21: "ESL_API_SEQUENCE_ERROR",                  # Didn't receive expected notification from the hardware
   -22: "ESL_API_RESPONSE_TOO_SMALL",              # Response from the device didn't contain enough data
   -23: "ESL_API_RESPONSE_MISMATCH",               # Response does not match I/O request
   -24: "ESL_API_MODULE_NOT_PRESENT",              # Module not present
   -25: "ESL_API_PARAMETER_RANGE_INCORRECT",       # Parameter not in range
   -26: "ESL_API_FILE_NOT_PRESENT",                # Requested file is not present
   -27: "ESL_API_EINTR",                           # EINTR occurred
   -28: "ESL_API_LINK_INCORRECT",                  # Link number is incorrect
   -29: "ESL_API_INCORRECT_DEVICE",                # Connecting to a device which does not support functionality
   -30: "ESL_API_MEMORY",                          # Unable to allocate memory
   -31: "ESL_API_HOST_UNRESOLVABLE",               # Unable to resolve host
   -32: "ESL_API_HOST_UNRESPONSIVE",               # Unable to connect to host
   -33: "ESL_API_WAVEFORM_DIR_CREATE",             # Unable to create waveform directory
   -34: "ESL_API_ZERO_READ",                       # asked to read zero bytes
   -35: "ESL_API_SET_OPTION_FILE",                 # Asked to set an option when playing back from file
   -36: "ESL_API_INVALID_DEVICE",                  # Device is not supported by API
   -37: "ESL_API_FILE_MOVE",                       # Unable to move file into place
   -38: "ESL_API_INVALID_FILE",                    # Unable to open file
   -39: "ESL_API_CALLBACK_RETURN",                 # Callback has asked for a return
   -40: "ESL_API_FILELIST_EMPTY",                  # List of files given is empty
   -41: "ESL_API_UNKNOWN_SYSTEM_TYPE",             # Unknown type
   -42: "ESL_API_NOT_KNOWN",                       # API returned 0 as an error should (should not happen)
   -43: "ESL_API_EXE_START_FAILED",                # Cannot start executable
   -44: "ESL_API_NO_CONNECTION",                   # Link Not established
   -45: "ESL_API_INVALID_LINK",                    # Invalid Link selected
}

esl_api_error_codes_names = dict([(v, k) for k, v in esl_api_error_codes.items()])

for name, value in esl_api_error_codes_names.items():
    try:
        if getattr(module, name) != value:
            logger.error(f"module {__name__} is trying to overwrite the constant {name} with a new value {value}.")
    except AttributeError:
        setattr(module, name, value)

del esl_api_error_codes_names

# RMAP Error Codes and Constants -------------------------------------------------------------------

RMAP_PROTOCOL_ID                    = 0x01
RMAP_TARGET_LOGICAL_ADDRESS_DEFAULT = 0xFE
RMAP_TARGET_KEY                     = 0xD1

# Error and Status Codes

RMAP_SUCCESS                        = 0
RMAP_GENERAL_ERROR                  = 1
RMAP_UNUSED_PACKET_TYPE_COMMAND_CODE= 2
RMAP_INVALID_KEY                    = 3
RMAP_INVALID_DATA_CRC               = 4
RMAP_EARLY_EOP                      = 5
RMAP_TOO_MUCH_DATA                  = 6
RMAP_EEP                            = 7
RMAP_RESERVED                       = 8
RMAP_VERIFY_BUFFER_OVERRUN          = 9
RMAP_NOT_IMPLEMENTED_AUTHORISED     = 10
RMAP_RMW_DATA_LENGTH_ERROR          = 11
RMAP_INVALID_TARGET_LOGICAL_ADDRESS = 12

# These codes are ESL-RMAP specific errors

esl_rmap_error_codes = {
    2000: 'ESL_RMAP_ERROR_READ',
    2001: 'ESL_RMAP_ERROR_TIMEOUT',
    2002: 'ESL_RMAP_ERROR_READ_HDR_TOO_SHORT',
    2003: 'ESL_RMAP_ERROR_READ_ILA_INCORRECT',
    2004: 'ESL_RMAP_ERROR_READ_PID_NOT_RMAP',
    2005: 'ESL_RMAP_ERROR_READ_INSTN_NOT_READ_RESP',
    2006: 'ESL_RMAP_ERROR_READ_STATUS_NONZERO',
    2100: 'ESL_RMAP_ERROR_WRITE',
    2103: 'ESL_RMAP_ERROR_WRITE_ILA_INCORRECT',
    2106: 'ESL_RMAP_ERROR_WRITE_STATUS_NONZERO',
}

esl_rmap_error_names = dict([(v, k) for k, v in esl_rmap_error_codes.items()])

for name, value in esl_rmap_error_names.items():
    try:
        getattr(module, name)
        logger.error(f"module {__name__} is trying to overwrite the constant {name} with a new value.")
    except AttributeError:
        setattr(module, name, value)

del esl_rmap_error_names
