#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

# Built-in imports
import os

import requests

from ..pyrf.dist_append import dist_append
from ..pyrf.ts_append import ts_append
from ..pyrf.ttns2datetime64 import ttns2datetime64
from .get_dist import get_dist
from .get_ts import get_ts
from .list_files import list_files
from .list_files_sdc import list_files_sdc

# Local imports
from .tokenize import tokenize

__author__ = "Louis Richard"
__email__ = "louisr@irfu.se"
__copyright__ = "Copyright 2020-2023"
__license__ = "MIT"
__version__ = "2.4.2"
__status__ = "Prototype"

logging.captureWarnings(True)
logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)


def _var_and_cdf_name(var_str, mms_id):
    var = tokenize(var_str)
    cdf_name = f"mms{mms_id}_{var['cdf_name']}"
    return var, cdf_name


def _check_times(inp):
    if inp.time.data.dtype == "int64":
        out = inp.assign_coords(time=ttns2datetime64(inp.time.data))
    else:
        out = inp
    return out


def get_data(
    var_str,
    tint,
    mms_id,
    verbose: bool = True,
    data_path: str = "",
    from_sdc: bool = False,
):
    r"""Load a variable. var_str must be in var (see below)

    Parameters
    ----------
    var_str : str
        Key of the target variable (use mms.get_data() to see keys.).
    tint : list of str
        Time interval.
    mms_id : str or int
        Index of the target spacecraft.
    verbose : bool, Optional
        Set to True to follow the loading. Default is True.
    data_path : str, Optional
        Path of MMS data. If None use `pyrfu/mms/config.json`

    Returns
    -------
    out : xarray.DataArray or xarray.Dataset
        Time series of the target variable of measured by the target
        spacecraft over the selected time interval.

    See also
    --------
    pyrfu.mms.get_ts : Read time series.
    pyrfu.mms.get_dist : Read velocity distribution function.

    Examples
    --------
    >>> from pyrfu import mms

    Define time interval

    >>> tint_brst = ["2019-09-14T07:54:00.000", "2019-09-14T08:11:00.000"]

    Index of MMS spacecraft

    >>> ic = 1

    Load magnetic field from FGM

    >>> b_xyz = mms.get_data("b_gse_fgm_brst_l2", tint_brst, ic)

    """

    mms_id = str(mms_id)

    var, cdf_name = _var_and_cdf_name(var_str, mms_id)

    if from_sdc:
        file_names = [file["url"] for file in list_files_sdc(tint, mms_id, var)]
    else:
        file_names = list_files(tint, mms_id, var, data_path)

    assert file_names, "No files found. Make sure that the data_path is correct"

    if verbose:
        logging.info("Loading %s...", cdf_name)

    out = None

    for file_name in file_names:
        if from_sdc:
            file = requests.get(file_name, timeout=None).content
        else:
            file = os.path.normpath(file_name)

        if "-dist" in var["dtype"]:
            out = dist_append(out, get_dist(file, cdf_name, tint))

        else:
            out = ts_append(out, get_ts(file, cdf_name, tint))

    out = _check_times(out)

    return out
