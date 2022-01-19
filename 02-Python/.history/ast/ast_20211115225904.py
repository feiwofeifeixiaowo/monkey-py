from abc import ABCMeta, abstractmethod


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
        self.statements = []
        pass
