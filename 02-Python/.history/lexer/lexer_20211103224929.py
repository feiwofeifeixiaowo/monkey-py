import sys

sys.path.append("..")
sys.path.append(".")
import tokens.tokens as token
from lexer import Lexer
from tokens.tokens import ASSIGN, COMMA, EOF, LBRACE, LPAREN, PLUS, RBRACE, RPAREN, SEMICOLON, TokenType, Token


class Lexer:
    def __init__(self, input: str, position: int = -1, read_position: int = -1, ch: str = '') -> None:
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

    def next_token(self) -> Token:
        tok = Token(TokenType(""), "")
        if self.ch == '=':
            tok = new_token(ASSIGN, self.ch)
        elif self.ch == ';':
            tok = new_token(SEMICOLON, self.ch)
        elif self.ch == '(':
            tok = new_token(LPAREN, self.ch)
        elif self.ch == ')':
            tok = new_token(RPAREN, self.ch)
        elif self.ch == '{':
            tok = new_token(LBRACE, self.ch)
        elif self.ch == '}':
            tok = new_token(RBRACE, self.ch)
        elif self.ch == ',':
            tok = new_token(COMMA, self.ch)
        elif self.ch == '+':
            tok = new_token(PLUS, self.ch)
        elif self.ch == 0:
            tok.token_type = EOF
            tok.literal = ""
        else:
            pass
        self.read_char()
        return tok


def new_token(token_type: str, ch: str) -> Token:
    pass


func
newToken(tokenType
token.TokenType, ch
byte) token.Token
{
return token.Token
{Type: tokenType, Literal: string(ch)}
}

def new(input: str) -> Lexer:
    l = Lexer(input)
    l.read_char()
    return l
