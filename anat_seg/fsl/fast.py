# -*- coding: utf-8 -*-
from glob import glob
from typing import List, Tuple, Union

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
) -> Tuple[str, str, str]:
    """Performs automated segmentation of NIFTI brain MR images.

    Uses ``FSL``'s ``FAST`` (FMRIB's Automated Segmentation Tool) to classify
    and segment input anatomical MR images of the brain.

    NOTE: 
        * Bias field correction needs to be performed prior to use of ``fast``
            as it not implemented in this function.
        * ``neonate`` will change the default options to be compatible T2w 
            images.

    WARNING: Use of this function on neonatal neuroimages **WILL** result in
        suboptimal outputs. **Use with supreme caution**.

    Args:
        images: _description_
        out: _description_
        intype: _description_. Defaults to 1.
        classes: _description_. Defaults to 3.
        neonate: _description_. Defaults to False.
        log: _description_. Defaults to None.

    Returns:
        _description_
    """
    for i, image in enumerate(images):
        with NiiFile(
            src=image, assert_exists=True, validate_nifti=True
        ) as img:
            images[i]: List[str] = img.abspath()

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

