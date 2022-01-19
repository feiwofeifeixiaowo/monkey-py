from lexer.lexer import *


class Parser:
    def __init__(self, lexer: Lexer, cur_token: Token, peek_token: Token) -> None:
        self.lexer = lexer
        self.cur_token = cur_token
        self.peek_token = peek_token


def New(lexer: Lexer) -> Parser:
