# -*- coding: utf-8 -*-
"""Image warp field maniupaltion module.

This module is a wrapper for ``FSL``'s ``convertwarp``.
"""
from typing import Optional

from ..utils.commandio.commandio.command import Command
from ..utils.commandio.commandio.fileio import File
from ..utils.commandio.commandio.logutil import LogFile
from ..utils.niio import NiiFile


def convertwarp(
    warp: str,
    out: str,
    ref: str,
    warp2: Optional[str] = None,
    premat: Optional[str] = None,
    rel: bool = False,
    abs: bool = False,
    log: Optional[str] = None,
) -> str:
    """Converts/combines non-linear ``FSL`` warp fields into one warp field.

    Args:
        warp: Warp field.
        out: Output warp field.
        ref: Reference (target) image.
        warp2: Second warp field. Defaults to None.
        premat: Pre-xfm linear-xfm matrix. Defaults to None.
        rel: use relative warp convention: x' = x + w(x). Defaults to False.
        abs: use absolute warp convention (default): x' = w(x). Defaults to False.
        log: Log file object. Defaults to None.

    Returns:
        Warp field
    """
    _sub_cmd: str = ""

    with NiiFile(src=warp, assert_exists=True, validate_nifti=True) as wp:
        with NiiFile(src=ref, assert_exists=True, validate_nifti=True) as rf:
            warp: str = wp.abspath()
            ref: str = rf.abspath()

    if warp2 is not None:
        with NiiFile(src=warp2, assert_exists=True, validate_nifti=True) as wp:
            warp2: str = wp.abspath()
            _sub_cmd: str = f"--warp2={warp2}"

    if premat is not None:
        with File(src=premat, assert_exists=True) as pm:
            premat: str = pm.abspath()
            _sub_cmd: str = f"{_sub_cmd} --premat={premat}"

    if bool(rel):
        _sub_cmd: str = f"{_sub_cmd} --rel"
    elif bool(abs):
        _sub_cmd: str = f"{_sub_cmd} --abs"
    else:
        _sub_cmd: str = f"{_sub_cmd} --abs"

    cmd: str = f"convertwarp -v --warp1={warp} --out={out} --ref={ref} {_sub_cmd}"

    convwarp: Command = Command(cmd)
    convwarp.run(log=log)

    return out

