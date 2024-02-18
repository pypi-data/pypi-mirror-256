import logging
import os
from threading import Timer

from egse.command import ClientServerCommand
from egse.settings import Settings
from egse.setup import load_setup

WATCHDOG = 7
    
GSM = [8, 80, 78]

logger = logging.getLogger(__name__)
ctrl_settings = Settings.load('BeagleBone GSM Control Server')


class BeagleboneCommand(ClientServerCommand):
    def get_cmd_string(self, *args, **kwargs):
        out = super().get_cmd_string(*args, **kwargs)
        return out + '\n'

class BeagleboneDeviceInterface:
    
    def __init__(self):

        setup = load_setup()

        # Perform SRON gssw imports here to avoid issues at other THs
        from gssw.config.configclient import ConfigClient
        from gssw.common import addLoggingLevel
        from gssw.hal.hal import Hal
        from gssw.hal.halclient import HalClient
        from gssw.lib.device import Device

        self._is_connected = False

        # InitGssw does something to zmq that breaks cgse logging.
        # So instead I copied the essentials here.
        configClient = ConfigClient(os.getenv('GSSW_CONFIGURATION_FILE'))
        config = configClient.config
        addLoggingLevel('data', 15)

        self._availability = setup.gse.beaglebone_heater.availability

        hal = Hal()
        hal_client = HalClient(hal, config)
        hal_client.requestHal()

        self.dev_gpio_name = "gpio_gsm"
        self._dev_gpio = Device(self.dev_gpio_name, config, hal)
        
        self.watchdog_state = False

    def connect(self):
        self._is_connected = True  

    def disconnect(self):
        self._is_connected = False

    def reconnect(self):
        if self._is_connected:
            self.disconnect()
        self.connect()

    def is_connected(self):
        return self._is_connected
    
    def set_alert(self, pin):
        if pin >= 3:
            logger.info("Alert out of range (0 - 2)")
        else:
            GSM = [8, 80, 78]
            logger.info(f"Settings Alert {GSM[pin]}")
            self._dev_gpio.setMultiple([("GPIO_PIN", GSM[pin]), ("GPIO_VALUE", True)])
            unset = Timer(10.0, self.unset_alert, args=(pin,))
            unset.start()
        
    def unset_alert(self, pin):
        if pin >= 3:
            logger.info("Alert out of range (0 - 3)")
        else:
            logger.info(f"Unsettings Alert {GSM[pin]}")
            self._dev_gpio.setMultiple([("GPIO_PIN", GSM[pin]), ("GPIO_VALUE", False)])
        
    def get_alert(self, pin):
        if pin >= 3:
            logger.info("Alert out of range (0 - 3)")
        else:
            logger.info(f"{GSM[pin]} ")
            alert = self._dev_gpio.getSetMultiple([('GPIO_PIN', GSM[pin]), ('GPIO_VALUE', None)])
            return alert[0]
        
    def toggle_watchdog(self):
        self._dev_gpio.setMultiple([('GPIO_PIN', WATCHDOG), ('GPIO_VALUE', False if self.watchdog_state else True)])
        self.watchdog_state = not self.watchdog_state



def main():
    bb = BeagleboneDeviceInterface()
    
    # bb.set_alert(0)
    # bb.set_alert(1)
    # bb.set_alert(2)
    
    # time.sleep(1)
    
    print(bb.get_alert(0))
    print(bb.get_alert(1))
    print(bb.get_alert(2))
    
    
    # time.sleep(10)
    
    # print(bb.get_alert(0))
    # print(bb.get_alert(1))
    # print(bb.get_alert(2))



if __name__ == '__main__':
    main()
