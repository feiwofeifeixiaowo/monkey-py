import unittest
from collections import namedtuple
from typing import Type, List, Dict
from lexer import lexer
from object import object
from evaluator import evaluator
from parser import parser
from object import environment


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
                 EvalInt('"Hello" - "World";', 'unknown operator: STRING - STRING'),
                 EvalInt('''
                 if (10 > 1) {
  if (10 > 1) {
    return true + false;
  }

  return 1;
};
                 ''', 'unknown operator: BOOLEAN + BOOLEAN'),
            EvalInt('{"name": "Monkey"}[fn(x) { x }];', 'unusable as hash key: FUNCTION'),
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


class TestStringLiteral(unittest.TestCase):
    def test_stringliteral(self):
        input = '''"Hello World!";
                '''
        evaled = self.check_eval(input)
        if not isinstance(evaled, object.String):
            self.fail('object is not String. got={} ({})'.format(type(evaled), evaled))
        if evaled.value != 'Hello World!':
            self.fail('String has wrong value. got={}'.format(evaled.value))

    def check_eval(self, input: str) -> object.Object:
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        env = environment.new_environment()
        return evaluator.evals(program, env)


class TestStringConcatenation(unittest.TestCase):
    def test_stringconcate(self):
        input = '''"Hello" + " " + "World!";
                '''
        evaled = self.check_eval(input)
        if not isinstance(evaled, object.String):
            self.fail('object is not String. got={} ({})'.format(type(evaled), evaled))
        if evaled.value != 'Hello World!':
            self.fail('String has wrong value. got={}'.format(evaled.value))

    def check_eval(self, input: str) -> object.Object:
        l = lexer.new(input)
        p = parser.new(l)
        program = p.parse_program()
        env = environment.new_environment()
        return evaluator.evals(program, env)


class TestBuiltinFunctions(unittest.TestCase):
    def test_buildinfunc(self):
        EvalBuildin = namedtuple('EvalBuildin', ['input', 'expected'])
        tests = [
            EvalBuildin('len("")', 0),
            EvalBuildin('len("four")', 4),
            EvalBuildin('len("hello world")', 11),
            EvalBuildin('len(1)', 'argument to `len` not supported, got INTEGER'),
            EvalBuildin('len("one", "two")', 'wrong number of arguments. got=2, want=1'),
        ]
        for tt in tests:
            evaled = self.check_eval(tt.input)
            if isinstance(tt.expected, int):
                self.check_integerobject(evaled, tt.expected)
            elif isinstance(tt.expected, str):
                if not isinstance(evaled, object.Error):
                    self.fail('object is not Error. got={} ({})'.format(type(evaled), evaled))
                if evaled.message != tt.expected:
                    self.fail('wrong error message. expected={}, got={}'.format(tt.expected, evaled.message))

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


class TestArrayLiterals(unittest.TestCase):
    def test_arrayliteral(self):
        input = '[1, 2 * 2, 3 + 3]'
        evaled = self.check_eval(input)
        if not isinstance(evaled, object.Array):
            self.fail('object is not Array. got={} ({})'.format(type(evaled), evaled))
        if len(evaled.elements) !=3:
            self.fail('array has wrong num of elements. got={}'.format(len(evaled.elements)))
        self.check_integerobject(evaled.elements[0], 1)
        self.check_integerobject(evaled.elements[1], 4)
        self.check_integerobject(evaled.elements[2],6)


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


class TestArrayIndexExpressions(unittest.TestCase):
    def test_array_index(self):
        EvalArrayInd = namedtuple('EvalArrayInd', ['input', 'expected'])
        tests = [
            EvalArrayInd('[1, 2, 3][0];', 1),
            EvalArrayInd('[1, 2, 3][1];', 2),
            EvalArrayInd('[1, 2, 3][2];', 3),
            EvalArrayInd('let i = 0; [1][i];', 1),
            EvalArrayInd('[1, 2, 3][1 + 1];', 3),
            EvalArrayInd('let myArray = [1, 2, 3]; myArray[2];', 3),
            EvalArrayInd('let myArray = [1, 2, 3]; myArray[0] + myArray[1] + myArray[2];', 6),
            EvalArrayInd('let myArray = [1, 2, 3]; let i = myArray[0]; myArray[i]', 2),
            EvalArrayInd('[1, 2, 3][3]', None),
            EvalArrayInd('[1, 2, 3][-1]', None),
        ]
        for tt in tests:
            evaled = self.check_eval(tt.input)
            integer = tt.expected
            if isinstance(integer, int):
                self.check_integerobject(evaled, tt.expected)
            else:
                self.check_nullobject(evaled)

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

    def check_nullobject(self, obj: object.Object) -> bool:
        if obj != evaluator.NULL:
            print('object is not NULL. got={} ({})'.format(type(obj), obj))
            return False
        return True


class TestHashLiterals(unittest.TestCase):
    def test_hashliteral(self):
        input = '''
        let two = "two";
            {
                "one": 10 - 9,
                two: 1 + 1,
                "thr" + "ee": 6 / 2,
                4: 4,
                true: 5,
                false: 6
            }
        '''
        evaled = self.check_eval(input)
        if not isinstance(evaled, object.Hash):
            self.fail('Eval didn\'t return Hash. got={} ({})'.format(evaled, evaled))
        expected: Dict[object.Hash, int] = {
            object.String(value='one').hash_key(): 1,
            object.String(value='two').hash_key(): 2,
            object.String(value='three').hash_key(): 3,
            object.Integer(value=4).hash_key(): 4,
            evaluator.TRUE.hash_key(): 5,
            evaluator.FALSE.hash_key(): 6,
        }
        if len(evaled.pairs) != len(expected):
            self.fail('Hash has wrong num of pairs. got={}'.format(len(evaled.pairs)))

        for exp_key, exp_val in expected.items():
            pair = evaled.pairs.get(exp_key, 'error')
            if pair == 'error':
                self.fail('no pair for given key in Pairs')
            self.check_integerobject(pair.value, exp_val)

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


class TestHashIndexExpressions(unittest.TestCase):
    def test_hash_indexexpression(self):
        HashIndexs = namedtuple('HashIndexs', ['input', 'expected'])
        tests = [
            HashIndexs('{"foo": 5}["foo"]', 5),
            HashIndexs('{"foo": 5}["bar"]', None),
            HashIndexs('let key = "foo"; {"foo": 5}[key]', 5),
            HashIndexs('{}["foo"]', None),
            HashIndexs('{5: 5}[5]', 5),
            HashIndexs('{true: 5}[true]', 5),
            HashIndexs('{false: 5}[false]', 5),
        ]
        for tt in tests:
            evaled = self.check_eval(tt.input)
            intger = tt.expected
            if isinstance(intger, int):
                self.check_integerobject(evaled, intger)
            else:
                self.check_nullobject(evaled)

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

    def check_nullobject(self, obj: object.Object) -> bool:
        if obj != evaluator.NULL:
            print('object is not NULL. got={} ({})'.format(type(obj), obj))
            return False
        return True


if __name__ == '__main__':
    unittest.main()