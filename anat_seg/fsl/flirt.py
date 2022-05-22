# -*- coding: utf-8 -*-
"""Image (linear) registration module.

This module is a wrapper for ``FSL``'s ``FLIRT``.
"""
from typing import Optional, Tuple, Union

from ..utils.commandio.commandio.command import Command
from ..utils.commandio.commandio.fileio import File
from ..utils.commandio.commandio.logutil import LogFile
from ..utils.niio import NiiFile


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

    if (omat == True) and out:
        omat: str = f"{_out}.mat"
        _sub_cmd: str = f"{_sub_cmd} -omat {omat}"
    elif omat == True:
        omat: str = f"xfm-linear_dof-{dof}.mat"
    elif omat is not None:
        with File(src=omat) as om:
            _sub_cmd: str = f"{_sub_cmd} -omat {om.rm_ext()}.mat"

    cmd: str = f"flirt -in {image} -ref {ref} -dof {dof} -v {_sub_cmd}"

    flirt: Command = Command(cmd)
    flirt.run(log=log)

    return out, omat

