import sys

sys.path.append("..")
sys.path.append(".")
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
            ExpectedToken(token.EOF, 'EOF')
        ]
        l = new(input)
        for i, tt in enumerate(tests):
            print('=================index: ', i)
            tok = l.next_token()
            self.assertEqual(tok.token_type.type_name, tt.exp_token_type.type_name,
                             'token_type wrong, expected {}, got {}'.format(tok.token_type.type_name,
                                                                            tt.exp_token_type.type_name))
            self.assertEqual(tok.literal, tt.exp_literal,
                             'literal wrong, expected {}, got {}'.format(tok.literal, tt.exp_literal))


if __name__ == '__main__':
    from os import sys, path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    unittest.main()
