class Lexer:
    def __init__(self, input: str, position: int, read_position: int, ch: str) -> None:
        self.input = input
        self.position = position
        self.read_position = read_position
        self.ch = ch


def new(input: str) -> Lexer:
    l = Lexer(input)

    pass
