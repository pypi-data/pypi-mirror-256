import logging
import pickle

import zmq

import egse.rmap
import egse.spw
from egse.spw import ReadRequestReply
from egse.spw import SpaceWireInterface
from egse.spw import SpaceWirePacket
from egse.spw import WriteRequestReply

LOGGER = logging.getLogger(__name__)


class SpaceWireOverZeroMQ(SpaceWireInterface):
    """High level SpaceWire protocol running over ZeroMQ."""
    def __init__(self, endpoint: str, identity: str):
        self._endpoint = endpoint
        self._identity = identity.encode("ascii")
        self._zcontext = None
        self._zsock = None
        self._poller = None
        self._transaction_id = 0

    def connect(self):
        LOGGER.debug(f"Called {self.__class__.__name__}.connect().")
        self._zcontext = zmq.Context.instance()
        if "*" in self._endpoint:
            self._zsock = self._zcontext.socket(zmq.DEALER)
            self._zsock.identity = self._identity
            self._zsock.bind(self._endpoint)
        else:
            self._zsock = self._zcontext.socket(zmq.DEALER)
            self._zsock.identity = self._identity
            self._zsock.connect(self._endpoint)

        self._poller = zmq.Poller()
        self._poller.register(self._zsock, zmq.POLLIN)

    def disconnect(self):
        LOGGER.debug(f"Called disconnect() method of {self.__class__.__name__}.")
        self._zsock.close(linger=0)

    def configure(self):
        LOGGER.debug(f"Called configure() method of {self.__class__.__name__}.")

    def flush(self):
        LOGGER.debug(f"Called flush() method of {self.__class__.__name__}.")

    def send_timecode(self, timecode: int) -> int:
        LOGGER.debug(f"Called {self.__class__.__name__}.send_timecode({timecode}).")
        packet = bytes([0x91, timecode])
        self._zsock.send_multipart([self._identity, pickle.dumps(packet)])
        return 0

    def read_packet(self, timeout: int = None):

        try:
            socks = dict(self._poller.poll(timeout))  # timeout in milliseconds, do not block
        except KeyboardInterrupt:
            LOGGER.warning("Keyboard interrupt caught!")
            LOGGER.warning(
                "The process can not be interrupted with CTRL-C, "
                "send a quit command to the server."
            )
            return None, None

        if self._zsock not in socks:
            # This happens most of the time, no RMAP commands, therefore commented out the log msg
            # LOGGER.warning(f"No message received during {timeout=} seconds.")
            return None, None

        # LOGGER.debug(f"Called read_packet() method of {self.__class__.__name__}.")

        identity, pickle_string = self._zsock.recv_multipart()
        if not pickle_string:
            return None, None
        # LOGGER.debug(f"identity = {identity}, pickle_string = {type(pickle_string)}")
        response = pickle.loads(pickle_string)
        # LOGGER.debug(f"response = {response[:20]}")
        return None, response

    def write_packet(self, packet: bytes):
        LOGGER.debug(f"Called {self.__class__.__name__}.write_packet({packet[:10]=}).")
        self._zsock.send_multipart([self._identity, pickle.dumps(packet)])

    def read_register(self, address: int, length: int = 4, strict: bool = True) -> bytes:
        LOGGER.debug(f"Called {self.__class__.__name__}.read_register(0x{address:0x}, {length=}).")

        self._transaction_id = egse.spw.update_transaction_identifier(self._transaction_id)

        buffer = egse.rmap.create_rmap_read_request_packet(address, length, self._transaction_id, strict=strict)

        self.write_packet(buffer)
        _, data = self.read_packet()

        packet = SpaceWirePacket.create_packet(data)

        if isinstance(packet, ReadRequestReply):
            data = packet.data

            if len(data) != length:
                LOGGER.warning(
                    f"Expected data to be {length} bytes, but received {len(data)} bytes. {data=}")
        else:
            LOGGER.error(
                f"Expected RMAP read request reply packet, got {packet.__class__.__name__}")
            data = bytes()

        return data

    def write_register(self, address: int, data: bytes):
        LOGGER.debug(f"Called {self.__class__.__name__}.write_register(0x{address:0x}, {data}) method.")

        self._transaction_id = egse.spw.update_transaction_identifier(self._transaction_id)

        if egse.rmap.CRITICAL_AREA_START <= address <= egse.rmap.CRITICAL_AREA_END:
            buffer = egse.rmap.create_rmap_verified_write_packet(address, data, self._transaction_id)
        else:
            buffer = egse.rmap.create_rmap_unverified_write_packet(
                address, data, len(data), self._transaction_id)

        self.write_packet(buffer)
        _, data = self.read_packet()

        packet = SpaceWirePacket.create_packet(data)

        if isinstance(packet, WriteRequestReply):
            status = packet.status
        else:
            LOGGER.error(f"Expected RMAP write request reply packet, got {packet.__class__.__name__}")
            status = -1

        return status

    def read_memory_map(self, address: int, length: int = 4) -> bytes:
        LOGGER.debug(f"Called read_memory_map({address}, {length}) method of {self.__class__.__name__}.")

        self._transaction_id = egse.spw.update_transaction_identifier(self._transaction_id)

        buffer = egse.rmap.create_rmap_read_request_packet(address, length, self._transaction_id, strict=True)

        self.write_packet(buffer)
        _, data = self.read_packet()

        packet = SpaceWirePacket.create_packet(data)

        if isinstance(packet, ReadRequestReply):
            data = packet.data

            if len(data) != length:
                LOGGER.warning(
                    f"Expected data to be {length} bytes, but received {len(data)} bytes. {data=}")
        else:
            LOGGER.error(
                f"Expected RMAP read request reply packet, got {packet.__class__.__name__}")
            data = bytes()

        return data
