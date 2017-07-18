from PIL import Image

from precessor.excs import InvalidParameter

mode_map = {
    'nearest': Image.NEAREST,
    'bilinear': Image.BILINEAR,
    'bicubic': Image.BICUBIC,
    'lanczos': Image.LANCZOS,
}


def map_resample_mode(mode):
    try:
        return mode_map[mode]
    except KeyError:
        raise InvalidParameter('Invalid resize mode %s' % mode)
