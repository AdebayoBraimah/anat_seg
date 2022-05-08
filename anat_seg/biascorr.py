# -*- coding: utf-8 -*-
"""Bias field correction module.

This module is a wrapper for ``FSL``'s ``FAST`` and ``ANTs``'s 
``N4BiasFieldCorrection``.
"""
from typing import Tuple, Union

from utils.commandio.command import Command, DependencyError
from utils.commandio.fileio import File
from utils.commandio.logutil import LogFile
from utils.commandio.workdir import WorkDir
from utils.commandio.tmpdir import TmpDir
from utils.niio import NiiFile
from fsl.bet import bet


def biascorr(
    image: str, out: str, N4: bool = False, log: Union[str, LogFile] = None
) -> Tuple[str, str]:
    """Performs bias field correction.

    Bias field correction is performed via FSL's bias field correction method 
    (via FAST) or using ANTs' N4 bias field correction algorithm.

    NOTE: Input image **SHOULD NOT** be skull-stripped.

    Usage example:
        >>>

    Args:
        image: Input image NIFTI file.
        out: Output image prefix.
        N4: Use N4 bias field correction. Defaults to False.
        log: ``LogFile`` object or path to log file. Defaults to None.

    Returns:
        Tuple of strings that correspond to bias field corrected image and the 
            corresponding bias field.
    """
    if N4:
        restore, biasfield = _N4_biascorr(image=image, out=out, log=log)
    else:
        restore, biasfield = _fsl_biascorr(image=image, out=out, log=log)
    return restore, biasfield


def _fsl_biascorr(
    image: str, out: str, log: Union[str, LogFile] = None
) -> Tuple[str, str]:
    """Performs FSL's bias field correction.

    NOTE: Input image **SHOULD NOT** be skull-stripped.

    Usage example:
        >>>

    Args:
        image: Input image NIFTI file.
        out: Output image prefix.
        log: ``LogFile`` object or path to log file. Defaults to None.

    Returns:
        Tuple of strings that correspond to bias field corrected image and the 
            corresponding bias field.
    """
    with NiiFile(src=image, assert_exists=True, validate_nifti=True) as img:
        image: str = img.abspath()

    with File(src=out) as f:
        out: str = f.rm_ext()
        outdir, _, _ = f.file_parts()

    with WorkDir(src=outdir) as od:
        with TmpDir(src=od.abspath()) as td:
            tmpout: str = td.join("fast")

            cmd: str = f"fast -b -B -o {tmpout} {image}"

            fast: Command = Command(cmd)
            fast.check_dependency()
            fast.run(log=log)

            tmp_restore: str = f"{tmpout}_restore.nii.gz"
            tmp_biasfield: str = f"{tmpout}_bias_field.nii.gz"

            with NiiFile(
                src=tmp_restore, assert_exists=True, validate_nifti=True
            ) as rs:
                with NiiFile(
                    src=tmp_biasfield, assert_exists=True, validate_nifti=True
                ) as bs:
                    restore: str = rs.copy(f"{out}_restore.nii.gz")
                    biasfield: str = bs.copy(f"{out}_bias_field.nii.gz")

    return restore, biasfield


def _N4_biascorr(
    image: str, out: str, log: Union[str, LogFile] = None
) -> Tuple[str, str]:
    """Performs N4 bias field correction.

    NOTE: Input image **SHOULD NOT** be skull-stripped.

    Usage example:
        >>>

    Args:
        image: Input image NIFTI file.
        out: Output image prefix.
        log: ``LogFile`` object or path to log file. Defaults to None.

    Raises:
        DependencyError: Raised if ``N4BiasFieldCorrection`` or ``N4`` is not 
            in the system path.

    Returns:
        Tuple of strings that correspond to bias field corrected image and the 
            corresponding bias field.
    """
    with NiiFile(src=image, assert_exists=True, validate_nifti=True) as img:
        image: str = img.abspath()

    with File(src=out) as f:
        out: str = f.rm_ext()
        outdir, _, _ = f.file_parts()

    with WorkDir(src=outdir) as od:
        with TmpDir(src=od.abspath()) as td:
            tmpout: str = td.join("brain")

            _, mask = bet(
                image=image, out=tmpout, frac_int=0.1, mask=True, log=log
            )

            _cmd1: Command = Command("N4BiasFieldCorrection")
            _cmd2: Command = Command("N4")

            # NOTE: Dependency check is performed here as N4BiasFieldCorrection
            #   (installed via ANTs) can also be installed as just N4 (via dHCP
            #   structural pipleline). Both are checked here.
            if _cmd1.check_dependency(raise_exc=False):
                cmd: str = f"{_cmd1}"
            elif _cmd2.check_dependency(raise_exc=False):
                cmd: str = f"{_cmd2}"
            else:
                raise DependencyError(
                    f"{_cmd1} is not installed or in system PATH variable."
                )

            # Create output filenames
            tmp_rest: str = td.join("restore.nii.gz")
            tmp_bias: str = td.join("bias.nii.gz")

            # Construct command
            cmd: str = f"{cmd} -i {image} -x {mask} -o \"[{tmp_rest},{tmp_bias}]\" \
                -c \"[50x50x50,0.001]\" -s 2 -b \"[100,3]\" -t \"[0.15,0.01,200]\""

            N4: Command = Command(cmd)
            N4.run(log=log)

            # Verify and validate output NIFTI files
            with NiiFile(
                src=tmp_rest, assert_exists=True, validate_nifti=True
            ) as rs:
                with NiiFile(
                    src=tmp_bias, assert_exists=True, validate_nifti=True
                ) as bs:
                    restore: str = rs.copy(f"{out}_restore.nii.gz")
                    biasfield: str = bs.copy(f"{out}_bias_field.nii.gz")

    return restore, biasfield

