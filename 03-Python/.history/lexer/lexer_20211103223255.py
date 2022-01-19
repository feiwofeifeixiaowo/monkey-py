class Lexer:
    def __init__(self, input: str, position: int, read_position: int, ch: str) -> None:
        self.input = input
        self.position = position
        self.read_position = read_position
        self.ch = ch

    def read_char(self) -> None:
        if self.read_position >= len(self.input):
            self.ch = 0
        else:
            self.ch = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1


def new(input: str) -> Lexer:
    l = Lexer(input)
    l.read
    return l
