from tokens.tokens import TokenType, Token, lookup_ident


class Lexer:
    def __init__(self, input: str, position: int = 0, read_position: int = 0, ch: str = '') -> None:
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

    def read_identifier(self) -> str:
        pos = self.position
        while (is_letter(self.ch)):
            self.read_char()
        return self.input[pos:self.position]

    def skip_whitespace(self) -> None:
        while (self.ch == ' ' or self.ch == '\t' or self.ch == '\n' or self.ch == '\r'):
            self.read_char()

    def next_token(self) -> Token:
        tok = Token(TokenType.EOF, "")

        self.skip_whitespace()

        if self.ch == '=':
            tok = new_token(TokenType.ASSIGN, self.ch)
        elif self.ch == ';':
            tok = new_token(TokenType.SEMICOLON, self.ch)
        elif self.ch == '(':
            tok = new_token(TokenType.LPAREN, self.ch)
        elif self.ch == ')':
            tok = new_token(TokenType.RPAREN, self.ch)
        elif self.ch == '{':
            tok = new_token(TokenType.LBRACE, self.ch)
        elif self.ch == '}':
            tok = new_token(TokenType.RBRACE, self.ch)
        elif self.ch == ',':
            tok = new_token(TokenType.COMMA, self.ch)
        elif self.ch == '+':
            tok = new_token(TokenType.PLUS, self.ch)
        elif self.ch == 0:
            tok = Token(TokenType.EOF, "")
        else:
            if is_letter(self.ch):
                tok.literal = self.read_identifier()
                tok.token_type = lookup_ident(tok.literal)
                return tok
            else:
                tok = Token(TokenType.ILLEGAL, self.ch)
            pass
        self.read_char()
        return tok


def new_token(token_type: TokenType, ch: str) -> Token:
    return Token(token_type, ch)


def new(input: str) -> Lexer:
    l = Lexer(input)
    l.read_char()
    return l


def is_letter(ch: str) -> bool:
    return 'a' <= ch and ch <= 'z' or 'A' <= ch and ch <= 'Z' or ch == '_'
