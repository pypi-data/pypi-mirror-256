#!/usr/bin/env python3
import argparse
import os
import shutil
import logging

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from datetime import datetime
from dateutil.rrule import rrule, DAILY

from scripts.sron.gimbal_conversions import gimbal_rotations_to_fov_angles
from egse.obsid import obsid_from_storage
from egse.config import find_file

logger = logging.getLogger(__name__)

FOV_ORIGIN = 'FOV'
ENSEMBLE_ORIGIN = 'ENSEMBLE'


def correct_brigand_chimay(data_dir: str = None):
    data_dir = data_dir or os.environ['PLATO_DATA_STORAGE_LOCATION']

    correct_obsid_range(308, 382, "brigand", data_dir)
    correct_obsid_range(383, 391, "arthureddington", data_dir)
    correct_obsid_range(392, 688, "brigand", data_dir)
    correct_obsid_range(831, 1109, "chimay", data_dir)

    correct_od_range(20230629, 20231020, data_dir)


def correct_obsid_range(first_obsid: int, last_obsid: int, camera_name: str, data_dir: str):
    """
     Recompute the FOV housekeeping for the obsid range.

     This function does the following:

        * Make a copy of the original FOV files (incl. "old" in the filename)
        * In the original files:
            - Recompute all actual and commanded positions based on ENSEMBLE HK

     Args:
         - first_obsid: First obsid.
         - last_obsid: Last obsid.
         - data_dir: Full path to the directory in which the data resides.  This is the
         folder with sub-folders /obs and /daily, in which the FOV and ENSEMBLE HK files
         are stored.
    """
    for obsid in range(first_obsid, last_obsid+1):
        correct_obsid(obsid, camera_name, data_dir)


def correct_obsid(obsid: int, camera_name: str, data_dir: str):
    """
     Recompute the FOV housekeeping for the given obsid.

     This function does the following:

        * Make a copy of the original FOV file (incl. "old" in the filename)
        * In the original file:
            - Recompute all actual and commanded positions based on ENSEMBLE HK

     Args:
         - obsid: Observation identifier.
         - data_dir: Full path to the directory in which the data resides.  This is the
         folder with sub-folders /obs and /daily, in which the FOV and ENSEMBLE HK files
         are stored.
    """

    stored_obsid = obsid_from_storage(obsid,
                                      data_dir=data_dir,
                                      site_id="SRON",
                                      camera_name=camera_name)

    fov_pattern = f"{stored_obsid}_{FOV_ORIGIN}_*.csv"
    gimbal_pattern = f"{stored_obsid}_{ENSEMBLE_ORIGIN}_*.csv"

    fov_hk_filename = find_file(fov_pattern, root=f"{data_dir}/obs/{stored_obsid}")
    gimbal_hk_filename = find_file(gimbal_pattern, root=f"{data_dir}/obs/{stored_obsid}")

    if fov_hk_filename is None:
        logger.warning(f"No FOV HK available for OBSID {stored_obsid}")
        return

    if gimbal_hk_filename is None:
        logger.warning(f"No ENSEMBLE HK available for OBSID {stored_obsid}")
        return

    correct_valid_file(str(fov_hk_filename), str(gimbal_hk_filename))


def correct_od_range(first_od: int, last_od: int, data_dir: str):
    """
     Recompute the FOV housekeeping for the OD range.

     This function does the following:

        * Make a copy of the original FOV files (incl. "old" in the filename)
        * In the original files:
            - Recompute all actual and commanded positions based on ENSEMBLE HK.

     Args:
         - first_od: First observing day [yyyymmdd].
         - last_od: Last observing day [yyyymmdd].
         - data_dir: Full path to the directory in which the data resides.  This is the
         folder with sub-folders /obs and /daily, in which the FOV and ENSEMBLE HK files
         are stored.
    """
    start = datetime.strptime(str(first_od), "%Y%m%d")
    end = datetime.strptime(str(last_od), "%Y%m%d")

    for dt in rrule(DAILY, dtstart=start, until=end):
        correct_od(dt.strftime("%Y%m%d"), data_dir)


def correct_od(od: int, data_dir: str):
    """
     Recompute the FOV housekeeping for the given OD.

     This function does the following:

        * Make a copy of the original FOV files (incl. "old" in the filename)
        * In the original files:
            - Recompute all actual and commanded positions based on ENSEMBLE HK.

     Args:
         - od: Observing day [yyyymmdd].
         - data_dir: Full path to the directory in which the data resides.  This is the
         folder with sub-folders /obs and /daily, in which the FOV and ENSEMBLE HK files
         are stored.
    """
    fov_pattern = f"{od}_SRON_{FOV_ORIGIN}.csv"
    gimbal_pattern = f"{od}_SRON_{ENSEMBLE_ORIGIN}.csv"

    fov_hk_filename = find_file(fov_pattern, root=f"{data_dir}/daily/{od}")
    gimbal_hk_filename = find_file(gimbal_pattern, root=f"{data_dir}/daily/{od}")

    if fov_hk_filename is None:
        logger.warning(f"No FOV HK file '{fov_pattern}' available for OD {od}")
        return

    if gimbal_hk_filename is None:
        logger.warning(f"No ENSEMBLE HK file '{gimbal_pattern}' available for OD {od}")
        return

    correct_valid_file(str(fov_hk_filename), str(gimbal_hk_filename))


def add_angles_row(angles_dict, timestamp, act_theta, act_phi, cmd_theta=np.nan,
                   cmd_phi=np.nan):
    """ Appends a row to the angles dictionary

    Args:
        - angles_dict: dictionary representing a pandas dataframe
        - timestamp: timestamp from the gimbal housekeepng file
        - act_theta: recomputed actual theta angle
        - act_phi: recomputed actual phi angle
        - cmd_theta: recomputed commanded theta angle
        - cmd_phi: recomputed commanded phi angle

    """
    angles_dict['timestamp'].append(timestamp)
    angles_dict['FOV_ACT_THETA'].append(act_theta)
    angles_dict['FOV_ACT_PHI'].append(act_phi)
    angles_dict['FOV_CMD_THETA'].append(cmd_theta)
    angles_dict['FOV_CMD_PHI'].append(cmd_phi)


def correct_valid_file(fov_filename: str, gimbal_filename: str, plot: bool = False):
    """ Recompute the theta, phi values in the FOV HK file with the given filename.

    This function does the following:

        * Make a copy of the original file (incl. "old" in the filename).
        * Iterate over all rows in ENSEMBLE housekeeping
            - For each row, recompute the actual theta and phi.
            - When the gimbal is not moving, and the previous commanded position !=
            current commanded position, recompute the commanded theta and phi.

    Args:
        - fov_filename: Filename of the original FOV HK file that needs to be corrected.
        - gimbal_filename: Filename of the ensemble HK file with the valid X, Y
        coordinates.
    """
    # Make a copy of the original file (incl. "old" in the filename) in the same folder
    logger.info(f"Now correcting: {fov_filename}")

    copy_fov_filename = f"{fov_filename.split('.')[0]}_old.csv"
    if not os.path.isfile(copy_fov_filename):
        shutil.copyfile(fov_filename, copy_fov_filename)

    # Iterate over all rows in the FOV HK
    # angles_df = pd.read_csv(fov_filename)
    angles_dict = {
        'timestamp': [],
        'FOV_ACT_THETA': [],
        'FOV_ACT_PHI': [],
        'FOV_CMD_THETA': [],
        'FOV_CMD_PHI': []
    }

    coordinates_df = pd.read_csv(gimbal_filename)
    len_coordinates_ds = len(coordinates_df)

    is_moving = False

    previous_commanded_position = (np.nan, np.nan)

    for i, row in coordinates_df.iterrows():
        print(f"Now correcting row {i+1:06}/{len_coordinates_ds:06}\r", end="")

        # Extract timestamp, status, actual positions and commanded positions
        timestamp = row['timestamp']

        status_plane = row['GSRON_ENSEMBLE_STATUS_PLANE']

        act_x, act_y = (row['GSRON_ENSEMBLE_ACT_POS_X'],
                        row['GSRON_ENSEMBLE_ACT_POS_Y'])

        cmd_x, cmd_y = (row['GSRON_ENSEMBLE_CMD_POS_X'],
                        row['GSRON_ENSEMBLE_CMD_POS_Y'])

        # Recompute and save commanded positions when gimbal stops moving
        # Also compare commanded position vs. previous commanded position to prevent
        # false positives
        if (cmd_x, cmd_y) != previous_commanded_position and not status_plane & 0x1:
            if is_moving is True:
                is_moving = False
                # Recompute and save commanded position
                cmd_theta, cmd_phi = gimbal_rotations_to_fov_angles(cmd_x, cmd_y)
                add_angles_row(angles_dict, timestamp, np.nan, np.nan, cmd_theta, cmd_phi)
            previous_commanded_position = (cmd_x, cmd_y)
        else:
            is_moving = True

        # Recompute and save actual positions for each row
        act_theta, act_phi = gimbal_rotations_to_fov_angles(act_x, act_y)
        add_angles_row(angles_dict, timestamp, act_theta, act_phi)

    print("")
    angles_df = pd.DataFrame(angles_dict)
    angles_df.to_csv(fov_filename, index=False)

    if plot:
        angles_df.plot(x='timestamp', y=['FOV_ACT_THETA',
                                             'FOV_CMD_THETA',
                                             'FOV_ACT_PHI',
                                             'FOV_CMD_PHI'], style=['-', 'o', '-', 'o'])
        plt.show()


def main():
    parser = argparse.ArgumentParser(description="CLI tool for correcting FOV "
                                                 "housekeeping - PLATO-INAF-PL-NCR-0013")
    parser.add_argument('data_dir', type=str,
                        help='Full path to the directory in which the data resides.  '
                             'This is the folder with sub-folders /obs and /daily, '
                             'in which the N-FEE HK files are stored.  '
                             'Default is the content of the '
                             'PLATO_DATA_STORAGE_LOCATION environment variable.')

    args = parser.parse_args()

    correct_brigand_chimay(args.data_dir)


if __name__ == "__main__":
    main()

