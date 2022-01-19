from copy import deepcopy
import object
import evaluator
from typing import Dict, List


def len_func(args: List[object.Object]) -> object.Object:
    if len(args) !=1:
        return evaluator.new_error('wrong number of arguments. got={}, want=1'.format(len(args)))
    arg = args[0]
    if isinstance(arg, object.Array):
        return object.Integer(value=len(arg.elements))
    elif isinstance(arg, object.String):
        return object.Integer(value=len(arg.value))
    else:
        return evaluator.new_error('argument to `len` not supported, got {}'.format(arg.type().value))


def first_func(args: List[object.Object]) -> object.Object:
    if len(args) !=1:
        return evaluator.new_error('wrong number of arguments. got={}, want=1'.format(len(args)))
    arg = args[0]
    if arg.type() != object.ObjectType.ARRAY_OBJ:
        return evaluator.new_error('argument to `first` must be ARRAY, got {}'.format(arg.type().value))
    arr:object.Array = arg
    if len(arr.elements) > 0:
        return arr.elements[0]
    return evaluator.NULL


def last_func(args: List[object.Object]) -> object.Object:
    if len(args) !=1:
        return evaluator.new_error('wrong number of arguments. got={}, want=1'.format(len(args)))
    arg = args[0]
    if arg.type() != object.ObjectType.ARRAY_OBJ:
        return evaluator.new_error('argument to `last` must be ARRAY, got {}'.format(arg.type().value))
    arr:object.Array = arg
    length = len(arr.elements)
    if length > 0:
        return arr.elements[length - 1]
    return evaluator.NULL


def rest_func(args: List[object.Object]) -> object.Object:
    if len(args) !=1:
        return evaluator.new_error('wrong number of arguments. got={}, want=1'.format(len(args)))
    arg = args[0]
    if arg.type() != object.ObjectType.ARRAY_OBJ:
        return evaluator.new_error('argument to `rest` must be ARRAY, got {}'.format(arg.type().value))
    arr:object.Array = arg
    length = len(arr.elements)
    if length > 0:
        new_elements = deepcopy(arr.elements[1:length])
        arr = object.Array()
        arr.elements = new_elements
        return arr
    return evaluator.NULL


def push_func(args: List[object.Object]) -> object.Object:
    if len(args) !=2:
        return evaluator.new_error('wrong number of arguments. got={}, want=2'.format(len(args)))
    arg = args[0]
    if arg.type() != object.ObjectType.ARRAY_OBJ:
        return evaluator.new_error('argument to `push` must be ARRAY, got {}'.format(arg.type().value))
    arr:object.Array = arg
    # length = len(arr.elements)
    new_elements = deepcopy(arr.elements)
    new_elements.append(args[1])

    arr = object.Array()
    arr.elements = new_elements
    return arr


def puts_func(args: List[object.Object]) -> object.Object:
    for arg in args:
        print(arg.inspect())
    return evaluator.NULL


builtin_func: Dict[str, object.Builtin] = {
    'len': object.Builtin(fn=len_func),
    'first': object.Builtin(fn=first_func),
    'last': object.Builtin(fn=last_func),
    'rest': object.Builtin(fn=rest_func),
    'push': object.Builtin(fn=push_func),
    'puts': object.Builtin(fn=puts_func),
}