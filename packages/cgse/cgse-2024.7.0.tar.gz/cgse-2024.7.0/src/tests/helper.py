"""
This module provides helper functions for the unit test scripts. Do not use these functions
in your production code.
"""

# This module contains helper functions for making the unit tests work independently of any production setup.
# The Setup that is loaded from GlobalState would normally be provided by the configuration mananger (a server app)
# and provide devices that talk to the actual hardware. In the test scripts we do not want this behavior and the
# Setup is therefore loaded from the test_setup.yaml file and uses the device simulators.

from __future__ import annotations

from pathlib import Path

import numpy as np

from egse.config import find_file
from egse.config import find_root
from egse.spw import SpaceWirePacket
from egse.state import GlobalState


def load_test_setup():
    yaml_file = find_file(name='test_setup.yaml', in_dir='tests/data',
                          root=find_root(Path(__file__).resolve(), tests=('LICENSE',)))
    GlobalState._reload_setup_from(yaml_file)


def deserialize_packet_data(line: str, output_bytes: bool = False) -> np.ndarray | bytes:
    """Converts the ascii representation of the packet into a numpy array."""
    if output_bytes:
        return np.array([int(x, 16) for x in line.split()], dtype=np.uint8).tobytes()
    else:
        return np.array([int(x, 16) for x in line.split()], dtype=np.uint8)


def serialize_packet(packet: SpaceWirePacket, stride: int = 22):
    """Serializes the SpaceWirePacket to an ascii representation."""
    data = packet.packet_as_bytes

    data_serialized = [f"0x{b:02x}" for b in data]

    result = "(\n"
    while data_serialized:
        result += "    \""
        result += " ".join(data_serialized[:stride]) + " \"\n"
        del data_serialized[:stride]
    result += ")\n"

    return result
