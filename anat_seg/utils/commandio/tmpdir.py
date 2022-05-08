# -*- coding: utf-8 -*-
"""Temporary working directory module for the ``commandio`` package.
"""
import os
import random

from workdir import WorkDir


class TmpDir(WorkDir):
    """Temporary directory class that creates (random) temporary directories and files given a parent directory.

    This class inherits methods from the ``WorkDir`` base class.

    Attributes:
        src: Input temproary working directory.
        parent_dir: Parent directory of the specified temproary directory.

    Usage example:
           >>> with TmpDir("/path/to/temporary_directory",False) as tmp_dir:
            ...     cwd = os.getcwd()
            ...     print("My temporary directory")
            ...     os.chdir(tmp_dir.src)
            ...     # do more stuff
            ...     os.chdir(cwd)
            ...
            >>> # or
            >>>
            >>> tmp_dir = TmpDir("/path/to/temporary_directory")
            >>> tmp_dir
            "/path/to/temporary_directory"
            >>> tmp_dir.rmdir(rm_parent=False)

    Args:
        src: Temporary parent directory name/path.
        use_cwd: Use current working directory as working direcory.
        cleanup: Perform clean-up of the temporary directory.
    """

    def __init__(
        self, src: str, use_cwd: bool = False, cleanup: bool = True
    ) -> None:
        """Initialization method for the TmpDir child class.

        Usage example:
            >>> with TmpDir("/path/to/temporary_directory",False) as tmp_dir:
            ...     cwd = os.getcwd()
            ...     print("My temporary directory")
            ...     os.chdir(tmp_dir.src)
            ...     # do more stuff
            ...     os.chdir(cwd)
            ...
            >>> # or
            >>> tmp_dir = TmpDir("/path/to/temporary_directory")
            >>> tmp_dir
            "/path/to/temporary_directory"
            >>> tmp_dir.rmdir(rm_parent=False)

        Args:
            src: Temporary parent directory name/path.
            use_cwd: Use current working directory as working directory.
            cleanup: Perform clean-up of the temporary directory.
        """
        _n: int = 10000
        self.src: str = os.path.join(
            src, "tmp_dir_" + str(random.randint(0, _n))
        )

        if cleanup:
            self.cleanup: bool = True
        else:
            self.cleanup: bool = False

        if use_cwd:
            _cwd: str = os.getcwd()
            self.src = os.path.join(_cwd, self.src)
        super(TmpDir, self).__init__(self.src, use_cwd)

    def __exit__(self, exc_type, exc_val, traceback):
        """Context manager exit method for ``TmpDir`` class."""
        if self.cleanup:
            self.rmdir()
        return super().__exit__(exc_type, exc_val, traceback)
