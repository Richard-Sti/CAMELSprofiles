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
"""Various utilities."""
import numpy as np
import warnings


def profiles_percentiles(profiles, percentiles=[16, 50, 84]):
    """
    Calculate the percentiles of the profiles over the haloes.

    Parameters
    ----------
    profiles : 2-dimensional array of shape (n_haloes, n_bins)
        The profiles of the haloes.
    percentiles : list of floats, optional
        The percentiles to calculate.

    Returns
    -------
    percentiles : tuple of 1-dimensional arrays
        The percentiles of the profiles.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="All-NaN slice encountered")
        return np.nanpercentile(profiles, percentiles, axis=0)
