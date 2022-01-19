class Lexer:
    def __init__(self, input: str, position: int, read_position: int, ch: str) -> None:
        self.input = input
        self.position = position
        self.read_position = read_position
        self.ch = ch

    def read_char(self) -> None:
        if l.read_position >= len(l.input):
            l.ch = 0
        else:
            l.ch = l.input[l.read_position]
        l.position = l.read_position
        l.read_position += 1


def new(input: str) -> Lexer:
    l = Lexer(input)
    l.read
    return l
