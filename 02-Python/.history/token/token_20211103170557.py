from collections import namedtuple

TokenType = namedtuple('TokenType', 'type')
Token = namedtuple('Token', 'token_type literal')

############# const vars ############
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
############# const vars ############
