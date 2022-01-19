from enum import Enum


class TokenType(Enum):
    ILLEGAL = 'ILLEGAL'
    EOF = 'EOF'
    # Identifiers + literals
    IDENT = 'IDENT'
    INT = 'INT'
    STRING = 'STRING'

    # operators
    ASSIGN = '='
    PLUS = '+'
    MINUS = '-'
    BANG = '!'
    ASTERISK = '*'
    SLASH = '/'

    LT = '<'
    GT = '>'

    # Delimiters
    COMMA = ','
    SEMICOLON = ';'
    LPAREN = '('
    RPAREN = ')'
    LBRACE = '{'
    RBRACE = '}'
    LBRACKET = '['
    RBRACKET = ']'
    COLON = ':'

    # Keywords
    FUNCTION = 'FUNCTION'
    LET = 'LET'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    IF = 'IF'
    ELSE = 'ELSE'
    RETURN = 'RETURN'

    EQ = '=='
    NOT_EQ = '!='


class Token:
    def __init__(self, type_name: TokenType, literal: str) -> None:
        self.token_type = type_name
        self.literal = literal

    def __str__(self) -> str:
        return 'Type: {}, Literal: {}'.format(self.token_type, self.literal)


key_words = {
    'fn': TokenType.FUNCTION,
    'let': TokenType.LET,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'return': TokenType.RETURN
}


def lookup_ident(ident: str) -> TokenType:
    if ident in key_words:
        return key_words[ident]
    return TokenType.IDENT
