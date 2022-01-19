import unittest

from ast import *
from tokens.tokens import *


class TestString(unittest.TestCase):
    def test_string(self):
        program = Programs()
        let_stmt = LetStatement(token=Token(TokenType.LET, literal='let'),
                                name=Identifier(token=Token(TokenType.IDENT, literal='myVar'),
                                                value='myVar'),
                                value=Identifier(token=Token(TokenType.IDENT, literal='anotherVar'),
                                                 value='anotherVar'))
        program.statements.append(let_stmt)
        if program.string() != 'let myVar = anotherVar;':
            self.fail('program.string() wrong. got={}'.format(program.string()))


if __name__ == '__main__':
    unittest.main()
