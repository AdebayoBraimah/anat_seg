# -*- coding: utf-8 -*-
"""File IO methods, functions and operations for the ``commandio`` package.
"""
import os
from typing import Optional, Tuple

from iobase import IOBaseObj


class File(IOBaseObj):
    """This class creates a ``File`` object that encapsulates a number of methods and properites for file and filename handling, and file manipulation.

    File object base class that inherits from the ``IOBaseObj`` abstract base class.

    Attributes:
        src: Input file.
        ext: File extension of input file. If no extension is provided, it is inferred.

    Usage example:
        >>> # Using class object as context manager
        >>> with File("file_name.txt") as file:
        ...     file.touch()
        ...     file.write_txt("some text")
        ...
        >>> # or
        >>>
        >>> file = File("file_name.txt")
        >>> file
        "file_name.txt"

    Args:
        src: Input file (need not exist at runtime/instantiated).
        ext: File extension of input file. If no extension is provided, it is inferred.
        assert_exists: Asserts that the specified input file must exist.
    """

    __slots__ = ("src", "ext")

    def __init__(
        self, src: str, ext: Optional[str] = "", assert_exists: bool = False
    ) -> None:
        """Initialization method for the File base class.

        Usage example:
            >>> # Using class object as context manager
            >>> with File("file_name.txt") as file:
            ...     file.touch()
            ...     file.write_txt("some text")
            ...     print(file.src)
            ...
            "file_name.txt"
            >>>
            >>> # or
            >>>
            >>> file = File("file_name.txt")
            >>> file
            "file_name.txt"

        Args:
            src: Input file (need not exist at runtime/instantiated).
            ext: File extension of input file. If no extension is provided, it is inferred.
            assert_exists: Asserts that the specified input file must exist.
        """
        self.src: str = src
        if ext:
            self.ext: str = ext
        else:
            self.ext: str = None
        super(File, self).__init__(src)

        if ext:
            self.ext: str = ext
        elif self.src.endswith(".gz"):
            self.ext: str = self.src[-7:]
        else:
            _, self.ext = os.path.splitext(self.src)

        if assert_exists:
            assert os.path.exists(
                self.src
            ), f"Input file {self.src} does not exist."

    def copy(self, dst: str) -> str:
        """Copies file to some source destination.

        Usage example:
            >>> # Using class object as context manager
            >>> with File("file_name.txt") as file:
            ...     new_file: str = file.copy("file2.txt")
            ...
            >>> new_file
            "/abs/path/to/file2.txt"
            >>>
            >>> # or
            >>>
            >>> file = File("file_name.txt")
            >>> file.copy("file2.txt")
            "/abs/path/to/file2.txt"

        Args:
            dst: Destination file path.
            relative: Symbolically link the file using a relative path.

        Returns:
            String that corresponds to the copied file.
        """
        return super().copy(dst)

    def touch(self) -> None:
        """Creates an empty file.

        This class mehtod is analagous to UNIX's ``touch`` command.

        Usage example:
            >>> # Using class object as context manager
            >>> with File("file_name.txt") as file:
            ...     file.touch()
            ...
            >>> # or
            >>>
            >>> file = File("file_name.txt")
            >>> file.touch()
        """
        if os.path.exists(self.src):
            print(f"The file: {self.src} already exists.")
        else:
            with open(self.src, "w") as _:
                pass
        return None

    def rm_ext(self, ext: str = "") -> str:
        """Removes file extension from the file.

        Usage example:
            >>> # Using class object as context manager
            >>> with File("file_name.txt") as file:
            ...     file.touch()
            ...     print(file.rm_ext())
            ...
            "file_name"
            >>>
            >>> # or
            >>>
            >>> file = File("file_name.txt")
            >>> file.rm_ext()
            "file_name"

        Args:
            ext: File extension.

        Returns:
            Filename as string with no extension.
        """
        if ext:
            ext_len: int = len(ext)
            return self.src[:-(ext_len)]
        elif self.ext:
            ext_len = len(self.ext)
            return self.src[:-(ext_len)]
        else:
            return self.src[:-(4)]

    def write(self, txt: str = "") -> None:
        """Writes/appends text to file.

        NOTE:
            Text written to file is ALWAYS utf-8 encoded.

        Usage example:
            >>> # Using class object as context manager
            >>> with File("file_name.txt") as file:
            ...     file.write("<Text to be written>")
            ...
            >>> # or
            >>>
            >>> file = File("file_name.txt")
            >>> file.write("<Text to be written>")

        Args:
            txt: Text/string to be written to file.
        """
        with open(self.src, mode="a", encoding="utf-8") as tmp_file:
            tmp_file.write(txt)
            tmp_file.close()
        return None

    def file_parts(self, ext: str = "") -> Tuple[str, str, str]:
        """Similar to MATLAB's ``fileparts``, this function splits a file and its path into its constituent parts:

            * file path
            * filename
            * extension

        Usage example:
            >>> # Using class object as context manager
            >>> with File("file_name.txt") as file:
            ...     print(file.file_parts())
            ...
            ("path/to/file", "filename", ".txt")
            >>>
            >>> # or
            >>>
            >>> file = File("file_name.txt")
            >>> file.file_parts()
            ("path/to/file", "filename", ".txt")

        Args:
            ext: File extension, needed if the file extension of file object is longer than 4 characters.

        Returns:
            Tuple:
                * Absolute file path, excluding filename.
                * Filename, excluding extension.
                * File extension.
        """
        file: str = self.src
        file: str = os.path.abspath(file)

        path, _filename = os.path.split(file)

        if ext:
            ext_num: int = len(ext)
            _filename: str = _filename[:-(ext_num)]
            [filename, _] = os.path.splitext(_filename)
        elif self.ext:
            ext: str = self.ext
            ext_num: int = len(ext)
            _filename: str = _filename[:-(ext_num)]
            [filename, _] = os.path.splitext(_filename)
        else:
            [filename, ext] = os.path.splitext(_filename)

        return (path, filename, ext)

    def remove(self) -> None:
        """Removes file.

        Usage example:
            >>> # Using class object as context manager
            >>> with File("file_name.txt") as file:
            ...     file.remove()
            ...
            >>>
            >>> # or
            >>>
            >>> file = File("file_name.txt")
            >>> file.remove()
        """
        return os.remove(self.abspath())
