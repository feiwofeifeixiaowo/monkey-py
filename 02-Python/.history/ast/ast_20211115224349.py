from abc import ABCMeta, abstractmethod


class AST:
    def __init__(self) -> None:
        pass


class Node:
    __meta_class = ABCMeta

    @abstractmethod
    def token_literal(self) -> str:
        raise NotImplementedError
