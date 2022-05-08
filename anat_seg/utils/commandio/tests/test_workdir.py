"""Tests for the ``workdir`` module in the ``commandio`` package.
"""
import os
import sys
import pathlib


# Add package/module to PYTHONPATH
_pkg_path: str = os.path.join(
    str(pathlib.Path(os.path.abspath(__file__)).parents[1])
)
sys.path.append(_pkg_path)

from workdir import WorkDir


def test_mkdir():
    with WorkDir(src="test.1", use_cwd=True) as wd:
        assert wd.exists() == True


def test_rmdir():
    with WorkDir(src="test.1", use_cwd=True) as wd:
        wd.rmdir()
        assert wd.exists() == False


def test_abspath():
    with WorkDir(src="test.1", use_cwd=True) as wd:
        absolute_path: str = os.path.abspath(wd.src)
        assert wd.abspath() == absolute_path
        wd.rmdir()


def test_relpath():
    with WorkDir(src="test.1/test.1.2/test.1.3", use_cwd=True) as wd1:
        with WorkDir(src="test.2/test.2.2/test.2.3", use_cwd=True) as wd2:
            assert wd1.relpath(wd2.src) == "../../test.1/test.1.2/test.1.3"
            wd1.rmdir()
            wd2.rmdir()


def test_symlink():
    with WorkDir(src="test.1/test.1.2/test.1.3", use_cwd=True) as wd1:
        with WorkDir(src="test.2/test.2.2/test.2.3", use_cwd=True) as wd2:
            wd1.sym_link(dst="test.2/test.2.2")

            assert os.path.realpath(
                wd1.sym_link(dst="test.2/test.2.2/test.sym1")
            ) == os.path.abspath("test.1/test.1.2/test.1.3")

            assert os.path.realpath(
                wd2.sym_link(dst="test.1/test.1.2/test.1.3/test.sym2")
            ) == os.path.abspath("test.2/test.2.2/test.2.3")

            wd1.rmdir()
            wd2.rmdir()


def test_relative_symlink():
    with WorkDir(src="test.1/test.1.2/test.1.3", use_cwd=True) as wd1:
        with WorkDir(src="test.2/test.2.2/test.2.3", use_cwd=True) as wd2:
            wd1.sym_link(dst="test.2/test.2.2")

            assert os.path.realpath(
                wd1.sym_link(
                    dst="test.2/test.2.2/test.2.3/test.sym1", relative=True
                )
            ) == os.path.abspath("test.1/test.1.2/test.1.3")

            assert os.path.realpath(
                wd2.sym_link(
                    dst="test.1/test.1.2/test.1.3/test.sym2", relative=True
                )
            ) == os.path.abspath("test.2/test.2.2/test.2.3")

            wd1.rmdir()
            wd2.rmdir()


def test_abspath():
    with WorkDir(src="test.1", use_cwd=True) as wd1:
        with WorkDir(src="test.2", use_cwd=True) as wd2:
            assert wd1.abspath() == os.path.abspath("test.1")
            assert wd2.abspath() == os.path.abspath("test.2")
            wd1.rmdir()
            wd2.rmdir()
            assert wd1.exists() == False


# def test_basename():
# def test_dirname():
# def test_move():
# def test_join():
# def test_exists():
