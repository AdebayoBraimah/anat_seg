# -*- coding: utf-8 -*-
"""Brain segmentation module.

This module is a wrapper for ``FSL``'s ``FAST``.
"""
from glob import glob
from typing import List, Union

from ..utils.commandio.command import Command
from ..utils.commandio.fileio import File
from ..utils.commandio.logutil import LogFile
from ..utils.niio import NiiFile


def fast(
    images: List[str],
    out: str,
    intype: int = 1,
    classes: int = 3,
    neonate: bool = False,
    log: Union[str, LogFile] = None,
) -> List[str]:
    """Performs automated segmentation of NIFTI brain MR images.

    Uses ``FSL``'s ``FAST`` (FMRIB's Automated Segmentation Tool) to classify
    and segment input anatomical MR images of the brain.

    NOTE: 
        * Bias field correction needs to be performed prior to use of ``fast``
            as it not implemented in this function.
        * ``neonate`` will change the default options to be compatible T2w 
            images.

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
        neonate: Enables settings for neonatal neuroimages. Defaults to False.
            * Assumes input image(s) is/are T2w
        log: ``LogFile`` object or path to log file. Defaults to None.

    Returns:
        List of files that correspond to segmentation outputs.
    """
    for i, image in enumerate(images):
        with NiiFile(
            src=image, assert_exists=True, validate_nifti=True
        ) as img:
            images[i] = img.abspath()

    with File(src=out) as f:
        out: str = f.rm_ext()

    intype: int = int(intype)
    classes: int = int(classes)

    if neonate:
        intype: int = 2
        classes: int = 4

    channels: int = len(images)

    cmd: str = f"fast --nobias --channels={channels} --class={classes} \
        --type={intype} --out={out} {' '.join(images)}"

    fast: Command = Command(cmd)
    fast.run(log=log)

    seg_list: List[str] = glob(f"{out}_pve_*", recursive=False)
    seg_list.sort()

    return seg_list

