import abc
from abc import ABCMeta, abstractmethod


class AST:
    def __init__(self) -> None:
        pass


class Node:
    __meta_class__ = ABCMeta

    @abstractmethod
    def token_literal(self) -> str:
        raise NotImplementedError


class Statement:
    __meta_class__ = ABCMeta
    node = abc.

    @abstractmethod
    def statement_node():
        raise NotImplementedError
