import sys

sys.path.append("..")
print(sys.path)
import parser.parser as parser
import lexer.lexer as lexer
from ast.ast import Statement, LetStatement
from typing import Type

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

    def __test_letstatement(self, s: Type[Statement], name: str) -> bool:
        if s.token_literal() != 'let':
            print("s.token_literal not 'let'. got={}".format(s.token_literal()))
            return False

        if not isinstance(s, LetStatement):
            print("s not *ast.LetStatement. got={}".format(type(s)))
            return False
        if s.name.value != name:
            print("let_stmt.name.value not {}. got={}".format(name, s.name.value))
            return False
        if s.name.token_literal() != name:
            print("let_stmt.name.token_literal not {}. got={}".format(name, s.name.token_literal()))
            return False
        return True


if __name__ == '__main__':
    unittest.main()
