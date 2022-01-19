from enum import Enum


class TokenType(Enum):
    ILLEGAL = 'ILLEGAL'
    EOF = 'EOF'
    # Identifiers + literals
    IDENT = 'IDENT'
    INT = 'INT'
    ASSIGN = '='
    PLUS = '+'

    # Delimiters
    COMMA = ','
    SEMICOLON = ';'
    LPAREN = '('
    RPAREN = ')'
    LBRACE = '{'
    RBRACE = '}'
    # Keywords
    FUNCTION = 'FUNCTION'
    LET = 'LET'


class Token:
    def __init__(self, type_name: TokenType, literal: str) -> None:
        self.token_type = type_name
        self.literal = literal


key_words = {
    'fn': TokenType.FUNCTION,
    'let': TokenType.LEt
}
