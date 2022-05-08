# -*- coding: utf-8 -*-
"""Temporary file module for the ``commandio`` package.
"""
import os
import random
from typing import Optional

from fileio import File


class TmpFile(File):
    """Creates and manipulates temporary files via inheritance from the ``File`` object base class.

    Attributes:
        file: Temporary file name.
        ext: File extension of input file. If no extension is provided, it is inferred.

    Usage example:
        >>> tmp_directory = TmpDir("/path/to/temporary_directory")
        >>>
        >>> temp_file = TmpFile(tmp_directory.tmp_dir,
        ...                             ext="txt")
        ...
        >>> temp_file
        "/path/to/temporary_directory/temporary_file.txt"

    Args:
        tmp_file: Temporary file name.
        ext: Temporary directory file extension.
    """

    def __init__(
        self,
        tmp_dir: Optional[str] = "",
        tmp_file: Optional[str] = "",
        ext: Optional[str] = "",
    ) -> None:
        """Initialization method for the TmpFile class that inherits from the ``File`` base class, allowing for the creation and maninuplation of temporary files.

        Usage example:
            >>> tmp_directory = TmpDir("/path/to/temporary_directory")
            >>>
            >>> temp_file = TmpFile(tmp_directory.tmp_dir,
            ...                             ext=".txt")
            ...
            >>> temp_file
            "/path/to/temporary_directory/temporary_file.txt"

        Args:
            tmp_dir: Temporary directory name.
            tmp_file: Temporary file name.
            ext: File extension.
        """
        if tmp_file:
            pass
        else:
            _n: int = 10000
            tmp_file: str = "tmp_file_" + str(random.randint(0, _n))

        if ext:
            if "." in ext:
                pass
            else:
                ext: str = f".{ext}"
            tmp_file: str = tmp_file + f"{ext}"

        tmp_file: str = os.path.join(tmp_dir, tmp_file)
        super(TmpFile, self).__init__(tmp_file, ext)
