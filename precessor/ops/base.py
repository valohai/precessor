from precessor.excs import InvalidParameter


def identity(value):
    return value


class Operation:
    name = None
    param_regexp = None
    param_defaults = {}
    param_types = {}

    def __init__(self, options):
        self.options = options

    def process(self, image):
        """
        :type image: Image.Image
        :rtype: Image.Image
        """
        raise NotImplementedError('...')  # pragma: no cover

    @classmethod
    def parse(cls, value):
        try:
            params_match = cls.param_regexp.match(value)
            if not params_match:
                raise InvalidParameter('"%s" is not formatted correctly for %s' % (value, cls.name))
            params = cls.param_defaults.copy()
            params.update({
                name: cls.param_types.get(name, identity)(value)
                for (name, value)
                in params_match.groupdict().items()
                if value is not None
            })
            return cls(options=params)
        except InvalidParameter:
            raise
        except Exception as exc:
            raise InvalidParameter('Could not parse parameters for %s: %s (%s)' % (cls.name, value, exc))

    def __str__(self):
        return '%s(%s)' % (self.name, self.options)
