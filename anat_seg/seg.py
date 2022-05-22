# -*- coding: utf-8 -*-
"""Brain image segmentation module.

This module is a wrapper for several of ``FSL``'s and ``ANTs``'s executables.
"""
from typing import Tuple, Union

from utils.commandio.commandio.command import Command, DependencyError
from utils.commandio.commandio.fileio import File
from utils.commandio.commandio.logutil import LogFile
from utils.commandio.commandio.workdir import WorkDir
from utils.commandio.commandio.tmpdir import TmpDir
from utils.niio import NiiFile

from biascorr import biascorr
from fsl.bet import bet
from fsl.fast import fast

# TODO: Add option(s) for atlas-based/probability map guided segmentation

# def segmentation(image: str, out: str, frac_int: float = 0.5, neonate: bool = False, cleanup: bool = False, full_cleanup: bool = False, log: Union[str, LogFile] = None):

