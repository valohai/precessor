from precessor.excs import OperationParseErrors, InvalidOperation
from precessor.ops.base import Operation
from precessor.ops.flip import FlipOperation
from precessor.ops.resize import ResizeOperation, ResizeSmallerOperation, ResizeLargerOperation
from precessor.ops.rotate import RotateOperation

operation_classes = [  # TODO: Add pluggability here
    ResizeOperation,
    ResizeSmallerOperation,
    ResizeLargerOperation,
    RotateOperation,
    FlipOperation,
]

operation_class_map = {op.name: op for op in operation_classes}


def parse_operations(param_list):
    operations = []
    errors = []
    for op, param in param_list:
        op_class = operation_class_map.get(op)
        if not op_class:
            errors.append(InvalidOperation('no such operation %s' % op))
            continue
        try:
            operations.append(op_class.parse(param))
        except Exception as exc:
            errors.append(exc)
    if errors:
        raise OperationParseErrors(errors=errors)
    return operations
