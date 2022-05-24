# -*- coding: utf-8 -*-
"""Image (linear) registration module.

This module is a wrapper for ``FSL``'s ``FLIRT``.
"""
import os
from typing import Optional, Tuple, Union

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
def flirt(
    image: str,
    ref: str,
    out: Optional[str] = None,
    omat: Optional[Union[str, bool]] = None,
    dof: int = 12,
    log: Optional[LogFile] = None,
) -> Tuple[str, str]:
    """Performs image linear registration of two images using ``FSL``'s ``FLIRT``.

    NOTE: ``FLIRT`` performs best when non-brain tissue has been removed.

    Args:
        image: Input image.
        ref: Reference (target) image.
        out: Output image name. Defaults to None.
        omat: Output transformation (xfm) matrix. If not specified, out is used to prefix this file. Defaults to None.
        dof: Degrees of freedom. Defaults to 12.
        log: Log file object. Defaults to None.

    Returns:
        Tuple of strings for the output linearly transformed image, and the output linear transformation matrix.
    """
    _sub_cmd: str = ""

    with NiiFile(src=image, assert_exists=True, validate_nifti=True) as im:
        with NiiFile(src=ref, assert_exists=True, validate_nifti=True) as rf:
            image: str = im.abspath()
            ref: str = rf.abspath()

    if out is not None:
        with NiiFile(src=out) as ot:
            _out: str = ot.rm_ext()
            _sub_cmd: str = f"-out {out}"

    if bool(omat) and out:
        omat: str = f"{_out}.mat"
        _sub_cmd: str = f"{_sub_cmd} -omat {omat}"
    elif bool(omat):
        omat: str = f"xfm-linear_dof-{dof}.mat"
    elif omat is not None:
        with File(src=omat) as om:
            _sub_cmd: str = f"{_sub_cmd} -omat {om.rm_ext()}.mat"

    cmd: str = f"flirt -in {image} -ref {ref} -dof {dof} -v {_sub_cmd}"

    flirt: Command = Command(cmd)
    flirt.check_dependency()
    flirt.run(log=log)

    return out, omat
