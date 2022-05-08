"""Tests for the ``tmpdir`` module in the ``commandio`` package.
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

from tmpdir import TmpDir


def test_mkdir():
    with TmpDir(src="test.1", use_cwd=True) as td:
        assert td.exists() == True


def test_no_cleanup():
    with TmpDir(src="test.1", use_cwd=True, cleanup=False) as td:
        assert td.exists() == True  # check if the directory exists
    assert td.exists() == True  # check if the directory still exists


def test_rmdir():
    with TmpDir(src="test.1", use_cwd=True) as td:
        assert td.exists() == True  # check if the directory exists
    assert td.exists() == False  # check if the directory was removed


# def test_abspath():
#     with TmpDir(src="test.1", use_cwd=True) as td:
#         absolute_path: str = os.path.abspath(td.src)
#         assert td.abspath() == absolute_path
#         td.rmdir()


# def test_relpath():
#     with TmpDir(src="test.1/test.1.2/test.1.3", use_cwd=True) as td1:
#         with TmpDir(src="test.2/test.2.2/test.2.3", use_cwd=True) as td2:
#             assert td1.relpath(td2.src) == "../../test.1/test.1.2/test.1.3"
#             td1.rmdir()
#             td2.rmdir()


# def test_symlink():
#     with TmpDir(src="test.1/test.1.2/test.1.3", use_cwd=True) as td1:
#         with TmpDir(src="test.2/test.2.2/test.2.3", use_cwd=True) as td2:
#             td1.sym_link(dst="test.2/test.2.2")

#             assert os.path.realpath(
#                 td1.sym_link(dst="test.2/test.2.2/test.sym1")
#             ) == os.path.abspath("test.1/test.1.2/test.1.3")

#             assert os.path.realpath(
#                 td2.sym_link(dst="test.1/test.1.2/test.1.3/test.sym2")
#             ) == os.path.abspath("test.2/test.2.2/test.2.3")

#             td1.rmdir()
#             td2.rmdir()


# def test_relative_symlink():
#     with TmpDir(src="test.1/test.1.2/test.1.3", use_cwd=True) as td1:
#         with TmpDir(src="test.2/test.2.2/test.2.3", use_cwd=True) as td2:
#             td1.sym_link(dst="test.2/test.2.2")

#             assert os.path.realpath(
#                 td1.sym_link(
#                     dst="test.2/test.2.2/test.2.3/test.sym1", relative=True
#                 )
#             ) == os.path.abspath("test.1/test.1.2/test.1.3")

#             assert os.path.realpath(
#                 td2.sym_link(
#                     dst="test.1/test.1.2/test.1.3/test.sym2", relative=True
#                 )
#             ) == os.path.abspath("test.2/test.2.2/test.2.3")

#             td1.rmdir()
#             td2.rmdir()


# def test_abspath():
#     with TmpDir(src="test.1", use_cwd=True) as td1:
#         with TmpDir(src="test.2", use_cwd=True) as td2:
#             assert td1.abspath() == os.path.abspath("test.1")
#             assert td2.abspath() == os.path.abspath("test.2")
#             td1.rmdir()
#             td2.rmdir()
#             assert td1.exists() == False


# def test_basename():
# def test_dirname():
# def test_move():
# def test_join():
# def test_exists():
