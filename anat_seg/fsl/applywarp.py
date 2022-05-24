# -*- coding: utf-8 -*-
"""Apply image warp fields to other images.

This module is a wrapper for ``FSL``'s ``applywarp``.
"""
import os
from typing import Optional

from anat_seg.utils.commandio.commandio.command import Command
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
def applywarp(
    image: str,
    ref: str,
    out: str,
    warp: Optional[str] = None,
    abs: bool = False,
    rel: bool = False,
    log: Optional[LogFile] = None,
) -> str:
    """Applies non-linear ``FSL`` warp fields into one warp field.

    Args:
        image: Input image.
        ref: Reference (target) image.
        out: Output transformed image.
        warp: Warp field. Defaults to None.
        abs: use absolute warp convention (default): x' = w(x). Defaults to False.
        rel: use relative warp convention: x' = x + w(x). Defaults to False.
        log: Log file object. Defaults to None.

    Returns:
        Transformed image.
    """
    _sub_cmd: str = ""

    with NiiFile(src=image, assert_exists=True, validate_nifti=True) as im:
        with NiiFile(src=ref, assert_exists=True, validate_nifti=True) as rf:
            image: str = im.abspath()
            ref: str = rf.abspath()

    if warp is not None:
        with NiiFile(src=warp, assert_exists=True, validate_nifti=True) as wp:
            warp: str = wp.abspath()
            _sub_cmd: str = f"--warp={warp}"

    if bool(rel):
        _sub_cmd: str = f"{_sub_cmd} --rel"
    elif bool(abs):
        _sub_cmd: str = f"{_sub_cmd} --abs"
    else:
        _sub_cmd: str = f"{_sub_cmd} --abs"

    cmd: str = f"applywarp -v --in={image} --ref={ref} --out={out} {_sub_cmd}"

    appwarp: Command = Command(cmd)
    appwarp.check_dependency()
    appwarp.run(log=log)

    return out

