# Copyright 2017 GNU Radio Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import tempfile

import pytest

from sigmf.sigmffile import SigMFFile

from .testdata import TEST_FLOAT32_DATA, TEST_METADATA


@pytest.fixture
def test_data_file():
    """when called, yields temporary file"""
    with tempfile.NamedTemporaryFile() as temp:
        TEST_FLOAT32_DATA.tofile(temp.name)
        yield temp


@pytest.fixture
def test_sigmffile(test_data_file):
    """If pytest uses this signature, will return valid SigMF file."""
    sigf = SigMFFile()
    sigf.set_global_field("core:datatype", "rf32_le")
    sigf.add_annotation(start_index=0, length=len(TEST_FLOAT32_DATA))
    sigf.add_capture(start_index=0)
    sigf.set_data_file(test_data_file.name)
    assert sigf._metadata == TEST_METADATA
    return sigf
