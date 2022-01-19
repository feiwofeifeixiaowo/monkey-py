import sys

sys.path.append("..")
import unittest
from lexer import new
from tokens.tokens import TokenType


class TestNextToken(unittest.TestCase):
    def test_next_token(self):
        input = 'let five = 5; \
            let ten = 10; \
            let add = fn(x, y) { \
                x + y; \
            }; \
            let result = add(five, ten);'

        class ExpectedToken:
            def __init__(self, type_name: TokenType, literal: str) -> None:
                self.exp_token_type = type_name
                self.exp_literal = literal

        tests = [
            ExpectedToken(TokenType.LET, 'let'),
            ExpectedToken(TokenType.IDENT, 'five'),
            ExpectedToken(TokenType.ASSIGN, '='),
            ExpectedToken(TokenType.INT, '5'),
            ExpectedToken(TokenType.SEMICOLON, ';'),
            ExpectedToken(TokenType.LET, 'let'),
            ExpectedToken(TokenType.IDENT, 'ten'),
            ExpectedToken(TokenType.ASSIGN, '='),
            ExpectedToken(TokenType.INT, '10'),
            ExpectedToken(TokenType.SEMICOLON, ';'),
            ExpectedToken(TokenType.LET, 'LET'),
            ExpectedToken(TokenType.IDENT, 'add'),
            ExpectedToken(TokenType.ASSIGN, '='),
            ExpectedToken(TokenType.FUNCTION, 'fn'),
            ExpectedToken(TokenType.LPAREN, '('),
            ExpectedToken(TokenType.IDENT, 'x'),
            ExpectedToken(TokenType.COMMA, ','),
            ExpectedToken(TokenType.IDENT, 'y'),
            ExpectedToken(TokenType.RPAREN, ')'),
            ExpectedToken(TokenType.LBRACE, '{'),
            ExpectedToken(TokenType.IDENT, 'x'),
            ExpectedToken(TokenType.PLUS, '+'),
            ExpectedToken(TokenType.IDENT, 'y'),
            ExpectedToken(TokenType.SEMICOLON, ';'),
            ExpectedToken(TokenType.RBRACE, '}'),
            ExpectedToken(TokenType.SEMICOLON, ';'),
            ExpectedToken(TokenType.LET, 'let'),
            ExpectedToken(TokenType.IDENT, 'result'),
            ExpectedToken(TokenType.ASSIGN, '='),
            ExpectedToken(TokenType.IDENT, 'add'),
            ExpectedToken(TokenType.LPAREN, '('),
            ExpectedToken(TokenType.IDENT, 'five'),
            ExpectedToken(TokenType.COMMA, ','),
            ExpectedToken(TokenType.IDENT, 'ten'),
            ExpectedToken(TokenType.RPAREN, ')'),
            ExpectedToken(TokenType.SEMICOLON, ';'),
            ExpectedToken(TokenType.EOF, ''),
        ]
        l = new(input)
        for i, tt in enumerate(tests):
            tok = l.next_token()
            self.assertEqual(tok.token_type, tt.exp_token_type,
                             'tests[{}] - token_type wrong, expected {}, got {}'.format(i, tt.exp_token_type,
                                                                                        tok.token_type))
            self.assertEqual(tok.literal, tt.exp_literal,
                             'tests[{}] - literal wrong, expected {}, got {}'.format(i, tt.exp_literal, tok.literal))


if __name__ == '__main__':
    unittest.main()
