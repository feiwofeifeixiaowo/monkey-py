import sys

import lexer.lexer as lexer
import parser.parser as parser

sys.path.append("..")
import unittest


class TestLetStatement(unittest.TestCase):
    def test_next_token(self):
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

        class ExpectedIdenifiier:
            pass

        for i, tt in enumerate(tests):
            tok = l.next_token()
            self.assertEqual(tok.token_type, tt.exp_token_type,
                             'tests[{}] - token_type wrong, expected {}, got {}'.format(i, tt.exp_token_type,
                                                                                        tok.token_type))
            self.assertEqual(tok.literal, tt.exp_literal,
                             'tests[{}] - literal wrong, expected {}, got {}'.format(i, tt.exp_literal, tok.literal))


if __name__ == '__main__':
    unittest.main()
