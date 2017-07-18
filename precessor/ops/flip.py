import re

from PIL import Image, ImageOps

from precessor.ops.base import Operation


class FlipOperation(Operation):
    name = 'flip'
    param_regexp = re.compile(r'(?P<x>x)?(?P<y>y)?')

    def process(self, image: Image.Image):
        if self.options.get('x'):
            image = ImageOps.mirror(image)
        if self.options.get('y'):
            image = ImageOps.flip(image)
        return image
