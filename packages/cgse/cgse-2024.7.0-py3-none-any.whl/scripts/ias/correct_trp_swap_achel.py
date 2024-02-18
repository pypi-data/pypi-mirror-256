import os
import shutil
from datetime import datetime
from pathlib import PosixPath

import pandas as pd
from pandas.core.frame import DataFrame

from egse.config import find_file
from egse.fee.n_fee_hk import counts_to_temperature, ORIGIN
from egse.obsid import obsid_from_storage
from egse.setup import load_setup, NavigableDict
from dateutil.rrule import rrule, DAILY


def correct_achel(data_dir: str = None):
    """ PLATO-IAS-PL-NCR-0037: TRP5-8-10 inconsistent telemetry.

    During the Achel test campaign, the TRP5, TRP8, and TRP10 temperature sensors of the N-FEE were swapped in the TM
    dictionary.  As a result, the columns with their raw values have been swapped in the N-FEE HK file and the
    calibration is applied incorrectly.

    For all N-FEE HK files of the Achel test campaign (obsid 996 - 1528 / OD 20230404 - 20230719), this functions does
    the following:

        * Make a copy of the original N-FEE HK files (incl. "old" in their filename)
        * In the original files:
            - Swap the column names for the raw values for those three TRPs
            - Apply the calibration for those three columns

    These changes will be applied to the relevant folders in the /obs and /daily sub-folder of the given data folder.

    Args:
        - data_dir: Full path to the directory in which the data resides.  This is the folder with sub-folders /obs and
                    /daily, in which the N-FEE HK files are stored.  Default is the content of the
                    PLATO_DATA_STORAGE_LOCATION environment variable.
    """

    data_dir = data_dir or os.environ["PLATO_DATA_STORAGE_LOCATION"]

    setup = load_setup(setup_id=115, site_id="IAS", from_disk=True)
    sensor_info = setup.camera.fee.calibration.temperatures.TOU_TRP_PT1000

    # Correct /obs folder

    correct_obsid_range(996, 1528, sensor_info, "achel", data_dir)

    # Correct /daily folder

    correct_od_range(20230404, 20230719, sensor_info, data_dir)


def correct_obsid_range(first_obsid: int, last_obsid: int, sensor_info: NavigableDict, camera_name: str, data_dir: str):
    """
     Correct for the swap between TRP5, TRP8, and TRP10 in the N-FEE HK file for the obsid range.

     This function does the following:

        * Make a copy of the original N-FEE HK files (incl. "old" in the filename)
        * In the original files:
            - Swap the column names for the raw values for those three TRPs
            - Apply the calibration for those three columns

     Args:
         - first_obsid: First obsid.
         - last_obsid: Last obsid.
         - sensor_info: Calibration information for the TOU_TRP_PT1000 sensor type.
         - data_dir: Full path to the directory in which the data resides.  This is the folder with sub-folders /obs and
                    /daily, in which the N-FEE HK files are stored.
    """

    for obsid in range(first_obsid, last_obsid + 1):
        correct_obsid(obsid, sensor_info, camera_name, data_dir)


def correct_obsid(obsid: int, sensor_info: NavigableDict, camera_name: str, data_dir: str):
    """
     Correct for the swap between TRP5, TRP8, and TRP10 in the N-FEE HK file for the given obsid.

     This function does the following:

        * Make a copy of the original file (incl. "old" in the filename)
        * In the original file:
            - Swap the column names for the raw values for those three TRPs
            - Apply the calibration for those three columns

     Args:
         - obsid: Observation identifier.
         - sensor_info: Calibration information for the TOU_TRP_PT1000 sensor type.
         - data_dir: Full path to the directory in which the data resides.  This is the folder with sub-folders /obs and
                    /daily, in which the N-FEE HK files are stored.
    """

    stored_obsid = obsid_from_storage(obsid, data_dir=data_dir, site_id="IAS", camera_name=camera_name)
    pattern = f"{stored_obsid}_{ORIGIN}_*.csv"
    nfee_hk_filename = find_file(pattern, root=f"{data_dir}/obs/{stored_obsid}")    # PosixPath

    if nfee_hk_filename is None:
        print(f"No N-FEE HK available for obsid {stored_obsid}")
        return

    correct_file(nfee_hk_filename, sensor_info)


def correct_od_range(first_od: int, last_od: int, sensor_info: NavigableDict, data_dir: str):
    """
     Correct for the swap between TRP5, TRP8, and TRP10 in the N-FEE HK file for the OD range.

     This function does the following:

        * Make a copy of the original N-FEE HK files (incl. "old" in the filename)
        * In the original files:
            - Swap the column names for the raw values for those three TRPs
            - Apply the calibration for those three columns

     Args:
         - first_od: First observing day [yyyymmdd].
         - last_od: Last observing day [yyyymmdd].
         - sensor_info: Calibration information for the TOU_TRP_PT1000 sensor type.
         - data_dir: Full path to the directory in which the data resides.  This is the folder with sub-folders /obs and
                    /daily, in which the N-FEE HK files are stored.
    """

    start = datetime.strptime(str(first_od), "%Y%m%d")
    end = datetime.strptime(str(last_od), "%Y%m%d")

    for dt in rrule(DAILY, dtstart=start, until=end):
        correct_od(dt.strftime("%Y%m%d"), sensor_info, data_dir)


def correct_od(od: int, sensor_info: NavigableDict, data_dir: str):
    """
     Correct for the swap between TRP5, TRP8, and TRP10 in the N-FEE HK file for the given OD.

     This function does the following:

        * Make a copy of the original N-FEE HK file (incl. "old" in the filename)
        * In the original file:
            - Swap the column names for the raw values for those three TRPs
            - Apply the calibration for those three columns

     Args:
         - od: Observing day [yyyymmdd].
         - sensor_info: Calibration information for the TOU_TRP_PT1000 sensor type.
         - data_dir: Full path to the directory in which the data resides.  This is the folder with sub-folders /obs and
                    /daily, in which the N-FEE HK files are stored.
    """

    pattern = f"{od}_IAS_{ORIGIN}.csv"
    nfee_hk_filename = find_file(pattern, root=f"{data_dir}/daily/{od}")    # PosixPath

    if nfee_hk_filename is None:
        print(f"No N-FEE HK available for OD {od}")
        return

    correct_file(nfee_hk_filename, sensor_info)


def correct_file(filename: PosixPath, sensor_info: NavigableDict):
    """
     Correct for the swap between TRP5, TRP8, and TRP10 in the N-FEE HK file with the given filename.

     This function does the following:

        * Make a copy of the original file (incl. "old" in the filename)
        * In the original file:
            - Swap the column names for the raw values for those three TRPs
            - Apply the calibration for those three columns

     Args:
         - filename: Filename of the original N-FEE HK file that needs to be corrected.
         - sensor_info: Calibration information for the TOU_TRP_PT1000 sensor type.
    """

    filename = str(filename)

    # Make a copy of the original file (incl. "old" in the filename) in the same folder

    copy_filename = f"{filename.split('.')[0]}_old.csv"
    if not os.path.isfile(copy_filename):
        shutil.copyfile(filename, copy_filename)

    # Swap the column names (TRP5 -> TRP8; TRP8 -> TRP10; TRP10 -> TRP5)

    dataframe: DataFrame = pd.read_csv(filename)
    dataframe[["NFEE_TOU_TRP5_RAW", "NFEE_TOU_TRP8_RAW", "NFEE_TOU_TRP10_RAW"]] \
        = dataframe[["NFEE_TOU_TRP8_RAW", "NFEE_TOU_TRP10_RAW", "NFEE_TOU_TRP5_RAW"]]

    # Correct the calibration

    for trp in ["NFEE_TOU_TRP5", "NFEE_TOU_TRP8", "NFEE_TOU_TRP10"]:
        raw_values = dataframe[f"{trp}_RAW"].values
        calibrated_values = [counts_to_temperature(f"{trp}_RAW", raw_value, sensor_info[trp])
                             for raw_value in raw_values]
        dataframe[trp] = calibrated_values

    # Update the changes in the original file (not in the copy that was created at the beginning)

    dataframe.to_csv(filename)
