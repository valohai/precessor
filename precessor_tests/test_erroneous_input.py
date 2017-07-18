from urllib.parse import parse_qsl

import pytest

from precessor.excs import InvalidParameter, InvalidOperation
from precessor.ops import parse_operations
from precessor.params import parse_params


def test_erroneous_format():
    with pytest.raises(InvalidParameter):
        parse_params(parse_qsl('format=bmp'))


def test_erroneous_quality():
    with pytest.raises(InvalidParameter):
        parse_params(parse_qsl('quality=108'))
    with pytest.raises(InvalidParameter):
        parse_params(parse_qsl('quality=0'))


def test_erroneous_operation():
    with pytest.raises(InvalidOperation) as ei:
        parse_operations(parse_qsl('mangle=8&mongle=9'))
    assert 'mangle' in str(ei.value)
    assert 'mongle' in str(ei.value)


def test_erroneous_operation_parameter():
    with pytest.raises(InvalidOperation) as ei:
        parse_operations(parse_qsl('resize=yyy'))
    assert '"yyy" is not formatted correctly for resize' in str(ei.value)
