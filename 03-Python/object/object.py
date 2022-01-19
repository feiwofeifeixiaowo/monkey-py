import ast
from typing import List
from enum import Enum
from abc import ABCMeta, abstractmethod


class ObjectType(Enum):
    INTEGER_OBJ = 'INTEGER'
    BOOLEAN_OBJ = 'BOOLEAN'
    NULL_OBJ = 'NULL'
    RETURN_VALUE_OBJ = 'RETURN_VALUE'
    ERROR_OBJ = 'ERROR'
    FUNCTION_OBJ = 'FUNCTION'


class Object:
    __meta_class__ = ABCMeta

    @abstractmethod
    def type(self) -> ObjectType:
        return NotImplementedError

    @abstractmethod
    def inspect(self) -> str:
        return NotImplementedError


class Integer(Object):
    def __init__(self, value: int):
        super(Integer, self).__init__()
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.INTEGER_OBJ

    def inspect(self) -> str:
        return '{}'.format(self.value)


class Error(Object):
    def __init__(self, msg: str):
        super(Error, self).__init__()
        self.message = msg

    def type(self) -> ObjectType:
        return ObjectType.ERROR_OBJ

    def inspect(self) -> str:
        return 'ERROR: ' + self.message


class Boolean(Object):
    def __init__(self, value: bool):
        super(Boolean, self).__init__()
        self.value = value

    def type(self) -> ObjectType:
        return ObjectType.BOOLEAN_OBJ

    def inspect(self) -> str:
        return '{}'.format(str(self.value).lower())


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
