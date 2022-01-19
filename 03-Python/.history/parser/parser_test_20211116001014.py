import sys

from ast.ast import *
from lexer.lexer import *

sys.path.append("..")
import unittest


class TestLetStatement(unittest.TestCase):
    def test_next_token(self):
        input = 'let five = 5; \
            let ten = 10; \
            let add = fn(x, y) { \
                x + y; \
            }; \
            let result = add(five, ten);\
            !-/*5;\
            5 < 10 > 5;\
            if (5 < 10) { \
                return true;\
            } else {\
                return false;\
            }\
            10 == 10;\
            10 != 9;\
            '

        class ExpectedToken:
            def __init__(self, type_name: TokenType, literal: str) -> None:
                self.exp_token_type = type_name
                self.exp_literal = literal

        tests = [

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