import re

from PIL import Image

from precessor.ops.base import Operation


class RotateOperation(Operation):
    name = 'rotate'
    param_regexp = re.compile(r'(?P<angle>\d+)')
    param_types = {
        'angle': float,
    }

    def process(self, image: Image.Image):
        angle = self.options['angle']
        return image.rotate(
            angle=angle,
            resample=(Image.NEAREST if angle % 90 == 0 else Image.BICUBIC),
        )
