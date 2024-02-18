from egse.decorators import dynamic_interface

class FdirManagerInterface:
    """ Descriptions of the interface can be found in the corresponding yaml file. """
    @dynamic_interface
    def signal_fdir(self, fdir_code: int):
        raise NotImplementedError

    @dynamic_interface
    def clear_fdir(self):
        raise NotImplementedError

    @dynamic_interface
    def get_state(self):
        raise NotImplementedError
