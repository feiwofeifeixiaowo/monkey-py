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

    def peek_char(self) -> str:
        if self.read_position >= len(self.input):
            return 0
        else:
            return self.input[self.read_position]

    def read_identifier(self) -> str:
        pos = self.position
        while (is_letter(self.ch)):
            self.read_char()
        return self.input[pos:self.position]

    def read_number(self) -> str:
        pos = self.position
        while is_digit(self.ch):
            self.read_char()
        return self.input[pos:self.position]

    def read_string(self) -> str:
        position = self.position + 1
        while True:
            self.read_char()
            if self.ch == '"':
                break
        return self.input[position:self.position]

    def skip_whitespace(self) -> None:
        while (self.ch == ' ' or self.ch == '\t' or self.ch == '\n' or self.ch == '\r'):
            self.read_char()

    def next_token(self) -> Token:
        tok = Token(TokenType.EOF, "")

        self.skip_whitespace()

        if self.ch == '=':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                tok = new_token(TokenType.EQ, ch + self.ch)
            else:
                tok = new_token(TokenType.ASSIGN, self.ch)
        elif self.ch == '-':
            tok = new_token(TokenType.MINUS, self.ch)
        elif self.ch == '!':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                tok = new_token(TokenType.NOT_EQ, ch + self.ch)
            else:
                tok = new_token(TokenType.BANG, self.ch)
        elif self.ch == '*':
            tok = new_token(TokenType.ASTERISK, self.ch)
        elif self.ch == '/':
            tok = new_token(TokenType.SLASH, self.ch)
        elif self.ch == '<':
            tok = new_token(TokenType.LT, self.ch)
        elif self.ch == '>':
            tok = new_token(TokenType.GT, self.ch)
        elif self.ch == ';':
            tok = new_token(TokenType.SEMICOLON, self.ch)
        elif self.ch == '(':
            tok = new_token(TokenType.LPAREN, self.ch)
        elif self.ch == ')':
            tok = new_token(TokenType.RPAREN, self.ch)
        elif self.ch == '"':
            tok.token_type = TokenType.STRING
            tok.literal = self.read_string()
        elif self.ch == '{':
            tok = new_token(TokenType.LBRACE, self.ch)
        elif self.ch == '}':
            tok = new_token(TokenType.RBRACE, self.ch)
        elif self.ch == '[':
            tok = new_token(TokenType.LBRACKET, self.ch)
        elif self.ch == ']':
            tok = new_token(TokenType.RBRACKET, self.ch)
        elif self.ch == ',':
            tok = new_token(TokenType.COMMA, self.ch)
        elif self.ch == ':':
            tok = new_token(TokenType.COLON, self.ch)
        elif self.ch == '+':
            tok = new_token(TokenType.PLUS, self.ch)
        elif self.ch == 0:
            tok = Token(TokenType.EOF, "")
        else:
            if is_letter(self.ch):
                tok.literal = self.read_identifier()
                tok.token_type = lookup_ident(tok.literal)
                return tok
            elif is_digit(self.ch):
                tok.token_type = TokenType.INT
                tok.literal = self.read_number()
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
    return 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch == '_'


def is_digit(ch: str) -> bool:
    return '0' <= ch <= '9'
