import logging

from egse.setup import load_setup
from egse.stages.aerotech.ensemble import EnsembleProxy

# This script is triggerend when the gimbal motor tempertature is too high.
# The gimbal is moved to the resting position and is disabled.

log = logging.getLogger(__name__)
logging.basicConfig()

log.info(f'running {__name__}')

setup = load_setup()

# Get resting position values from the setup.
position = setup.gse.ensemble.resting_positions

with EnsembleProxy() as ensemble:

    # Move to resting position.
    ensemble.move_axes_degrees(position['X'], position['Y'])
    while ensemble.is_moving():
        pass

    log.info('moved to resting position')

    # Disable motors.
    ensemble.disable_axis('X')
    ensemble.disable_axis('Y')
    log.info('disabled axes')

log.info(f'finished {__name__}')
