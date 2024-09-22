# Copyright (C) 2024 Richard Stiskalek
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""Code to read in the gas densities."""
from glob import glob
from os.path import join
from re import search

import numpy as np
from h5py import File
from tqdm import tqdm
import pandas as pd

BASEPATH = "/mnt/extraspace/rstiskalek/CAMELS/"


def read_LH_parameters(basepath=None):
    """
    Read in the LH parameters from the provided table
    `CosmoAstroSeed_params_IllustrisTNG.txt`.

    Parameters
    ----------
    fname : str, optional
        The path to the file containing the parameters.

    Returns
    -------
    pandas.DataFrame
    """
    if basepath is None:
        basepath = BASEPATH

    fname = join(basepath, "CosmoAstroSeed_params_IllustrisTNG.txt")

    # Initialize an empty list to store data and a variable for headers
    data = []
    headers = None

    # Open the file and read it line by line
    with open(fname, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('+'):
                continue  # Skip border lines
            elif line.startswith('|'):
                # Remove leading and trailing '|' and split the line on '|'
                items = line.strip('|').split('|')
                # Strip whitespace from each item
                items = [item.strip() for item in items]
                if headers is None:
                    headers = items  # First data line is the header
                else:
                    data.append(items)  # Append data rows

    # Create a pandas DataFrame from the data
    df = pd.DataFrame(data, columns=headers)

    # Optionally, convert data types (e.g., numeric columns)
    numeric_cols = df.columns.drop('Name')
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
    df = df[df['Name'].str.startswith('LH')]

    return df


###############################################################################
#                        Read in the gas densities                            #
###############################################################################


def read_CV(simulation_set, snapnum, basepath=None):
    """
    Read in the CV files for a given simulation set and snapshot number.

    Parameters
    ----------
    simulation_set : str
        The name of the simulation set.
    snapnum : int
        The snapshot number, 33 corresponds to `z = 0`.
    basepath : str, optional
        The base path to the profiles. If not given, the default path is used.

    Returns
    -------
    data : dict
        A dictionary containing the various data.
    """
    if basepath is None:
        basepath = BASEPATH

    basepath = join(BASEPATH, "Profiles")
    files = glob(join(basepath, simulation_set, "CV", "CV_*"))
    indxs = sorted([int(search(r"CV_(\d+)", file).group(1)) for file in files])
    snapnum = str(snapnum).zfill(3)

    group_mass = [None] * len(indxs)
    profiles = [None] * len(indxs)
    r = [None] * len(indxs)

    for n, i in enumerate(tqdm(indxs, desc="Reading CV files")):
        fname = join(basepath, simulation_set, "CV", f"CV_{i}",
                     f"{simulation_set}_CV_{i}_{snapnum}.hdf5")

        with File(fname, 'r') as f:
            group_mass[n] = f["GroupMass"][...] * 1e10
            # The zeroth index reads in the gas densities.
            profiles[n] = f["Profiles"][0, ...]
            r[n] = f["r"][...]

    group_mass = np.hstack(group_mass)
    r = np.vstack(r)[0]
    profiles = np.vstack(profiles)

    # Replace zeroes with NaNs
    profiles[profiles == 0] = np.nan

    return {"GroupMass": group_mass,
            "r": r,
            "GasDensity": profiles}


def read_single(indx, simulation_set, suite, snapnum, basepath=None):
    if basepath is None:
        basepath = BASEPATH

    basepath = join(basepath, "Profiles", simulation_set, suite)

    snapnum = str(snapnum).zfill(3)
    fname = join(
        basepath, f"{suite}_{indx}",
        f"{simulation_set}_{suite}_{indx}_{snapnum}.hdf5")

    with File(fname, 'r') as f:
        group_mass = f["GroupMass"][...] * 1e10
        group_len = f["GroupLen"][...]
        # The zeroth index reads in the gas densities.
        profiles = f["Profiles"][0, ...]
        r = f["r"][...]

    # Replace zeroes with NaNs
    profiles[profiles == 0] = np.nan

    data = {"GroupMass": group_mass,
            "GroupLen": group_len,
            "r": r,
            "GasDensity": profiles}

    return data
