from lexer.lexer import *


class Parser:
    def __init__(self, lexer: Lexer, cur_token: Token = Token(TokenType.EOF, ""),
                 peek_token: Token = Token(TokenType.EOF, "")) -> None:
        self.lexer = lexer
        self.cur_token = cur_token
        self.peek_token = peek_token

    def next_token(self) -> None:
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()


def new(lexer: Lexer) -> Parser:
    p = Parser(lexer)
    p.next_token()
    p.next_token()
