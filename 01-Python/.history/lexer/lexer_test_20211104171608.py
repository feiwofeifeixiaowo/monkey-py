import sys

sys.path.append("..")
import unittest
from lexer import new
from tokens.tokens import TokenType


class TestNextToken(unittest.TestCase):
    def test_next_token(self):
        input = '=+(){},;'

        class ExpectedToken:
            def __init__(self, type_name: TokenType, literal: str) -> None:
                self.exp_token_type = type_name
                self.exp_literal = literal

        tests = [
            ExpectedToken(TokenType.ASSIGN, '='),
            ExpectedToken(TokenType.PLUS, '+'),
            ExpectedToken(TokenType.LPAREN, '('),
            ExpectedToken(TokenType.RPAREN, ')'),
            ExpectedToken(TokenType.LBRACE, '{'),
            ExpectedToken(TokenType.RBRACE, '}'),
            ExpectedToken(TokenType.COMMA, ','),
            ExpectedToken(TokenType.SEMICOLON, ';'),
            ExpectedToken(TokenType.EOF, '')
        ]
        l = new(input)
        for i, tt in enumerate(tests):
            tok = l.next_token()
            self.assertEqual(tok.token_type.type_name, tt.exp_token_type.type_name,
                             'tests[{}] - token_type wrong, expected {}, got {}'.format(i, tt.exp_token_type.type_name,
                                                                                        tok.token_type.type_name))
            self.assertEqual(tok.literal, tt.exp_literal,
                             'tests[{}] - literal wrong, expected {}, got {}'.format(i, tt.exp_literal, tok.literal))


if __name__ == '__main__':
    from os import sys, path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    unittest.main()
