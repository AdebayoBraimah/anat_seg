# -*- coding: utf-8 -*-
"""Perform mathematical operations on images.

This module is a wrapper for ``FSL``'s ``fslmaths``.
"""
import os
from enum import Enum, unique

from typing import Optional, Union

try:
    from typing_extensions import Self
except ImportError:
    class Self:
        """Helper class meant to act as a place holder for
        typing_extensions.Self class type hint.
        """
        pass

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
class fslmaths:
    """``FSL`` wrapper class for the ``fslmaths`` utility binary executable.

    Perform mathematical operations and/or manipulations of images.
    """

    def __init__(self, image: str, dt: Optional[str] = None):
        """``FSL`` wrapper class for the ``fslmaths`` utility binary executable.

        Perform mathematical operations and/or manipulations of images.

        Args:
            image: Input image.
            dt: Data type. Defaults to None.
        """
        _sub_cmd: str = ""

        with NiiFile(
            src=image, assert_exists=True, validate_nifti=True
        ) as img:
            image: str = img.abspath()

        if dt is not None:
            dt: str = FSLDataType(dt).name
            _sub_cmd: str = f"-dt {dt}"

        self._cmd: str = f"fslmaths {_sub_cmd} {image}"

    def thrP(self, num=Union[int, float]) -> Self:
        """Threshold image by some percentage.

        Args:
            num: Voxel intensity percentage to use for threshold. Defaults to Union[int,float].

        Raises:
            TypeError: Exception that is raised if ``num`` is not a number.

        Returns:
            Class instance of ``fslmaths``.
        """
        if isinstance(num, int) or isinstance(num, float):
            self._cmd: str = f"{self._cmd} -thrP {num}"
        else:
            raise TypeError(f"Input {num} is not a number.")
        return self

    def thr(self, num=Union[int, float]) -> Self:
        """Threshold image by some value.

        Args:
            num: Voxel intensity value to use for threshold. Defaults to Union[int,float].

        Raises:
            TypeError: Exception that is raised if ``num`` is not a number.

        Returns:
            Class instance of ``fslmaths``.
        """
        if isinstance(num, int) or isinstance(num, float):
            self._cmd: str = f"{self._cmd} -thr {num}"
        else:
            raise TypeError(f"Input {num} is not a number.")
        return self

    def mask(self, image: str) -> Self:
        """Mask image.

        Args:
            image: Input image to use as mask.

        Returns:
            Class instance of ``fslmaths``.
        """
        with NiiFile(
            src=image, assert_exists=True, validate_nifti=True
        ) as img:
            self._cmd: str = f"{self._cmd} -mas {img.abspath()}"
        return self

    def ero(self, repeat: int = 1) -> Self:
        """Erode image.

        Args:
            repeat: Number of times to perform erosion. Defaults to 1.

        Returns:
            Class instance of ``fslmaths``.
        """
        for _ in range(repeat):
            self._cmd: str = f"{self._cmd} -ero"
        return self

    def fmean(self, repeat: int = 1) -> Self:
        """Mean filtering, kernel weighted (conventionally used with gauss kernel)

        Args:
            repeat: Number of times to perform erosion. Defaults to 1.

        Returns:
            Class instance of ``fslmaths``.
        """
        for _ in range(repeat):
            self._cmd: str = f"{self._cmd} -fmean"
        return self

    def fmedian(self, repeat: int = 1) -> Self:
        """Median Filtering.

        Args:
            repeat: Number of times to perform erosion. Defaults to 1.

        Returns:
            Class instance of ``fslmaths``.
        """
        for _ in range(repeat):
            self._cmd: str = f"{self._cmd} -fmedian"
        return self

    def add(self, input: Union[int, float, str]) -> Self:
        """Add a value or NIFTI-1 image to another NIFTI-1 image file.
        
        Args:
            input: Input NIFTI-1 file, or number.

        Raises:
            TypeError: Exception that is raised if ``input`` is not a number or a NIFTI-1 image file.

        Returns:
            Class instance of ``fslmaths``.
        """
        if isinstance(input, int) or isinstance(input, float):
            self._cmd: str = f"{self._cmd} -add {input}"
        elif isinstance(input, str):
            with NiiFile(
                src=input, assert_exists=True, validate_nifti=True
            ) as img:
                self._cmd: str = f"{self._cmd} -add {img.abspath()}"
        else:
            raise TypeError(
                f"Input {input} is not an 'int', 'float' or 'string'."
            )
        return self

    def sub(self, input: Union[int, float, str]) -> Self:
        """Subtract a value or NIFTI-1 image to another NIFTI-1 image file.
        
        Args:
            input: Input NIFTI-1 file, or number.

        Raises:
            TypeError: Exception that is raised if ``input`` is not a number or a NIFTI-1 image file.

        Returns:
            Class instance of ``fslmaths``.
        """
        if isinstance(input, int) or isinstance(input, float):
            self._cmd: str = f"{self._cmd} -sub {input}"
        elif isinstance(input, str):
            with NiiFile(
                src=input, assert_exists=True, validate_nifti=True
            ) as img:
                self._cmd: str = f"{self._cmd} -sub {img.abspath()}"
        else:
            raise TypeError(
                f"Input {input} is not an 'int', 'float' or 'string'."
            )
        return self

    def mul(self, input: Union[int, float, str]) -> Self:
        """Multiply a value or NIFTI-1 image to another NIFTI-1 image file.
        
        Args:
            input: Input NIFTI-1 file, or number.

        Raises:
            TypeError: Exception that is raised if ``input`` is not a number or a NIFTI-1 image file.

        Returns:
            Class instance of ``fslmaths``.
        """
        if isinstance(input, int) or isinstance(input, float):
            self._cmd: str = f"{self._cmd} -mul {input}"
        elif isinstance(input, str):
            with NiiFile(
                src=input, assert_exists=True, validate_nifti=True
            ) as img:
                self._cmd: str = f"{self._cmd} -mul {img.abspath()}"
        else:
            raise TypeError(
                f"Input {input} is not an 'int', 'float' or 'string'."
            )
        return self

    def div(self, input: Union[int, float, str]) -> Self:
        """Divide a NIFTI-1 image by another NIFTI-1 image file or value.
        
        Args:
            input: Input NIFTI-1 file, or number.

        Raises:
            TypeError: Exception that is raised if ``input`` is not a number or a NIFTI-1 image file.

        Returns:
            Class instance of ``fslmaths``.
        """
        if isinstance(input, int) or isinstance(input, float):
            self._cmd: str = f"{self._cmd} -div {input}"
        elif isinstance(input, str):
            with NiiFile(
                src=input, assert_exists=True, validate_nifti=True
            ) as img:
                self._cmd: str = f"{self._cmd} -div {img.abspath()}"
        else:
            raise TypeError(
                f"Input {input} is not an 'int', 'float' or 'string'."
            )
        return self

    def run(
        self,
        out: str,
        odt: Optional[str] = None,
        log: Optional[LogFile] = None,
    ):
        """Run fslmaths command with command line flags.

        Args:
            out: Output image filename.
            odt: Output datatype. Defaults to None.
            log: Log file to be written to. Defaults to None.

        Returns:
            NIFTI-1 image file.
        """
        _sub_cmd: str = ""

        if odt is not None:
            odt: str = FSLDataType(odt).name
            _sub_cmd: str = f"-odt {odt}"

        self._cmd: str = f"{self._cmd} {out} {_sub_cmd}"

        fslmaths: Command = Command(self._cmd)
        fslmaths.check_dependency()
        fslmaths.run(log=log)

        return out


@unique
class FSLDataType(Enum):
    """``FSL`` input and output datatypes.

    NOTE:
        * The ``input`` option will set the datatype to that of the original image.
    """

    char: str = "char"
    short: str = "short"
    int: str = "int"
    float: str = "float"
    double: str = "double"
    input: str = "input"
