import os
import sys

sys.path.append(os.getcwd())
import unittest
import..token.token as token
from ..token.token import TokenType


class TestNextToken(unittest.TestCase):
    def test_next_token(self):
        input = '=+(){},;'

        class ExpectedToken:
            def __init__(self, type_name: TokenType, literal: str) -> None:
                self.exp_token_type = type_name
                self.exp_literal = literal

        tests = [
            ExpectedToken(token.ASSIGN, '='),
            ExpectedToken(token.PLUS, '+'),
            ExpectedToken(token.LPAREN, '('),
            ExpectedToken(token.RPAREN, ')'),
            ExpectedToken(token.LBRACE, '{'),
            ExpectedToken(token.RBRACE, '}'),
            ExpectedToken(token.COMMA, ','),
            ExpectedToken(token.SEMICOLON, ';'),
            ExpectedToken(token.EOF, 'EOF')
        ]
        l = new(input)
        for i, tt in enumerate(tests):
            tok = l.next_token()
            self.assertEqual(tok.token_type, tt.exp_token_type, 'token_type wrong.')
            self.assertEqual(tok.literal, tt.exp_literal, 'literal wrong.')


if __name__ == '__main__':
    unittest.main()
