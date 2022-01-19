from abc import ABCMeta, abstractmethod
from typing import List

from tokens.tokens import *


class AST:
    def __init__(self) -> None:
        pass


class Node:
    __meta_class__ = ABCMeta

    @abstractmethod
    def token_literal(self) -> str:
        raise NotImplementedError


class Statement(Node):
    @abstractmethod
    def statement_node():
        raise NotImplementedError


class Expression(Node):
    @abstractmethod
    def expression_node():
        raise NotImplementedError


class Programs:
    def __init__(self) -> None:
        self.statements: List[Statement] = []

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ""


class LetStatement():
    def __init__(self, token: Token, name: Identifier) -> None:
        self.token = token
        self.name = name
        self.value: Expression
