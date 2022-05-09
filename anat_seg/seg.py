# -*- coding: utf-8 -*-
"""Brain image segmentation module.

This module is a wrapper for several of ``FSL``'s and ``ANTs``'s executables.
"""
from typing import Tuple, Union

from utils.commandio.command import Command, DependencyError
from utils.commandio.fileio import File
from utils.commandio.logutil import LogFile
from utils.commandio.workdir import WorkDir
from utils.commandio.tmpdir import TmpDir
from utils.niio import NiiFile

from biascorr import biascorr
from fsl.bet import bet
from fsl.fast import fast

# TODO: Add option(s) for atlas-based/probability map guided segmentation

# def segmentation(image: str, out: str, frac_int: float = 0.5, neonate: bool = False, cleanup: bool = False, full_cleanup: bool = False, log: Union[str, LogFile] = None):

