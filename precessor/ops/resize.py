import re

from PIL import Image

from precessor.excs import InvalidOperation
from precessor.ops.base import Operation
from precessor.ops.utils import map_resample_mode


class ResizeOperation(Operation):
    name = 'resize'
    param_regexp = re.compile(r'(?P<width>\d+)?x(?P<height>\d+)?(?:,(?P<mode>\w+))?')
    param_types = {
        'width': int,
        'height': int,
        'mode': map_resample_mode,
    }
    param_defaults = {
        'mode': Image.LANCZOS,
    }

    def process(self, image):
        width = self.options.get('width')
        height = self.options.get('height')
        ratio = image.size[0] / image.size[1]

        if width is None or width < 0:
            if height is not None:
                width = int(ratio * height)

        if height is None or height < 0:
            if width is not None:
                height = int(width / ratio)

        if width is None or height is None:
            raise InvalidOperation('invalid resize parameters')

        if width > 10000 or height > 10000:  # TODO: Make this configurable
            raise InvalidOperation('result image too large')

        return self._inner_process(image, width, height)

    def _inner_process(self, image, width, height):
        return image.resize(
            size=(width, height),
            resample=self.options['mode'],
        )


class ResizeLargerOperation(ResizeOperation):
    name = 'resize-larger'

    def _inner_process(self, image, width, height):
        if image.size[0] < width or image.size[1] < height:
            return image
        return super()._inner_process(image, width, height)


class ResizeSmallerOperation(ResizeOperation):
    name = 'resize-smaller'

    def _inner_process(self, image, width, height):
        if image.size[0] > width or image.size[1] > height:
            return image
        return super()._inner_process(image, width, height)
