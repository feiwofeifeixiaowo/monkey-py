import ast
from typing import List, Dict
from enum import Enum
from abc import ABCMeta, abstractmethod


class ObjectType(Enum):
    INTEGER_OBJ = 'INTEGER'
    BOOLEAN_OBJ = 'BOOLEAN'
    NULL_OBJ = 'NULL'
    RETURN_VALUE_OBJ = 'RETURN_VALUE'
    ERROR_OBJ = 'ERROR'
    FUNCTION_OBJ = 'FUNCTION'
    STRING_OBJ = 'STRING'
    BULIDIN_OBJ = 'BUILDIN'
    ARRAY_OBJ = 'ARRAY'
    HASH_OBJ = 'HASH'


class HashKey:
    def __init__(self, type: ObjectType, value: int):
        self.value = value
        self.type = type

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def __hash__(self):
        return self.value


class Hashable:
    @abstractmethod
    def hash_key(self) -> HashKey:
        return NotImplementedError


class Object:
    __meta_class__ = ABCMeta

    @abstractmethod
    def type(self) -> ObjectType:
        return NotImplementedError

    @abstractmethod
    def inspect(self) -> str:
        return NotImplementedError


class HashPair:
    def __init__(self, key: Object, value: Object):
        self.key = key
        self.value = value


class Hash(Object):
    def __init__(self, pairs: Dict[HashKey, HashPair]):
        self.pairs = pairs

    def type(self) -> ObjectType:
        return ObjectType.HASH_OBJ

    def inspect(self) -> str:
        pairs = []
        for _, pair in self.pairs.items():
            pairs.append('{}: {}'.format(pair.key.inspect(), pair.value.inspect()))
        return '{' + ', '.join(pairs) + '}'


class Integer(Object, Hashable):
    def __init__(self, value: int):
        super(Integer, self).__init__()
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.INTEGER_OBJ

    def inspect(self) -> str:
        return '{}'.format(self.value)

    def hash_key(self):
        return HashKey(type=self.type(), value=int(self.value))


class Error(Object):
    def __init__(self, msg: str):
        super(Error, self).__init__()
        self.message = msg

    def type(self) -> ObjectType:
        return ObjectType.ERROR_OBJ

    def inspect(self) -> str:
        return 'ERROR: ' + self.message


class Boolean(Object, Hashable):
    def __init__(self, value: bool):
        super(Boolean, self).__init__()
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.BOOLEAN_OBJ

    def inspect(self) -> str:
        return '{}'.format(str(self.value).lower())

    def hash_key(self):
        return HashKey(type=self.type(), value=1 if self.value else 0)


def BuiltinFunction(*args: List[Object]) -> Object:
    pass


class Builtin(Object):
    def __init__(self, fn):
        self.fn: BuiltinFunction = fn

    def type(self) -> ObjectType:
        return ObjectType.BULIDIN_OBJ

    def inspect(self) -> str:
        return 'buildin function'


class String(Object, Hashable):
    def __init__(self, value: str):
        super(String, self).__init__()
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.STRING_OBJ

    def inspect(self) -> str:
        return self.value

    def hash_key(self):
        return HashKey(type=self.type(), value=hash(self.value))


class Array(Object):
    def __init__(self):
        super(Array, self).__init__()
        self.elements: List[Object] = []

    def type(self) -> ObjectType:
        return ObjectType.ARRAY_OBJ

    def inspect(self) -> str:
        out = ''
        elems = []
        for el in self.elements:
            elems.append(el.inspect())
        out = out + '[' + ', '.join(elems) + ']'
        return out


class Null(Object):
    def __init__(self):
        super(Null, self).__init__()

    def type(self) -> ObjectType:
        return ObjectType.NULL_OBJ

    def inspect(self) -> str:
        return 'null'


class ReturnValue(Object):
    def __init__(self, value: Object):
        super(ReturnValue, self).__init__()
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.RETURN_VALUE_OBJ

    def inspect(self) -> str:
        return self.value.inspect()


class Function(Object):
    def __init__(self, params: List[ast.Identifier],
                 body: ast.BlockStatement,
                 env):
        self.parameters = params
        self.body = body
        self.env = env

    def type(self) -> ObjectType:
        return ObjectType.FUNCTION_OBJ

    def inspect(self) -> str:
        out = ''
        params = []
        for p in self.parameters:
            params.append(p.string())
        return out + 'fn' + '(' + ', '.join(params) + ') {\n' + self.body.string() + '\n'
