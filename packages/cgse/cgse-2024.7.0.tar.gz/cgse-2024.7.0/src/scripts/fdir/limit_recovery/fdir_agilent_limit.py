import logging
from argparse import ArgumentParser

import sys

from egse.setup import load_setup
from egse.tempcontrol.beaglebone.beaglebone import BeagleboneProxy
from egse.tempcontrol.spid.spid import PidProxy

# This script is triggered when one of the agilent channels violated the rate of change limit.
# This script is called with the agilent index and channel index as arguments.
# The corresponding PID channel and heater are turned off.

log = logging.getLogger(__name__)
logging.basicConfig()

log.info(f'running {__name__}')

parser = ArgumentParser()
parser.add_argument('hk_name', type=str, help='HK metric name')
args = parser.parse_args()

setup = load_setup()

bb_proxy = BeagleboneProxy()
pid_proxy = PidProxy()

if not pid_proxy.is_cs_connected():
    log.critical(f"Could not connect to PID proxy")
    sys.exit(f"Could not connect to PID proxy")
if not bb_proxy.is_cs_connected():
    log.critical(f"Could not connect to Beaglebone Black proxy")
    sys.exit(f"Could not connect to Beaglebone Black proxy")

agilent_model = 0 if args.hk_name.split('_')[1] == 'AG34972' else 2
agilent_num = 0 if int(args.hk_name.split('_')[2]) == 0 else 1
agilent_channel = int(args.hk_name.split('_')[3][1:])
daq_num = agilent_model + agilent_num


pid_channels = []
for l in setup.gse.spid.configuration.heaters.values():
    pid_channels.extend(l)

# Turn off all PID channels controlled by this DAQ and set the heater power to the last value.
for (pid_channel, agilent_idx, channel_index, beaglebone_idx, beaglebone_ch, _, _, _) in pid_channels:

    if agilent_idx == daq_num and channel_index == agilent_channel:
        log.info(f"Temperature sensor {agilent_channel} of DAQ {daq_num} was associated to PID channel {pid_channel}")
        log.info(f"PID channel {pid_channel} was associated with heater {beaglebone_idx} channel {beaglebone_ch}")
       
        log.info(f"Turning off PID channel {pid_channel}")
        # log.debug(f"pid_proxy.disable({pid_channel})")
        pid_proxy.disable(pid_channel)
        
        log.info(f'Disabling heater {beaglebone_idx} channel {beaglebone_ch}')
        # log.debug(f"bb_proxy.set_enable({beaglebone_idx}, {beaglebone_ch}, False)")
        bb_proxy.set_enable(beaglebone_idx, beaglebone_ch, False)


log.info(f'finished {__name__}')
