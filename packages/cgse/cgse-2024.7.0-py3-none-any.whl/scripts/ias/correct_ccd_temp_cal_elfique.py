import os

from egse.setup import _load_yaml
from scripts.correct_ccd_cold_temperature_cal import correct_obsid_range, correct_od_range

SITE_ID = "IAS"


def correct_elfique(data_dir: str = None):
    """ Apply correct CCD temperature calibration in the cold.

     The problem was reported in https://github.com/IvS-KULeuven/plato-cgse-conf/issues/403:
     Correction needed to Cold CCD Temperature Calibration Coefficient

    During the Elfique test campaign, the CCD temperature calibration in the cold was incorrect.

    For all N-FEE HK files of the Elfique test campaign (obsid 1529 - 1754 / OD 20230822 - 20231009), this functions does
    the following:

        * Make a copy of the original N-FEE HK files (incl. "old" in their filename)
        * In the original files: Apply the correct CCD temperature calibration in the columns for the calibrated CCD
          temperatures (in the cold)

    These changes will be applied to the relevant folders in the /obs and /daily sub-folder of the given data folder.

    Args:
        - data_dir: Full path to the directory in which the data resides.  This is the folder with sub-folders /obs and
                    /daily, in which the N-FEE HK files are stored.  Default is the content of the
                    PLATO_DATA_STORAGE_LOCATION environment variable.
    """

    data_dir = data_dir or os.environ["PLATO_DATA_STORAGE_LOCATION"]

    cal_filename = "yaml//../../common/n-fee/nfee_sensor_calibration_elfique_v2.yaml"
    sensor_info = _load_yaml(cal_filename).temperatures.CCD_PT1000

    # Correct /obs folder -> https://github.com/IvS-KULeuven/plato-common-egse/issues/2772

    correct_obsid_range(1529, 1754, sensor_info, "elfique", data_dir, SITE_ID)

    # Correct /daily folder -> https://github.com/IvS-KULeuven/plato-common-egse/issues/2772

    correct_od_range(20230822, 20231009, sensor_info, data_dir, SITE_ID)
