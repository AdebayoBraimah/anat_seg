# -*- coding: utf-8 -*-
"""Brain extraction module.

This module is a wrapper for ``FSL``'s ``BET``.
"""
import os
from typing import Tuple, Union

from anat_seg.utils.commandio.commandio.command import Command
from anat_seg.utils.commandio.commandio.fileio import File
from anat_seg.utils.commandio.commandio.logutil import LogFile
from anat_seg.utils.commandio.commandio.tmpfile import TmpFile
from anat_seg.utils.commandio.commandio.util import timeops
from anat_seg.utils.niio import NiiFile


# Globlally define (temporary) log file object
# NOTE: Not the best practice in this scenario, but
#   it gets the job done.
with TmpFile(tmp_dir=os.getcwd(), ext=".log") as tmpf:
    log: LogFile = LogFile(log_file=tmpf.src)
    tmpf.remove()


@timeops(log=log)
def bet(
    image: str,
    out: str,
    frac_int: float = 0.5,
    mask: bool = False,
    log: Union[str, LogFile] = None,
) -> Tuple[str, Union[str, None]]:
    """Performs brain extraction of a NIFTI image file.

    Uses ``FSL``'s ``BET`` (Brain Extraction Tool) to perform brain extraction
    of some input NIFTI MR image.

    Usage example:
        >>> 

    Args:
        image: Input image.
        out: Output image prefix.
        frac_int: Fractional intensity threshold (0->1); smaller values give 
            larger brain outline estimates.
        mask: Output binarized brain mask.
        log: Log file object or file path.

    Returns:
        Tuple of strings that corresponds to the skull-stripped image, and the 
            mask (if requested).
    """
    with NiiFile(src=image, assert_exists=True, validate_nifti=True) as img:
        image: str = img.abspath()

    if out.endswith('.nii.gz') or out.endswith('.nii'):
        with File(src=out) as f:
            out: str = f.rm_ext()

    frac_int: float = float(frac_int)

    cmd: str = f"bet {image} {out} -f {frac_int} -v -R"

    if mask:
        cmd: str = f"{cmd} -m"
        mask_img: str = f"{out}_mask.nii.gz"
    else:
        mask_img: str = None

    # Run the command
    bet: Command = Command(cmd)
    bet.run(log=log)

    return f"{out}.nii.gz", mask_img

