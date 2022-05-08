# -*- coding: utf-8 -*-
"""Tests for the ``fileio`` module in the ``commandio`` package.
"""
import pytest

import os
import sys
import pathlib

# Add package/module to PYTHONPATH
_pkg_path: str = os.path.join(
    str(pathlib.Path(os.path.abspath(__file__)).parents[1])
)
sys.path.append(_pkg_path)

from fileio import File


def test_file_assert_exist():
    with pytest.raises(AssertionError):
        with File(src='test.txt', assert_exists=True) as f:
            f.basename


def test_file_create():
    with File(src='test.txt') as f:
        f.touch()
        assert os.path.exists(f.abspath()) == True


def test_file_remove():
    with File(src='test.txt') as f:
        f.touch()
        f.remove()
        assert os.path.exists(f.abspath()) == False


def test_file_copy():
    with File(src='test.txt') as f:
        f.touch()
        src2: str = f.copy("test.2.txt")

        with File(src=src2, assert_exists=True) as f2:
            assert os.path.exists(f2.abspath()) == True

            f.remove()
            f2.remove()

