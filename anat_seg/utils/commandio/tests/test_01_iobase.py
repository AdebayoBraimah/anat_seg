# -*- coding: utf-8 -*-
"""Tests for the ``iobase`` module in the ``commandio`` package.
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

from iobase import IOBaseObj


def test_iobase_abc():
    with pytest.raises(TypeError):

        class myClass(IOBaseObj):
            """Test class object"""

            def __init__(self, src):
                super(myClass, self).__init__(src)

        c: myClass = myClass(src="t.txt")
