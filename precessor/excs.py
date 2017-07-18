class InvalidUrl(Exception):
    http_status = 403


class InvalidOperation(Exception):
    http_status = 400


class InvalidParameter(ValueError):
    http_status = 400


class OperationParseErrors(InvalidOperation):
    def __init__(self, errors):
        super(OperationParseErrors, self).__init__('%d errors' % len(errors))
        self.errors = errors

    def __str__(self):
        return '\n'.join(str(e) for e in self.errors)
