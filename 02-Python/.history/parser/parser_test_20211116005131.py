import sys
from typing import Type

import lexer.lexer as lexer
import parser.parser as parser
from ast.ast import *

sys.path.append("..")
import unittest


class TestLetStatement(unittest.TestCase):
    def test_letstatement(self):
        input = '\
            let x = 5; \
            let y = 10; \
            let foobar = 838383;\
            '
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        if program == None:
            self.fail('parse_program returned None')
        if len(program.statements) != 3:
            self.fail('program.statements does not contain 3 statements got{}'.format(len(program.statements)))

        class ExpectedStatements:
            def __init__(self, expect_identifier: str) -> None:
                self.expect_identifier = expect_identifier

        tests = [
            ExpectedStatements('x'),
            ExpectedStatements('y'),
            ExpectedStatements('foobar'),
        ]
        for i, tt in enumerate(tests):
            stmt = program.statements[i]
            if (self.__test_letstatement(stmt, tt.expect_identifier)):
                return
            tok = l.next_token()
            self.assertEqual(tok.token_type, tt.exp_token_type,
                             'tests[{}] - token_type wrong, expected {}, got {}'.format(i, tt.exp_token_type,
                                                                                        tok.token_type))
            self.assertEqual(tok.literal, tt.exp_literal,
                             'tests[{}] - literal wrong, expected {}, got {}'.format(i, tt.exp_literal, tok.literal))

    def __test_letstatement(self, s: Type[Statement], name: str) -> bool:
        if s.token_literal() != 'let':
            print("s.token_literal not 'let'. got={}".format(s.token_literal()))
            return False

        if not isinstance(s, LetStatement):
            print("s not *ast.LetStatement. got=%T", s)
            return False
        return 1


if __name__ == '__main__':
    unittest.main()
