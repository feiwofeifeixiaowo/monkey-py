from abc import abstractmethod


class AST:
    def __init__(self) -> None:
        pass


class Node:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def token_literal(self) -> str:
        pass
