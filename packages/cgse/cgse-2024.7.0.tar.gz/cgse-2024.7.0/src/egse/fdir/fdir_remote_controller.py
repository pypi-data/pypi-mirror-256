import os
import logging
import subprocess

from egse.control import Response
from egse.fdir.fdir_remote_interface import FdirRemoteInterface

logger = logging.getLogger(__name__)


class FdirRemoteController(FdirRemoteInterface):
    def __init__(self):
        self.dialog = None

    def is_connected(self):
        return True
    
    def is_simulator(self):
        return False

    def generate_popup(self, code: str, actions: str, success: bool) -> Response:
        path = os.path.dirname(os.path.abspath(__file__))
        subprocess.Popen(['python3', f'{path}/fdir_remote_popup.py', code, actions, str(success)])




if __name__ == "__main__":
    fdir = FdirRemoteController()
    fdir.generate_popup("FDIR_CS_STOPPED", "rip", True)