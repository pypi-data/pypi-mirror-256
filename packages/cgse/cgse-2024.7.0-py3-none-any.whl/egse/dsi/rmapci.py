# RMAP Configuration Interface
#
# This file implements functions to easily create the packets send over the RMAP protocol
# for the DPU-FEE interface.
#
# Please check the document PLATO-DLR-PL-IC-0002 v1.0 [25/09/2018] for reference.
# The RMAP Verified Write Request Packet Structure is defined on page 26 with req. FEE-DPU-IF-582.

from egse.dsi.rmap import ESL_RMAP
from egse.dsi.constants import RMAP_PROTOCOL_ID
from egse.rmap import rmap_crc_check


# FIXME: We could just use the rmap_write(..) command for this, but that currently doesn't have verify before write etc.
# It more looks like the RMAP interface to the device can also (better) be implemented in Python.

def write_critical_configuration_data(rmap_link: ESL_RMAP, buf, tid, addr, data):
    buf[0]  = rmap_link.target_logical_address
    buf[1]  = RMAP_PROTOCOL_ID
    buf[2]  = 0x7C                    # Instruction: RMAP Request, write, incrementing address, verify before write, and send reply, reply addr length=0
    buf[3]  = 0xD1                    # Key:
    buf[4]  = rmap_link.initiator_logical_address
    buf[5]  = (tid >> 8) & 0xFF       # MSB of the Transition ID
    buf[6]  = (tid) & 0xFF            # LSB of the Transition ID
    buf[7]  = (addr >> 32) & 0xFF     # Extended address
    buf[8]  = (addr >> 24) & 0xFF     # address (MSB)
    buf[9]  = (addr >> 16) & 0xFF     # address
    buf[10] = (addr >>  8) & 0xFF     # address
    buf[11] = (addr      ) & 0xFF     # address (LSB)
    buf[12] = 0x00                    # data length (MSB)
    buf[13] = 0x00                    # data length, fixed to 4 bytes for critical configuration parameters
    buf[14] = 0x04                    # data length (LSB)
    buf[15] = rmap_crc_check(buf, 0, 15)
    buf[16] = (data >> 24) & 0xFF     # data (MSB)
    buf[17] = (data >> 16) & 0xFF     # data
    buf[18] = (data >>  8) & 0xFF     # data
    buf[19] = (data      ) & 0xFF     # data (LSB)
    buf[20] = rmap_crc_check(buf, 16, 4)
    return buf
