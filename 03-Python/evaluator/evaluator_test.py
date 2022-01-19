import unittest
from collections import namedtuple
from typing import Type
import lexer
import object
import evaluator
import parser
import environment


class TestEvalIntegerExpression(unittest.TestCase):
    def test_evalintegerexpression(self):
        EvalInt = namedtuple('EvalInt', ['input', 'expected'])
        tests = [EvalInt('5;', 5),
                 EvalInt('10;', 10),
                 EvalInt('-10;', -10),
                 EvalInt('-5;', -5),
                 EvalInt('5 + 5 + 5 + 5 - 10;', 10),
                 EvalInt('2 * 2 * 2 * 2 * 2;', 32),
                 EvalInt('-50 + 100 + -50;', 0),
                 EvalInt('5 * 2 + 10;', 20),
                 EvalInt('5 + 2 * 10;', 25),
                 EvalInt('20 + 2 * -10;', 0),
                 EvalInt('50 / 2 * 2 + 10;', 60),
                 EvalInt('2 * (5 + 10);', 30),
                 EvalInt('3 * 3 * 3 + 10;', 37),
                 EvalInt('3 * (3 * 3) + 10;', 37),
                 EvalInt('(5 + 10 * 2 + 15 / 3) * 2 + -10;', 50)
                 ]
        for tt in tests:
            evaled = self.check_eval(tt.input)
            self.check_integerobject(evaled, tt.expected)

    def check_eval(self, input: str) -> object.Object:
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        env = environment.new_environment()
        return evaluator.evals(program, env)

    def check_integerobject(self, obj: object.Object, expected: int) -> bool:
        if not isinstance(obj, object.Integer):
            print('object is not Integer. got={} ({})'.format(type(obj), obj))
            return False
        if obj.value != expected:
            print('object has wrong value. got={}, want={}'.format(obj.value, expected))
            return False
        return True


class TestEvalBooleanExpression(unittest.TestCase):
    def test_evalbooleanexpression(self):
        EvalInt = namedtuple('EvalInt', ['input', 'expected'])
        tests = [EvalInt('true;', True),
                 EvalInt('false;', False),
                 EvalInt('1<2;', True),
                 EvalInt('1>2;', False),
                 EvalInt('1<1;', False),
                 EvalInt('1>1;', False),
                 EvalInt('1==1;', True),
                 EvalInt('1!=1;', False),
                 EvalInt('1==2;', False),
                 EvalInt('1!=2;', True),

                 EvalInt('true==true;', True),
                 EvalInt('false==false;', True),
                 EvalInt('true==false;', False),
                 EvalInt('false==true;', False),
                 EvalInt('false!=true;', True),
                 EvalInt('true!=false;', True),
                 EvalInt('(1 < 2) == true;', True),
                 EvalInt('(1 < 2) == false;', False),
                 EvalInt('(1 > 2) == true;', False),
                 EvalInt('(1 > 2) == false;', True),
                 ]
        for tt in tests:
            evaled = self.check_eval(tt.input)
            self.check_booleanobject(evaled, tt.expected)

    def check_eval(self, input: str) -> object.Object:
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        env = environment.new_environment()
        return evaluator.evals(program, env)

    def check_booleanobject(self, obj: object.Object, expected: bool) -> bool:
        if not isinstance(obj, object.Boolean):
            print('object is not Boolean. got={} ({})'.format(type(obj), obj))
            return False
        if obj.value != expected:
            print('object has wrong value. got={}, want={}'.format(obj.value, expected))
            return False
        return True


class TestBangOperator(unittest.TestCase):
    def test_bang_operator(self):
        EvalInt = namedtuple('EvalInt', ['input', 'expected'])
        tests = [EvalInt('!true;', False),
                 EvalInt('!false;', True),
                 EvalInt('!5;', False),
                 EvalInt('!!true;', True),
                 EvalInt('!!false;', False),
                 EvalInt('!!5;', True)
                 ]
        for tt in tests:
            evaled = self.check_eval(tt.input)
            self.check_booleanobject(evaled, tt.expected)

    def check_eval(self, input: str) -> object.Object:
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        env = environment.new_environment()
        return evaluator.evals(program, env)

    def check_booleanobject(self, obj: object.Object, expected: bool) -> bool:
        if not isinstance(obj, object.Boolean):
            print('object is not Boolean. got={} ({})'.format(type(obj), obj))
            return False
        if obj.value != expected:
            print('object has wrong value. got={}, want={}'.format(obj.value, expected))
            return False
        return True


class TestIfElseExpressions(unittest.TestCase):
    def test_ifelse_expression(self):
        EvalInt = namedtuple('EvalInt', ['input', 'expected'])
        tests = [EvalInt('if (true) { 10 };', 10),
                 EvalInt('if (false) { 10 };', None),
                 EvalInt('if (1) { 10 };', 10),
                 EvalInt('if (1 < 2) { 10 };', 10),
                 EvalInt('if (1 > 2) { 10 };', None),
                 EvalInt('if (1 > 2) { 10 } else { 20 };', 20),
                 EvalInt('if (1 < 2) { 10 } else { 20 };', 10)
                 ]
        for tt in tests:
            evaled = self.check_eval(tt.input)
            if isinstance(tt.expected, int):
                self.check_integerobject(evaled, tt.expected)
            else:
                self.check_nullobject(evaled)

    def check_eval(self, input: str) -> object.Object:
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        env = environment.new_environment()
        return evaluator.evals(program, env)

    def check_nullobject(self, obj: object.Object) -> bool:
        if obj != evaluator.NULL:
            print('object is not NULL. got={} ({})'.format(type(obj), obj))
            return False
        return True

    def check_integerobject(self, obj: object.Object, expected: int) -> bool:
        if not isinstance(obj, object.Integer):
            print('object is not Integer. got={} ({})'.format(type(obj), obj))
            return False
        if obj.value != expected:
            print('object has wrong value. got={}, want={}'.format(obj.value, expected))
            return False
        return True


class TestReturnStatements(unittest.TestCase):
    def test_return_stmts(self):
        EvalInt = namedtuple('EvalInt', ['input', 'expected'])
        tests = [
                 EvalInt('return 10;', 10),
                 EvalInt('return 10; {9};', 10),
                 EvalInt('9; return 2 * 5; 9;', 10),
                 EvalInt('if (10 > 1) { return 10; };', 10),
                 EvalInt('''
                 if (10 > 1) {
                  if (10 > 1) {
                    return 10;
                  }

                  return 1;
                };
                 ''', 10),
                #  EvalInt('''
                #          let f = fn(x) {
                #           return x;
                #           x + 10;
                #         };
                #         f(10);
                #          ''', 10),
                #  EvalInt('''
                # let f = fn(x) {
                #    let result = x + 10;
                #    return result;
                #    return 10;
                # };
                # f(10);
                # ''', 20),
                 ]
        for tt in tests:
            evaled = self.check_eval(tt.input)
            self.check_integerobject(evaled, tt.expected)

    def check_eval(self, input: str) -> object.Object:
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        env = environment.new_environment()
        return evaluator.evals(program, env)

    def check_integerobject(self, obj: object.Object, expected: int) -> bool:
        if not isinstance(obj, object.Integer):
            print('object is not Integer. got={} ({})'.format(type(obj), obj))
            return False
        if obj.value != expected:
            print('object has wrong value. got={}, want={}'.format(obj.value, expected))
            return False
        return True


class TestErrorHandling(unittest.TestCase):
    def test_error_handling(self):
        EvalInt = namedtuple('EvalInt', ['input', 'expected'])
        tests = [
                 EvalInt('5 + true;', 'type mismatch: INTEGER + BOOLEAN'),
                 EvalInt('5 + true; 5;', 'type mismatch: INTEGER + BOOLEAN'),
                 EvalInt('-true;', 'unknown operator: -BOOLEAN'),
                 EvalInt('true + false;', 'unknown operator: BOOLEAN + BOOLEAN'),
                 EvalInt('true + false + true + false;', 'unknown operator: BOOLEAN + BOOLEAN'),
                 EvalInt('5; true + false; 5;', 'unknown operator: BOOLEAN + BOOLEAN'),
                 EvalInt('if (10 > 1) { true + false; };', 'unknown operator: BOOLEAN + BOOLEAN'),
                 EvalInt('foobar;', 'identifier not found: foobar'),
                 EvalInt('''
                 if (10 > 1) {
  if (10 > 1) {
    return true + false;
  }

  return 1;
};
                 ''', 'unknown operator: BOOLEAN + BOOLEAN'),
                 ]
        for tt in tests:
            # print(tt.input)
            evaled = self.check_eval(tt.input)
            if not isinstance(evaled, object.Error):
                print('no error object returned. got={}({})'.format(type(evaled), evaled))
                continue
            if evaled.message != tt.expected:
                print('wrong error message. expected={}, got={}'.format(tt.expected, evaled.message))

    def check_eval(self, input: str) -> object.Object:
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        env = environment.new_environment()
        return evaluator.evals(program, env)


class TestLetStatements(unittest.TestCase):
    def test_let_stmts(self):
        EvalInt = namedtuple('EvalInt', ['input', 'expected'])
        tests = [
                 EvalInt('let a = 5; a;', 5),
                 EvalInt('let a = 5 * 5; a;', 25),
                 EvalInt('let a = 5; let b = a; b;', 5),
                 EvalInt('let a = 5; let b = a; let c = a + b + 5; c;', 15),
                 ]
        for tt in tests:
            self.check_integerobject(self.check_eval(tt.input),
                                              tt.expected)

    def check_eval(self, input: str) -> object.Object:
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        env = environment.new_environment()
        return evaluator.evals(program, env)

    def check_integerobject(self, obj: object.Object, expected: int) -> bool:
        if not isinstance(obj, object.Integer):
            print('object is not Integer. got={} ({})'.format(type(obj), obj))
            return False
        if obj.value != expected:
            print('object has wrong value. got={}, want={}'.format(obj.value, expected))
            return False
        return True


class TestFunctionObject(unittest.TestCase):
    def test_function_object(self):
        input = 'fn(x) { x + 2; };'
        evaluated = self.check_eval(input)
        if not isinstance(evaluated, object.Function):
            self.fail('object is not Function. got={} ({})'.format(type(evaluated), evaluated))
        if len(evaluated.parameters) !=1:
            self.fail('function has wrong parameters. Parameters={}'.format(evaluated.parameters))
        if evaluated.parameters[0].string() != 'x':
            self.fail('parameter is not x. got={}'.format(evaluated.parameters[0]))
        expected_body = '(x + 2)'
        if evaluated.body.string() != expected_body:
            self.fail('body is not {}. got={}'.format(expected_body, evaluated.body.string()))

    def check_eval(self, input: str) -> object.Object:
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        env = environment.new_environment()
        return evaluator.evals(program, env)


class TestFunctionApplication(unittest.TestCase):
    def test_function_app(self):
        EvalInt = namedtuple('EvalInt', ['input', 'expected'])
        tests = [
            EvalInt('let identity = fn(x) { x; }; identity(5);', 5),
            EvalInt('let identity = fn(x) { return x; }; identity(5);', 5),
            EvalInt('let double = fn(x) { x * 2; }; double(5);', 10),
            EvalInt('let add = fn(x, y) { x + y; }; add(5, 5);', 10),
            EvalInt('let add = fn(x, y) { x + y; }; add(5 + 5, add(5, 5));', 20),
            EvalInt('fn(x) { x; }(5)', 5),
        ]
        for tt in tests:
            self.check_integerobject(self.check_eval(tt.input),
                                     tt.expected)

    def check_eval(self, input: str) -> object.Object:
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        env = environment.new_environment()
        return evaluator.evals(program, env)

    def check_integerobject(self, obj: object.Object, expected: int) -> bool:
        if not isinstance(obj, object.Integer):
            print('object is not Integer. got={} ({})'.format(type(obj), obj))
            return False
        if obj.value != expected:
            print('object has wrong value. got={}, want={}'.format(obj.value, expected))
            return False
        return True


class TestClosures(unittest.TestCase):
    def test_closures(self):
        input = '''let newAdder = fn(x) { fn(y) { x + y } };
                 let addTwo = newAdder(2);
                 addTwo(2);
                '''
        self.check_integerobject(self.check_eval(input), 4)

    def check_integerobject(self, obj: object.Object, expected: int) -> bool:
        if not isinstance(obj, object.Integer):
            print('object is not Integer. got={} ({})'.format(type(obj), obj))
            return False
        if obj.value != expected:
            print('object has wrong value. got={}, want={}'.format(obj.value, expected))
            return False
        return True

    def check_eval(self, input: str) -> object.Object:
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        env = environment.new_environment()
        return evaluator.evals(program, env)


if __name__ == '__main__':
    unittest.main()