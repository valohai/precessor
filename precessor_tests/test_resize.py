import pytest
from PIL import Image

from precessor.excs import InvalidOperation
from precessor.ops.resize import ResizeOperation, ResizeSmallerOperation, ResizeLargerOperation


def test_resize_by_height():
    img = Image.new('RGBA', (50, 80), 'blue')
    img = ResizeOperation.parse('x120').process(img)
    assert img.size == (75, 120)


def test_resize_by_width():
    img = Image.new('RGBA', (50, 80), 'blue')
    img = ResizeOperation.parse('120x').process(img)
    assert img.size == (120, 192)


def test_resize_invalid():
    img = Image.new('RGBA', (50, 80), 'blue')
    with pytest.raises(InvalidOperation):
        ResizeOperation.parse('x').process(img)


def test_resize_huge():
    img = Image.new('RGBA', (50, 80), 'blue')
    with pytest.raises(InvalidOperation):
        ResizeOperation.parse('7777777777x77777777').process(img)


def test_resize_smaller():
    img = Image.new('RGBA', (50, 80), 'blue')
    assert ResizeSmallerOperation.parse('120x').process(img).size == (120, 192)
    assert ResizeSmallerOperation.parse('30x').process(img) is img


def test_resize_larger():
    img = Image.new('RGBA', (50, 80), 'blue')
    assert ResizeLargerOperation.parse('30x44').process(img).size == (30, 44)
    assert ResizeLargerOperation.parse('60x').process(img) is img
