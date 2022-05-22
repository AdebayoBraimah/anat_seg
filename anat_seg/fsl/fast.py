# -*- coding: utf-8 -*-
"""Brain segmentation module.

This module is a wrapper for ``FSL``'s ``FAST``.
"""
from glob import glob
from typing import List, Union

from ..utils.commandio.commandio.command import Command
from ..utils.commandio.commandio.fileio import File
from ..utils.commandio.commandio.logutil import LogFile
from ..utils.niio import NiiFile


def fast(
    images: List[str],
    out: str,
    intype: int = 1,
    classes: int = 3,
    priors: List[str] = None,
    log: Union[str, LogFile] = None,
) -> List[str]:
    """Performs automated segmentation of NIFTI brain MR images.

    Uses ``FSL``'s ``FAST`` (FMRIB's Automated Segmentation Tool) to classify
    and segment input anatomical MR images of the brain.

    NOTE: 
        * Bias field correction needs to be performed prior to use of ``fast``
            as it not implemented in this function.

    WARNING: Use of this function on neonatal neuroimages **WILL** result in
        suboptimal outputs and GM/WM segmentations. **Use this function with
        supreme caution**.
    
    Usage example:
        >>> 

    Args:
        images: List of input images as file paths.
        out: Output prefix.
        intype: Input image type. Defaults to 1.
            * ``1``: T1w
            * ``2``: T2w
            * ``3``: PD - Proton Density
        classes: Number of tissue classes. Defaults to 3.
        priors: Alternative prior images input as a list (e.g. [ 'csf.nii.gz', 'gm.nii.gz', 'wm.nii.gz' ]).
        log: ``LogFile`` object or path to log file. Defaults to None.

    Returns:
        List of files that correspond to segmentation outputs.
    """
    _sub_cmd: str = ""

    for i, image in enumerate(images):
        with NiiFile(
            src=image, assert_exists=True, validate_nifti=True
        ) as img:
            images[i] = img.abspath()

    if priors is not None:
        for i, prior in enumerate(priors):
            with NiiFile(
                src=prior, assert_exists=True, validate_nifti=True
            ) as img:
                priors[i] = img.abspath()

        _sub_cmd: str = f"-A {' '.join(priors)}"

    with File(src=out) as f:
        out: str = f.rm_ext()

    intype: int = int(intype)
    classes: int = int(classes)

    channels: int = len(images)

    cmd: str = f"fast {_sub_cmd} -v --nobias --channels={channels} --class={classes} \
        --type={intype} --out={out} {' '.join(images)}"

    fast: Command = Command(cmd)
    fast.run(log=log)

    seg_list: List[str] = glob(f"{out}_pve_*", recursive=False)
    seg_list.sort()

    return seg_list

