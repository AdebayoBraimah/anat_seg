# -*- coding: utf-8 -*-
"""Brain image segmentation module.

This module is a wrapper for several of ``FSL``'s and ``ANTs``'s executables.
"""
import os
from typing import List, Optional, Tuple, Union

from utils.commandio.commandio.command import Command, DependencyError
from utils.commandio.commandio.fileio import File
from utils.commandio.commandio.logutil import LogFile
from utils.commandio.commandio.workdir import WorkDir
from utils.commandio.commandio.tmpdir import TmpDir
from utils.niio import NiiFile
from utils.util import get_UNC_neonate_atlas

from biascorr import biascorr
from fsl.bet import bet
from fsl.fast import fast
from fsl.flirt import flirt
from fsl.fnirt import fnirt
from fsl.applywarp import applywarp
from fsl.convertwarp import convertwarp
from fsl.fslmaths import fslmaths


# TODO: Add option(s) for atlas-based/probability map guided segmentation

# def segmentation(image: str, out: str, frac_int: float = 0.5, neonate: bool = False, cleanup: bool = False, full_cleanup: bool = False, log: Union[str, LogFile] = None):

# def anat_seg(image: str, out: str, frac_int: float = 0.5, neonate: bool = False, cleanup: bool = False, full_cleanup: bool = False, log: Union[str, LogFile] = None):


def _neo_seg(
    image: str,
    out: str,
    frac_int: float = 0.5,
    priors: Optional[List[str]] = None,
    neonate: bool = False,
    N4: bool = False,
    cleanup: bool = True,
    full_cleanup: bool = False,
    log: Union[str, LogFile] = None,
):
    # Output working directory
    _out: str = os.path.abspath(out)
    outdir: str = os.path.dirname(_out)

    with WorkDir(src=outdir) as od:
        # Bias correct image
        restore, _ = biascorr(image=image, out=od.join('anat'), N4=N4, log=log)

        # Mask brain
        brain, _ = bet(
            image=restore,
            out=od.join('anat_brain'),
            frac_int=frac_int,
            mask=True,
            log=log,
        )

        # Compute transforms
        (
            template,
            template_brain,
            template_gm,
            template_wm,
            template_csf,
        ) = get_UNC_neonate_atlas()

        lin_xfm_img, lin_xfm_mat = flirt()
