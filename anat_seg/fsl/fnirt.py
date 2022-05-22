# -*- coding: utf-8 -*-
"""Image (non-linear) registration module.

This module is a wrapper for ``FSL``'s ``FNIRT``.
"""
from typing import Optional, Tuple

from ..utils.commandio.commandio.command import Command
from ..utils.commandio.commandio.fileio import File
from ..utils.commandio.commandio.logutil import LogFile
from ..utils.niio import NiiFile


def fnirt(
    image: str,
    ref: str,
    aff: Optional[str] = None,
    out: Optional[str] = 'xfm-nonlinear',
    iout: bool = False,
    fout: bool = False,
    cout: bool = False,
    log: Optional[LogFile] = None,
) -> Tuple[str, str, str]:
    """Performs image non-linear registration of two images using ``FSL``'s ``FNIRT``.

    NOTE: ``FNIRT`` performs best with the whole head (and skull).

    Args:
        image: Input image.
        ref: Reference (target) image.
        aff: Input affine transformation matrix. Defaults to None.
        out: Output prefix. Defaults to 'xfm-nonlinear'.
        iout: Output transformation image. Defaults to False.
        fout: Output non-linear warp field. Defaults to False.
        cout: Output non-linear warp field coefficients. Defaults to False.
        log: Log file object. Defaults to None.

    Returns:
        Tuple of strings that correspond to: transformed image, warp field, warp field coefficients.
    """
    _sub_cmd: str = ""

    with NiiFile(src=image, assert_exists=True, validate_nifti=True) as im:
        with NiiFile(src=ref, assert_exists=True, validate_nifti=True) as rf:
            image: str = im.abspath()
            ref: str = rf.abspath()

    if aff is not None:
        with File(src=aff, assert_exists=True) as f:
            aff: str = f.abspath()
            _sub_cmd: str = f"--aff={aff}"

    if bool(iout):
        iout: str = f"{out}.nii.gz"
        _sub_cmd: str = f"{_sub_cmd} --iout={iout}"
    else:
        iout: str = None

    if bool(fout):
        fout: str = f"{out}_field.nii.gz"
        _sub_cmd: str = f"{_sub_cmd} --fout={fout}"
    else:
        fout: str = None

    if bool(cout):
        cout: str = f"{out}_field_coeff.nii.gz"
        _sub_cmd: str = f"{_sub_cmd} --cout={cout}"
    else:
        cout: str = None

    cmd: str = f"fnirt --in={image} --ref={ref} -v {_sub_cmd}"

    fnirt: Command = Command(cmd)
    fnirt.run(log=log)

    return iout, fout, cout

