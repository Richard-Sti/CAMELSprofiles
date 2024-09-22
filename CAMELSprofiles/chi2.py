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
"""
Quick and dirty chi2 calculation to asses whether the profiles are similar.
"""
import numpy as np


def chi2(x, fiducial_data, min_log_group_mass, max_log_group_mass,
         max_radius, key="GasDensity", take_log10=True, verbose=True):
    min_group_mass = 10**min_log_group_mass
    max_group_mass = 10**max_log_group_mass

    group_mass_fiducial = fiducial_data["GroupMass"]

    mask_fiducial = group_mass_fiducial >= min_group_mass
    mask_fiducial &= group_mass_fiducial <= max_group_mass
    mask_radial = np.all(np.isfinite(fiducial_data[key]), axis=0)
    if verbose:
        print(f"{'Num. fiducial haloes:':<25} {np.sum(mask_fiducial)}")
        print(f"{'Num. fiducial bins:':<25} {np.sum(mask_radial)} / {len(mask_radial)}")  # noqa

    mask_x = x["GroupMass"] >= min_group_mass
    mask_x &= x["GroupMass"] <= max_group_mass

    mask_radial &= np.all(np.isfinite(x[key]), axis=0)
    mask_radial &= x["r"] < max_radius
    if verbose:
        print(f"{'Num. test haloes:':<25} {np.sum(mask_x)}")
        print(f"{'Num. bins:':<25} {np.sum(mask_radial)} / {len(mask_radial)}")

    f = lambda x: np.log10(x) if take_log10 else x  # noqa

    # Individual covariances
    C_fiducial = np.cov(f(fiducial_data[key][:, mask_radial]), rowvar=False)
    C_x = np.cov(f(x[key][:, mask_radial]), rowvar=False)

    # Combined covariance
    C = C_fiducial + C_x
    Cinv = np.linalg.inv(C)

    mean_fiducial = np.mean(f(fiducial_data[key][:, mask_radial]), axis=0)
    mean_x = np.mean(f(x[key][:, mask_radial]), axis=0)
    dx = mean_x - mean_fiducial

    return float(np.dot(dx, np.dot(Cinv, dx)))
