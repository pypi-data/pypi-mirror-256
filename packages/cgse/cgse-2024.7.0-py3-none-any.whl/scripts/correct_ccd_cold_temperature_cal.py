import os
import shutil
from datetime import datetime
from pathlib import PosixPath

from egse.config import find_file
from egse.fee.n_fee_hk import counts_to_temperature, ORIGIN
from egse.obsid import obsid_from_storage
from egse.setup import NavigableDict
import pandas as pd
from pandas.core.frame import DataFrame
from dateutil.rrule import rrule, DAILY


def correct_obsid_range(first_obsid: int, last_obsid: int, sensor_info: NavigableDict, camera_name: str, data_dir: str,
                        site_id: str):
    """ Correct the CCD temperature calibration in the cold in the N-FEE HK file for the given obsid range.

    This function does the following:

        * Make a copy of the original N-FEE HK files (incl. "old" in the filename)
        * In the original files: Apply the correct CCD temperature calibration in the columns for the calibrated CCD
          temperatures (in the cold)

    Args:
         - first_obsid: First obsid.
         - last_obsid: Last obsid.
         - sensor_info: Calibration information for the CCD_PT1000 sensor type.
         - data_dir: Full path to the directory in which the data resides.  This is the folder with sub-folders /obs and
                    /daily, in which the N-FEE HK files are stored.
        - site_id: Site ID.
    """

    for obsid in range(first_obsid, last_obsid + 1):
        correct_obsid(obsid, sensor_info, camera_name, data_dir, site_id)


def correct_obsid(obsid: int, sensor_info: NavigableDict, camera_name: str, data_dir: str, site_id: str):
    """ Correct the CCD temperature calibration in the cold in the N-FEE HK file for the given obsid.

    This function does the following:

        * Make a copy of the original file (incl. "old" in the filename)
        * In the original files: Apply the correct CCD temperature calibration in the columns for the calibrated CCD
          temperatures (in the cold)

    Args:
         - obsid: Observation identifier.
         - sensor_info: Calibration information for the CCD_PT1000 sensor type.
         - data_dir: Full path to the directory in which the data resides.  This is the folder with sub-folders /obs and
                    /daily, in which the N-FEE HK files are stored.
         - site_id: Site ID.
    """

    stored_obsid = obsid_from_storage(obsid, data_dir=data_dir, site_id=site_id, camera_name=camera_name)
    pattern = f"{stored_obsid}_{ORIGIN}_*.csv"
    nfee_hk_filename = find_file(pattern, root=f"{data_dir}/obs/{stored_obsid}")    # PosixPath

    if nfee_hk_filename is None:
        print(f"No N-FEE HK available for obsid {stored_obsid}")
        return

    correct_file(str(nfee_hk_filename), sensor_info)


def correct_od_range(first_od: int, last_od: int, sensor_info: NavigableDict, data_dir: str, site_id: str):
    """ Correct the CCD temperature calibration in the cold in the N-FEE HK file for the given OD range.

    This function does the following:

        * Make a copy of the original N-FEE HK files (incl. "old" in the filename)
        * In the original files: Apply the correct CCD temperature calibration in the columns for the calibrated CCD
          temperatures (in the cold)

    Args:
         - first_od: First observing day [yyyymmdd].
         - last_od: Last observing day [yyyymmdd].
         - sensor_info: Calibration information for the CCD_PT1000 sensor type.
         - data_dir: Full path to the directory in which the data resides.  This is the folder with sub-folders /obs and
                    /daily, in which the N-FEE HK files are stored.
        - site_id: Site ID.
    """

    start = datetime.strptime(str(first_od), "%Y%m%d")
    end = datetime.strptime(str(last_od), "%Y%m%d")

    for dt in rrule(DAILY, dtstart=start, until=end):
        correct_od(dt.strftime("%Y%m%d"), sensor_info, data_dir, site_id)


def correct_od(od: int, sensor_info: NavigableDict, data_dir: str, site_id: str):
    """ Correct the CCD temperature calibration in the cold in the N-FEE HK file for the given OD.

     This function does the following:

        * Make a copy of the original N-FEE HK file (incl. "old" in the filename)
        * In the original files: Apply the correct CCD temperature calibration in the columns for the calibrated CCD
          temperatures (in the cold)

     Args:
         - od: Observing day [yyyymmdd].
         - sensor_info: Calibration information for the CCD_PT1000 sensor type.
         - data_dir: Full path to the directory in which the data resides.  This is the folder with sub-folders /obs and
                    /daily, in which the N-FEE HK files are stored.
         - site_id: Site ID.
    """

    pattern = f"{od}_{site_id}_{ORIGIN}.csv"
    nfee_hk_filename = find_file(pattern, root=f"{data_dir}/daily/{od}")    # PosixPath

    if nfee_hk_filename is None:
        print(f"No N-FEE HK available for OD {od}")
        return

    correct_file(str(nfee_hk_filename), sensor_info)


def correct_file(filename: PosixPath, sensor_info: NavigableDict):
    """ Correct the CCD temperature calibration in the cold in the N-FEE HK file with the given filename.

     This function does the following:

        * Make a copy of the original file (incl. "old" in the filename)
        * In the original files: Apply the correct CCD temperature calibration in the columns for the calibrated CCD
          temperatures (in the cold)

     Args:
         - filename: Filename of the original N-FEE HK file that needs to be corrected.
         - sensor_info: Calibration information for the CCD_PT1000 sensor type.
    """

    filename = str(filename)

    # Make a copy of the original file (incl. "old" in the filename) in the same folder

    copy_filename = f"{filename.split('.')[0]}_old.csv"
    if not os.path.isfile(copy_filename):
        shutil.copyfile(filename, copy_filename)

    dataframe: DataFrame = pd.read_csv(filename)

    # Correct the calibration

    for ccd_number in range(1, 5):
        print(ccd_number)

        name_cal = f"NFEE_T_CCD{ccd_number}"
        name_raw = name_cal + "_RAW"

        raw_values = dataframe[name_raw].values
        calibrated_values = [counts_to_temperature(name_raw, raw_value, sensor_info[name_cal])
                             for raw_value in raw_values]
        dataframe[name_cal] = calibrated_values

    # Update the changes in the original file (not in the copy that was created at the beginning)

    dataframe.to_csv(filename)
