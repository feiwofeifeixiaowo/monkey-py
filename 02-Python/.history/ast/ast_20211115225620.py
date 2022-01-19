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
    def __init__(self) -> None:
        super().__init__()
        self.node = Node()

    @abstractmethod
    def statement_node():
        raise NotImplementedError
