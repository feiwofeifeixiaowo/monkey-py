import sys

sys.path.append("..")
print(sys.path)
import unittest
import tokens.tokens as token
from lexer import new
from tokens.tokens import TokenType


class TestNextToken(unittest.TestCase):
    def test_next_token(self):
        input = '=+(){},;'

        class ExpectedToken:
            def __init__(self, type_name: str, literal: str) -> None:
                self.exp_token_type = TokenType(type_name)
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
            ExpectedToken(token.EOF, '')
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
