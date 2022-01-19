import unittest
from collections import namedtuple
from typing import Type

import lexer.lexer as lexer
import parser
from ast.ast import Statement, Expression, Identifier, LetStatement, ReturnStatement, \
    ExpressionStatement, IntegerLiteral, PrefixExpression, InfixExpression, Boolean, IfExpression, FunctionLiteral, \
    CallExpression


# class TestLetStatement(unittest.TestCase):
#     def test_letstatement(self):
#         input = '\
#             let x = 5; \
#             let y = 10; \
#             let foobar = 838383;\
#             '
#         l = lexer.new(input)
#         p = parser.new(l)
#         program = p.parse_program()
#         self.check_parsererrors(p)
#         if program == None:
#             self.fail('parse_program returned None')
#         if len(program.statements) != 3:
#             self.fail('program.statements does not contain 3 statements got{}'.format(len(program.statements)))
#
#         class ExpectedStatements:
#             def __init__(self, expect_identifier: str) -> None:
#                 self.expect_identifier = expect_identifier
#
#         tests = [
#             ExpectedStatements('x'),
#             ExpectedStatements('y'),
#             ExpectedStatements('foobar'),
#         ]
#         for i, tt in enumerate(tests):
#             stmt = program.statements[i]
#             if self.__test_letstatement(stmt, tt.expect_identifier):
#                 return
#
#     def __test_letstatement(self, s: Type[Statement], name: str) -> bool:
#         if s.token_literal() != 'let':
#             print("s.token_literal not 'let'. got={}".format(s.token_literal()))
#             return False
#
#         if not isinstance(s, LetStatement):
#             print("s not *ast.LetStatement. got={}".format(type(s)))
#             return False
#         if s.name.value != name:
#             print("let_stmt.name.value not {}. got={}".format(name, s.name.value))
#             return False
#         if s.name.token_literal() != name:
#             print("let_stmt.name.token_literal not {}. got={}".format(name, s.name.token_literal()))
#             return False
#         return True

class TestLetStatements(unittest.TestCase):
    def test_letstatement(self):
        LetTest = namedtuple('LetTest', ['input', 'expected_identifier',
                                         'expected_value'])
        tests = [LetTest('let x = 5;', 'x', 5),
                 LetTest('let y = true;', 'y', True),
                 LetTest('let foobar = y;', 'foobar', 'y')
                 ]
        for tt in tests:
            l = lexer.new(tt.input)
            p = parser.new(l)
            program = p.parse_program()
            self.check_parsererrors(p)
            if len(program.statements) != 1:
                self.fail('program.Statements does not contain 1 statements. got={}'.format(len(program.statements)))
            stmt = program.statements[0]

            if not self.__test_letstatement(stmt, tt.expected_identifier):
                return None
            val = stmt.value
            if not self.check_literalexpression(val, tt.expected_value):
                return None

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
            if self.__test_letstatement(stmt, tt.expect_identifier):
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

    def check_parsererrors(self, p: parser.Parser) -> None:
        errs = p.errors()
        if len(errs) == 0:
            return
        print('parser has {} errors'.format(len(errs)))
        for e in errs:
            print('parser error: {}'.format(e))
        self.fail('parser error.')

    def check_literalexpression(self, exp: Expression, expected) -> bool:
        if type(expected) == int:
            return self.check_integer_literal(exp, expected)
        elif type(expected) == str:
            return self.check_identifier(exp, expected)
        elif type(expected) == bool:
            return self.check_booleanliteral(exp, expected)
        print('type of exp not handled. got={}'.format(type(exp)))
        return False

    def check_booleanliteral(self, exp: Expression, value: bool) -> bool:
        if not isinstance(exp, Boolean):
            print('exp not *ast.Boolean. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('bo.Value not {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != str(value).lower():
            print('bo.TokenLiteral not {}. got={}'.format(value, exp.token_literal()))
            return False

    def check_identifier(self, exp: Expression, value: str) -> bool:
        if not isinstance(exp, Identifier):
            print('exp not *ast.Identifier. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('ident.Value not {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != value:
            print('ident.TokenLiteral not {}. got={}'.format(value, exp.token_literal()))
            return False
        return True

    def check_integer_literal(self, il: Expression, value: int) -> bool:
        if not isinstance(il, IntegerLiteral):
            self.fail('il not *ast.IntegerLiteral. got={}'.format(type(il)))
            return False
        if il.value != value:
            print('"integ.Value not {}. got={}'.format(value, il.value))
            return False
        if il.token_literal() != str(value):
            print('integ.TokenLiteral not {}. got={}'.format(value, il.token_literal()))
            return False
        return True


class TestReturnStatement(unittest.TestCase):
    def test_returnstatement(self):
        input = '''
        return 5;
        return 10;
        return 993322;
        '''
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        self.check_parsererrors(p)
        if len(program.statements) != 3:
            self.fail('program.Statements does not contain 3 statements. got={}'.format(len(program.statements)))

        for stmt in program.statements:
            if not type(stmt) == ReturnStatement:
                print('stmt not *ast.returnStatement. got={}'.format(type(stmt)))
                continue
            if stmt.token_literal() != 'return':
                print('returnStmt.TokenLiteral not return, got {}'.format(stmt.token_literal()))

    def check_parsererrors(self, p: parser.Parser) -> None:
        errs = p.errors()
        if len(errs) == 0:
            return
        print('parser has {} errors'.format(len(errs)))
        for e in errs:
            print('parser error: {}'.format(e))
        self.fail('parser error.')


class TestIdentifierExpression(unittest.TestCase):
    def test_identifier_expression(self):
        input = '''
                foobar;
                '''
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        self.check_parsererrors(p)
        if len(program.statements) != 1:
            self.fail('program has not enough statements. got={}'.format(len(program.statements)))
        stmt = program.statements[0]
        if not isinstance(stmt, ExpressionStatement):
            self.fail('program.Statements[0] is not ast.ExpressionStatement. got={}'.format(type(stmt)))
        ident = stmt.expression
        if not isinstance(ident, Identifier):
            self.fail('exp not ast.Identifier. got={}'.format(type(ident)))
        if ident.value != 'foobar':
            print('ident.Value not {}. got={}'.format('foobar', ident.value))
        if ident.token_literal() != 'foobar':
            print('ident.TokenLiteral not {}. got={}'.format('foobar', ident.token_literal()))

    def check_parsererrors(self, p: parser.Parser) -> None:
        errs = p.errors()
        if len(errs) == 0:
            return
        print('parser has {} errors'.format(len(errs)))
        for e in errs:
            print('parser error: {}'.format(e))
        self.fail('parser error.')


class TestIntegerLiteralExpression(unittest.TestCase):
    def test_integerliteral_expression(self):
        input = '''
                5;
                '''
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        self.check_parsererrors(p)
        if len(program.statements) != 1:
            self.fail('program has not enough statements. got={}'.format(len(program.statements)))
        stmt = program.statements[0]
        if not isinstance(stmt, ExpressionStatement):
            self.fail('program.Statements[0] is not ast.ExpressionStatement. got={}'.format(type(stmt)))
        literal = stmt.expression
        if not isinstance(literal, IntegerLiteral):
            self.fail('exp not ast.IntegerLiteral. got={}'.format(type(literal)))
        if literal.value != 5:
            print('ident.Value not {}. got={}'.format(5, literal.value))
        if literal.token_literal() != '5':
            print('ident.TokenLiteral not {}. got={}'.format('5', literal.token_literal()))

    def check_parsererrors(self, p: parser.Parser) -> None:
        errs = p.errors()
        if len(errs) == 0:
            return
        print('parser has {} errors'.format(len(errs)))
        for e in errs:
            print('parser error: {}'.format(e))
        self.fail('parser error.')


class TestParsingPrefixExpressions(unittest.TestCase):
    def test_parsingprefix_expression(self):
        ParsPrefixTest = namedtuple('ParsPrefixTest', ['input', 'operator', 'integer_value'])
        prefix_tests = [ParsPrefixTest(input="!5;", operator='!', integer_value=5),
                        ParsPrefixTest(input="-15;", operator="-", integer_value=15)]
        for tt in prefix_tests:
            l = lexer.new(tt.input)
            p = parser.new(l)
            program = p.parse_program()
            self.check_parsererrors(p)
            if len(program.statements) != 1:
                self.fail('program has not enough statements. got={}'.format(len(program.statements)))
            stmt = program.statements[0]
            if not isinstance(stmt, ExpressionStatement):
                self.fail('program.Statements[0] is not ast.ExpressionStatement. got={}'.format(type(stmt)))
            exp = stmt.expression
            if not isinstance(exp, PrefixExpression):
                self.fail('exp not ast.PrefixExpression. got={}'.format(type(exp)))
            if exp.operator != tt.operator:
                print('exp.Operator is not {}. got={}'.format(exp.operator, tt.operator))
            if not self.check_integer_literal(exp.right, tt.integer_value):
                return None

    def check_integer_literal(self, il: Expression, value: int) -> bool:
        if not isinstance(il, IntegerLiteral):
            print('il not *ast.IntegerLiteral. got={}'.format(type(il)))
            return False
        if il.value != value:
            print('"integ.Value not {}. got={}'.format(value, il.value))
            return False
        if il.token_literal() != str(value):
            print('integ.TokenLiteral not {}. got={}'.format(value, il.token_literal()))
            return False
        return True

    def check_parsererrors(self, p: parser.Parser) -> None:
        errs = p.errors()
        if len(errs) == 0:
            return
        print('parser has {} errors'.format(len(errs)))
        for e in errs:
            print('parser error: {}'.format(e))
        self.fail('parser error.')


class TestParsingInfixExpressions(unittest.TestCase):

    def test_parsinginfix_expression(self):
        ParsInfixTest = namedtuple('ParsInfixTest', ['input', 'left_value', 'operator', 'right_value'])
        infix_tests = [ParsInfixTest("5 + 5;", 5, "+", 5),
                       ParsInfixTest("5 - 5;", 5, "-", 5),
                       ParsInfixTest("5 * 5;", 5, "*", 5),
                       ParsInfixTest("5 / 5;", 5, "/", 5),
                       ParsInfixTest("5 > 5;", 5, ">", 5),
                       ParsInfixTest("5 < 5;", 5, "<", 5),
                       ParsInfixTest("5 == 5;", 5, "==", 5),
                       ParsInfixTest("5 != 5;", 5, "!=", 5),
                       ParsInfixTest("true == true;", True, "==", True),
                       ParsInfixTest("true != false;", True, "!=", False),
                       ParsInfixTest("false == false;", False, "==", False),
                       ]

        for tt in infix_tests:
            l = lexer.new(tt.input)
            p = parser.new(l)
            program = p.parse_program()
            self.check_parsererrors(p)
            if len(program.statements) != 1:
                self.fail('program has not enough statements. got={}'.format(len(program.statements)))
            stmt = program.statements[0]
            if not isinstance(stmt, ExpressionStatement):
                self.fail('program.Statements[0] is not ast.ExpressionStatement. got={}'.format(type(stmt)))
            exp = stmt.expression
            # if not isinstance(exp, InfixExpression):
            #     self.fail('exp not ast.InfixExpression. got={}'.format(type(exp)))
            # if not self.check_integer_literal(exp.left, tt.left_value):
            #     return None
            # if exp.operator != tt.operator:
            #     print('exp.Operator is not {}. got={}'.format(exp.operator, tt.operator))
            # if not self.check_integer_literal(exp.right, tt.right_value):
            #     return None
            if not self.check_infixexpression(exp, tt.left_value, tt.operator, tt.right_value):
                return

    def check_infixexpression(self, exp: Expression, left, operator, right) -> bool:
        if not isinstance(exp, InfixExpression):
            print('exp is not ast.OperatorExpression. got={}({})'.format(exp, exp))
            return False
        if not self.check_literalexpression(exp.left, left):
            return False
        if exp.operator != operator:
            print('exp.Operator is not {}. got={}'.format(operator, exp.operator))
            return False
        if not self.check_literalexpression(exp.right, right):
            return False
        return True

    def check_literalexpression(self, exp: Expression, expected) -> bool:
        if type(expected) == int:
            return self.check_integer_literal(exp, expected)
        elif type(expected) == str:
            return self.check_identifier(exp, expected)
        elif type(expected) == bool:
            return self.check_booleanliteral(exp, expected)
        print('type of exp not handled. got={}'.format(type(exp)))
        return False

    def check_booleanliteral(self, exp: Expression, value: bool) -> bool:
        if not isinstance(exp, Boolean):
            print('exp not *ast.Boolean. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('bo.Value not {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != str(value).lower():
            print('bo.TokenLiteral not {}. got={}'.format(value, exp.token_literal()))
            return False

    def check_identifier(self, exp: Expression, value: str) -> bool:
        if not isinstance(exp, Identifier):
            print('exp not *ast.Identifier. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('ident.Value not {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != value:
            print('ident.TokenLiteral not {}. got={}'.format(value, exp.token_literal()))
            return False
        return True

    def check_integer_literal(self, il: Expression, value: int) -> bool:
        if not isinstance(il, IntegerLiteral):
            self.fail('il not *ast.IntegerLiteral. got={}'.format(type(il)))
            return False
        if il.value != value:
            print('"integ.Value not {}. got={}'.format(value, il.value))
            return False
        if il.token_literal() != str(value):
            print('integ.TokenLiteral not {}. got={}'.format(value, il.token_literal()))
            return False
        return True

    def check_parsererrors(self, p: parser.Parser) -> None:
        errs = p.errors()
        if len(errs) == 0:
            return
        print('parser has {} errors'.format(len(errs)))
        for e in errs:
            print('parser error: {}'.format(e))
        self.fail('parser error.')


class TestOperatorPrecedenceParsing(unittest.TestCase):
    def test_operator_precedence(self):
        OperatorTest = namedtuple('OperatorTest', ['input', 'expected'])
        tests = [OperatorTest("-a * b;", "((-a) * b)"),
                 OperatorTest("!-a;", "(!(-a))"),
                 OperatorTest("a + b + c;", "((a + b) + c)"),
                 OperatorTest("a + b - c;", "((a + b) - c)"),
                 OperatorTest("a * b * c;", "((a * b) * c)"),
                 OperatorTest("a * b / c;", "((a * b) / c)"),
                 OperatorTest("a + b / c;", "(a + (b / c))"),
                 OperatorTest("a + b * c + d / e - f;", "(((a + (b * c)) + (d / e)) - f)"),
                 OperatorTest("3 + 4; -5 * 5;", "(3 + 4)((-5) * 5)"),
                 OperatorTest("5 > 4 == 3 < 4;", "((5 > 4) == (3 < 4))"),
                 OperatorTest("5 < 4 != 3 > 4;", "((5 < 4) != (3 > 4))"),
                 OperatorTest("3 + 4 * 5 == 3 * 1 + 4 * 5;", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"),
                 OperatorTest("3 + 4 * 5 == 3 * 1 + 4 * 5;", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"),
                 OperatorTest("true;", "true"),
                 OperatorTest("false;", "false"),
                 OperatorTest("3 > 5 == false;", "((3 > 5) == false)"),
                 OperatorTest("3 < 5 == true;", "((3 < 5) == true)"),

                 OperatorTest("1 + (2 + 3) + 4;", "((1 + (2 + 3)) + 4)"),
                 OperatorTest("(5 + 5) * 2;", "((5 + 5) * 2)"),
                 OperatorTest("2 / (5 + 5);", "(2 / (5 + 5))"),
                 OperatorTest("-(5 + 5);", "(-(5 + 5))"),
                 OperatorTest("!(true == true);", "(!(true == true))"),

                 OperatorTest("a + add(b * c) + d;", "((a + add((b * c))) + d)"),
                 OperatorTest("add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8));",
                              "add(a, b, 1, (2 * 3), (4 + 5), add(6, (7 * 8)))"),
                 OperatorTest("add(a + b + c * d / f + g);", "add((((a + b) + ((c * d) / f)) + g))")
                 ]

        for tt in tests:
            l = lexer.new(tt.input)
            p = parser.new(l)
            program = p.parse_program()
            self.check_parsererrors(p)
            actual = program.string()
            if actual != tt.expected:
                print('expected={}, got={}'.format(tt.expected, actual))

    def check_parsererrors(self, p: parser.Parser) -> None:
        errs = p.errors()
        if len(errs) == 0:
            return
        print('parser has {} errors'.format(len(errs)))
        for e in errs:
            print('parser error: {}'.format(e))
        self.fail('parser error.')


class TestBooleanExpression(unittest.TestCase):
    def test_booleanexpression(self):
        BoolTest = namedtuple('BoolTest', ['input', 'expected_boolean'])
        tests = [BoolTest("true;", True),
                 BoolTest("false;", False)]
        for tt in tests:
            l = lexer.new(tt.input)
            p = parser.new(l)
            program = p.parse_program()
            self.check_parsererrors(p)

            if len(program.statements) != 1:
                self.fail('program has not enough statements. got={}'.format(len(program.statements)))
            stmt = program.statements[0]
            if not isinstance(stmt, ExpressionStatement):
                self.fail('program.Statements[0] is not ast.ExpressionStatement. got={}'.format(type(stmt)))
            boolean = stmt.expression
            if not isinstance(boolean, Boolean):
                self.fail('boolean not ast.Boolean. got={}'.format(type(boolean)))
            if boolean.value != tt.expected_boolean:
                print('boolean.Value not {}. got={}'.format(tt.expected_boolean, boolean.value))

    def check_parsererrors(self, p: parser.Parser) -> None:
        errs = p.errors()
        if len(errs) == 0:
            return
        print('parser has {} errors'.format(len(errs)))
        for e in errs:
            print('parser error: {}'.format(e))
        self.fail('parser error.')


class TestIfExpression(unittest.TestCase):
    def test_ifexpression(self):
        input = '''
                if (x < y) { x };
                '''
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        self.check_parsererrors(p)
        if len(program.statements) != 1:
            self.fail('program.Body does not contain {} statements. got={}\n'.format(1, len(program.statements)))
        stmt = program.statements[0]
        if not isinstance(stmt, ExpressionStatement):
            self.fail('program.Statements[0] is not ast.ExpressionStatement. got={}'.format(type(stmt)))
        exp = stmt.expression
        if not isinstance(exp, IfExpression):
            self.fail('exp not ast.IfExpression. got={}'.format(type(exp)))
        if not self.check_infixexpression(exp.conditioin, 'x', '<', 'y'):
            return None
        if len(exp.consequence.statements) != 1:
            print('consequence is not 1 statements. got={}\n'.format(len(exp.consequence.statements)))
        consequence = exp.consequence.statements[0]
        if not isinstance(consequence, ExpressionStatement):
            print('Statements[0] is not ast.ExpressionStatement. got={}'.format(type(consequence)))
        if not self.check_identifier(consequence.expression, 'x'):
            return None
        if exp.alternative:
            print('exp.Alternative.Statements was not nil. got={}'.format(exp.alternative))

    def check_parsererrors(self, p: parser.Parser) -> None:
        errs = p.errors()
        if len(errs) == 0:
            return
        print('parser has {} errors'.format(len(errs)))
        for e in errs:
            print('parser error: {}'.format(e))
        self.fail('parser error.')

    def check_infixexpression(self, exp: Expression, left, operator, right) -> bool:
        if not isinstance(exp, InfixExpression):
            print('exp is not ast.OperatorExpression. got={}({})'.format(exp, exp))
            return False
        if not self.check_literalexpression(exp.left, left):
            return False
        if exp.operator != operator:
            print('exp.Operator is not {}. got={}'.format(operator, exp.operator))
            return False
        if not self.check_literalexpression(exp.right, right):
            return False
        return True

    def check_identifier(self, exp: Expression, value: str) -> bool:
        if not isinstance(exp, Identifier):
            print('exp not *ast.Identifier. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('ident.Value not {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != value:
            print('ident.TokenLiteral not {}. got={}'.format(value, exp.token_literal()))
            return False
        return True

    def check_literalexpression(self, exp: Expression, expected) -> bool:
        if type(expected) == int:
            return self.check_integer_literal(exp, expected)
        elif type(expected) == str:
            return self.check_identifier(exp, expected)
        elif type(expected) == bool:
            return self.check_booleanliteral(exp, expected)
        print('type of exp not handled. got={}'.format(type(exp)))
        return False

    def check_booleanliteral(self, exp: Expression, value: bool) -> bool:
        if not isinstance(exp, Boolean):
            print('exp not *ast.Boolean. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('bo.Value not {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != str(value).lower():
            print('bo.TokenLiteral not {}. got={}'.format(value, exp.token_literal()))
            return False

    def check_identifier(self, exp: Expression, value: str) -> bool:
        if not isinstance(exp, Identifier):
            print('exp not *ast.Identifier. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('ident.Value not {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != value:
            print('ident.TokenLiteral not {}. got={}'.format(value, exp.token_literal()))
            return False
        return True

    def check_integer_literal(self, il: Expression, value: int) -> bool:
        if not isinstance(il, IntegerLiteral):
            self.fail('il not *ast.IntegerLiteral. got={}'.format(type(il)))
            return False
        if il.value != value:
            print('"integ.Value not {}. got={}'.format(value, il.value))
            return False
        if il.token_literal() != str(value):
            print('integ.TokenLiteral not {}. got={}'.format(value, il.token_literal()))
            return False
        return True


class TestIfElseExpression(unittest.TestCase):
    def test_ifelse_expression(self):
        input = '''
                if (x < y) { x } else { y };
                '''
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        self.check_parsererrors(p)
        if len(program.statements) != 1:
            self.fail('program.Body does not contain {} statements. got={}\n'.format(1, len(program.statements)))
        stmt = program.statements[0]
        if not isinstance(stmt, ExpressionStatement):
            self.fail('program.Statements[0] is not ast.ExpressionStatement. got={}'.format(type(stmt)))
        exp = stmt.expression
        if not isinstance(exp, IfExpression):
            self.fail('exp not ast.IfExpression. got={}'.format(type(exp)))
        if not self.check_infixexpression(exp.conditioin, 'x', '<', 'y'):
            return None
        if len(exp.consequence.statements) != 1:
            print('consequence is not 1 statements. got={}\n'.format(len(exp.consequence.statements)))
        consequence = exp.consequence.statements[0]
        if not isinstance(consequence, ExpressionStatement):
            print('Statements[0] is not ast.ExpressionStatement. got={}'.format(type(consequence)))
        if not self.check_identifier(consequence.expression, 'x'):
            return None
        if len(exp.alternative.statements) != 1:
            print('exp.Alternative.Statements does not contain 1 statements. got={}\n'.format(
                len(exp.alternative.statements)))
        alternative = exp.alternative.statements[0]
        if not isinstance(alternative, ExpressionStatement):
            self.fail('Statements[0] is not ast.ExpressionStatement. got={}'.format(type(alternative)))
        if not self.check_identifier(alternative.expression, 'y'):
            return None

    def check_parsererrors(self, p: parser.Parser) -> None:
        errs = p.errors()
        if len(errs) == 0:
            return
        print('parser has {} errors'.format(len(errs)))
        for e in errs:
            print('parser error: {}'.format(e))
        self.fail('parser error.')

    def check_infixexpression(self, exp: Expression, left, operator, right) -> bool:
        if not isinstance(exp, InfixExpression):
            print('exp is not ast.OperatorExpression. got={}({})'.format(exp, exp))
            return False
        if not self.check_literalexpression(exp.left, left):
            return False
        if exp.operator != operator:
            print('exp.Operator is not {}. got={}'.format(operator, exp.operator))
            return False
        if not self.check_literalexpression(exp.right, right):
            return False
        return True

    def check_identifier(self, exp: Expression, value: str) -> bool:
        if not isinstance(exp, Identifier):
            print('exp not *ast.Identifier. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('ident.Value not {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != value:
            print('ident.TokenLiteral not {}. got={}'.format(value, exp.token_literal()))
            return False
        return True

    def check_literalexpression(self, exp: Expression, expected) -> bool:
        if type(expected) == int:
            return self.check_integer_literal(exp, expected)
        elif type(expected) == str:
            return self.check_identifier(exp, expected)
        elif type(expected) == bool:
            return self.check_booleanliteral(exp, expected)
        print('type of exp not handled. got={}'.format(type(exp)))
        return False

    def check_booleanliteral(self, exp: Expression, value: bool) -> bool:
        if not isinstance(exp, Boolean):
            print('exp not *ast.Boolean. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('bo.Value not {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != str(value).lower():
            print('bo.TokenLiteral not {}. got={}'.format(value, exp.token_literal()))
            return False

    def check_identifier(self, exp: Expression, value: str) -> bool:
        if not isinstance(exp, Identifier):
            print('exp not *ast.Identifier. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('ident.Value not {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != value:
            print('ident.TokenLiteral not {}. got={}'.format(value, exp.token_literal()))
            return False
        return True

    def check_integer_literal(self, il: Expression, value: int) -> bool:
        if not isinstance(il, IntegerLiteral):
            self.fail('il not *ast.IntegerLiteral. got={}'.format(type(il)))
            return False
        if il.value != value:
            print('"integ.Value not {}. got={}'.format(value, il.value))
            return False
        if il.token_literal() != str(value):
            print('integ.TokenLiteral not {}. got={}'.format(value, il.token_literal()))
            return False
        return True


class TestFunctionLiteralParsing(unittest.TestCase):
    def test_functionliteral_parsing(self):
        input = '''
                fn(x, y) { x + y; };
                '''
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        self.check_parsererrors(p)
        if len(program.statements) != 1:
            self.fail('program.Body does not contain {} statements. got={}\n'.format(1, len(program.statements)))
        stmt = program.statements[0]
        if not isinstance(stmt, ExpressionStatement):
            self.fail('program.Statements[0] is not ast.ExpressionStatement. got={}'.format(type(stmt)))
        function = stmt.expression
        if not isinstance(function, FunctionLiteral):
            self.fail('exp not ast.FunctionLiteral. got={}'.format(type(function)))
        if len(function.parameters) != 2:
            print('function literal parameters wrong. want 2, got={}\n'.format(len(function.parameters)))
        self.check_literalexpression(function.parameters[0], 'x')
        self.check_literalexpression(function.parameters[1], 'y')
        if len(function.body.statements) != 1:
            print('function.Body.Statements has not 1 statements. got={}\n'.format(len(function.body.statements)))

        body_stmt = function.body.statements[0]
        if not isinstance(body_stmt, ExpressionStatement):
            self.fail('function body stmt is not ast.ExpressionStatement. got={}'.format(type(body_stmt)))
            return None
        self.check_infixexpression(body_stmt.expression, 'x', '+', 'y')

    def check_parsererrors(self, p: parser.Parser) -> None:
        errs = p.errors()
        if len(errs) == 0:
            return
        print('parser has {} errors'.format(len(errs)))
        for e in errs:
            print('parser error: {}'.format(e))
        self.fail('parser error.')

    def check_infixexpression(self, exp: Expression, left, operator, right) -> bool:
        if not isinstance(exp, InfixExpression):
            print('exp is not ast.OperatorExpression. got={}({})'.format(exp, exp))
            return False
        if not self.check_literalexpression(exp.left, left):
            return False
        if exp.operator != operator:
            print('exp.Operator is not {}. got={}'.format(operator, exp.operator))
            return False
        if not self.check_literalexpression(exp.right, right):
            return False
        return True

    def check_identifier(self, exp: Expression, value: str) -> bool:
        if not isinstance(exp, Identifier):
            print('exp not *ast.Identifier. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('ident.Value not {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != value:
            print('ident.TokenLiteral not {}. got={}'.format(value, exp.token_literal()))
            return False
        return True

    def check_literalexpression(self, exp: Expression, expected) -> bool:
        if type(expected) == int:
            return self.check_integer_literal(exp, expected)
        elif type(expected) == str:
            return self.check_identifier(exp, expected)
        elif type(expected) == bool:
            return self.check_booleanliteral(exp, expected)
        print('type of exp not handled. got={}'.format(type(exp)))
        return False

    def check_booleanliteral(self, exp: Expression, value: bool) -> bool:
        if not isinstance(exp, Boolean):
            print('exp not *ast.Boolean. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('bo.Value not {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != str(value).lower():
            print('bo.TokenLiteral not {}. got={}'.format(value, exp.token_literal()))
            return False

    def check_identifier(self, exp: Expression, value: str) -> bool:
        if not isinstance(exp, Identifier):
            print('exp not *ast.Identifier. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('ident.Value not {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != value:
            print('ident.TokenLiteral not {}. got={}'.format(value, exp.token_literal()))
            return False
        return True

    def check_integer_literal(self, il: Expression, value: int) -> bool:
        if not isinstance(il, IntegerLiteral):
            self.fail('il not *ast.IntegerLiteral. got={}'.format(type(il)))
            return False
        if il.value != value:
            print('"integ.Value not {}. got={}'.format(value, il.value))
            return False
        if il.token_literal() != str(value):
            print('integ.TokenLiteral not {}. got={}'.format(value, il.token_literal()))
            return False
        return True


class TestFunctionParameterParsing(unittest.TestCase):
    def test_functionparams(self):
        Params = namedtuple('Params', ['input', 'expected_params'])
        tests = [Params('fn() {};', []),
                 Params('fn(x) {};', ['x']),
                 Params('fn(x, y, z) {};', ['x', 'y', 'z']),
                 ]
        for tt in tests:
            l = lexer.new(tt.input)
            p = parser.new(l)
            program = p.parse_program()
            self.check_parsererrors(p)
            stmt = program.statements[0]
            function = stmt.expression
            if len(function.parameters) != len(tt.expected_params):
                self.fail('length parameters wrong. want {}, got={}\n'.format(len(tt.expected_params),
                                                                              len(function.parameters)))
            for i, ident in enumerate(tt.expected_params):
                self.check_literalexpression(function.parameters[i], ident)

    def check_parsererrors(self, p: parser.Parser) -> None:
        errs = p.errors()
        if len(errs) == 0:
            return
        print('parser has {} errors'.format(len(errs)))
        for e in errs:
            print('parser error: {}'.format(e))
        self.fail('parser error.')

    def check_literalexpression(self, exp: Expression, expected) -> bool:
        if type(expected) == int:
            return self.check_integer_literal(exp, expected)
        elif type(expected) == str:
            return self.check_identifier(exp, expected)
        elif type(expected) == bool:
            return self.check_booleanliteral(exp, expected)
        print('type of exp not handled. got={}'.format(type(exp)))
        return False

    def check_booleanliteral(self, exp: Expression, value: bool) -> bool:
        if not isinstance(exp, Boolean):
            print('exp not *ast.Boolean. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('bo.Value not {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != str(value).lower():
            print('bo.TokenLiteral not {}. got={}'.format(value, exp.token_literal()))
            return False

    def check_identifier(self, exp: Expression, value: str) -> bool:
        if not isinstance(exp, Identifier):
            print('exp not *ast.Identifier. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('ident.Value not {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != value:
            print('ident.TokenLiteral not {}. got={}'.format(value, exp.token_literal()))
            return False
        return True

    def check_integer_literal(self, il: Expression, value: int) -> bool:
        if not isinstance(il, IntegerLiteral):
            self.fail('il not *ast.IntegerLiteral. got={}'.format(type(il)))
            return False
        if il.value != value:
            print('"integ.Value not {}. got={}'.format(value, il.value))
            return False
        if il.token_literal() != str(value):
            print('integ.TokenLiteral not {}. got={}'.format(value, il.token_literal()))
            return False
        return True


class TestCallExpressionParsing(unittest.TestCase):
    def test_callexpression(self):
        input = 'add(1, 2 * 3, 4 + 5);'
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        self.check_parsererrors(p)

        if len(program.statements) != 1:
            self.fail('program.Statements does not contain {} statements. got={}\n'.format(1, len(program.statements)))
        stmt = program.statements[0]
        if not isinstance(stmt, ExpressionStatement):
            self.fail('stmt is not ast.ExpressionStatement. got={}'.format(type(stmt)))
        exp = stmt.expression
        if not isinstance(exp, CallExpression):
            self.fail('stmt.Expression is not ast.CallExpression. got={}'.format(type(exp)))
        if not self.check_identifier(exp.function, 'add'):
            return
        if len(exp.arguments) != 3:
            self.fail('wrong length of arguments. got={}'.format(len(exp.arguments)))
        self.check_literalexpression(exp.arguments[0], 1)
        self.check_infixexpression(exp.arguments[1], 2, '*', 3)
        self.check_infixexpression(exp.arguments[2], 4, '+', 5)

    def check_parsererrors(self, p: parser.Parser) -> None:
        errs = p.errors()
        if len(errs) == 0:
            return
        print('parser has {} errors'.format(len(errs)))
        for e in errs:
            print('parser error: {}'.format(e))
        self.fail('parser error.')

    def check_literalexpression(self, exp: Expression, expected) -> bool:
        if type(expected) == int:
            return self.check_integer_literal(exp, expected)
        elif type(expected) == str:
            return self.check_identifier(exp, expected)
        elif type(expected) == bool:
            return self.check_booleanliteral(exp, expected)
        print('type of exp not handled. got={}'.format(type(exp)))
        return False

    def check_booleanliteral(self, exp: Expression, value: bool) -> bool:
        if not isinstance(exp, Boolean):
            print('exp not *ast.Boolean. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('bo.Value not {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != str(value).lower():
            print('bo.TokenLiteral not {}. got={}'.format(value, exp.token_literal()))
            return False

    def check_identifier(self, exp: Expression, value: str) -> bool:
        if not isinstance(exp, Identifier):
            print('exp not *ast.Identifier. got={}'.format(type(exp)))
            return False
        if exp.value != value:
            print('ident.Value not {}. got={}'.format(value, exp.value))
            return False
        if exp.token_literal() != value:
            print('ident.TokenLiteral not {}. got={}'.format(value, exp.token_literal()))
            return False
        return True

    def check_integer_literal(self, il: Expression, value: int) -> bool:
        if not isinstance(il, IntegerLiteral):
            self.fail('il not *ast.IntegerLiteral. got={}'.format(type(il)))
            return False
        if il.value != value:
            print('"integ.Value not {}. got={}'.format(value, il.value))
            return False
        if il.token_literal() != str(value):
            print('integ.TokenLiteral not {}. got={}'.format(value, il.token_literal()))
            return False
        return True

    def check_infixexpression(self, exp: Expression, left, operator, right) -> bool:
        if not isinstance(exp, InfixExpression):
            print('exp is not ast.OperatorExpression. got={}({})'.format(exp, exp))
            return False
        if not self.check_literalexpression(exp.left, left):
            return False
        if exp.operator != operator:
            print('exp.Operator is not {}. got={}'.format(operator, exp.operator))
            return False
        if not self.check_literalexpression(exp.right, right):
            return False
        return True


if __name__ == '__main__':
    unittest.main()
