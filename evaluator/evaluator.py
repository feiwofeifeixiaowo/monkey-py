from ast import ast
from object import object
from evaluator import builtin_function
from object import environment
from typing import List

TRUE = object.Boolean(value=True)
FALSE = object.Boolean(value=False)
NULL = object.Null()


def evals(node: ast.Node, env: environment.Environment) -> object.Object:
    if isinstance(node, ast.Programs):
        return eval_program(node, env)
    elif isinstance(node, ast.BlockStatement):
        return eval_block_statement(node, env)
    elif isinstance(node, ast.ExpressionStatement):
        return evals(node.expression, env)
    elif isinstance(node, ast.ReturnStatement):
        val = evals(node.return_value, env)
        if is_error(val):
            return val
        return object.ReturnValue(value=val)
    elif isinstance(node, ast.LetStatement):
        val = evals(node.value, env)
        if is_error(val):
            return val
        env.set(node.name.value, val)
    elif isinstance(node, ast.ArrayLiteral):
        elements = eval_expression(node.elements, env)
        if len(elements) == 1 and is_error(elements[0]):
            return elements[0]
        arr = object.Array()
        arr.elements = elements
        return arr
    elif isinstance(node, ast.IndexExpression):
        left = evals(node.left, env)
        if is_error(left):
            return left
        index = evals(node.index, env)
        if is_error(index):
            return index
        return eval_indexexpression(left, index)
    elif isinstance(node, ast.HashLiteral):
        return eval_hashliteral(node, env)

    # expressions
    elif isinstance(node, ast.IntegerLiteral):
        return object.Integer(value=node.value)
    elif isinstance(node, ast.Boolean):
        return native_bool_2_boolean_object(node.value)
    elif isinstance(node, ast.StringLiteral):
        return object.String(value=node.value)
    elif isinstance(node, ast.PrefixExpression):
        right = evals(node.right, env)
        if is_error(right):
            return right
        return eval_prefix_expression(node.operator, right)
    elif isinstance(node, ast.InfixExpression):
        left = evals(node.left, env)
        if is_error(left):
            return left
        right = evals(node.right, env)
        if is_error(right):
            return right
        return eval_infix_expression(node.operator, left, right)
    elif isinstance(node, ast.IfExpression):
        return eval_ifexpression(node, env)
    elif isinstance(node, ast.Identifier):
        return eval_identifier(node, env)
    elif isinstance(node, ast.FunctionLiteral):
        params = node.parameters
        body = node.body
        return object.Function(params=params,
                               env=env,
                               body=body)
    elif isinstance(node, ast.CallExpression):
        function = evals(node.function, env)
        if is_error(function):
            return function
        args = eval_expression(node.arguments, env)
        if len(args) == 1 and is_error(args[0]):
            return args[0]
        return apply_function(function, args)
    else:
        return None


def apply_function(fn: object.Object, args: List[object.Object]) -> object.Object:
    if isinstance(fn, object.Function):
        extend_env = extend_function_env(fn, args)
        evaluated = evals(fn.body, extend_env)
        return unwrap_return_value(evaluated)
    elif isinstance(fn, object.Builtin):
        return fn.fn(args)
    else:
        return new_error('not a function: {}'.format(fn.type()))


def extend_function_env(fn: object.Function,
                        args: List[object.Object]) -> environment.Environment:
    en_env = environment.EnvironmentEnclosed()
    en_env.store = fn.env.store
    env = environment.new_enclosed_environment(en_env)
    for ind, param in enumerate(fn.parameters):
        env.set(param.value, args[ind])
    return env


def unwrap_return_value(obj: object.Object) -> object.Object:
    if isinstance(obj, object.ReturnValue):
        return obj.value
    return obj


def eval_expression(exps: List[ast.Expression],
                    env: environment.Environment) -> List[object.Object]:
    result = []
    for e in exps:
        evaluated = evals(e, env)
        if is_error(evaluated):
            return [evaluated]
        result.append(evaluated)
    return result


def eval_identifier(node: ast.Identifier, env: environment.Environment) -> object.Object:
    val, ok = env.get(node.value)
    if ok:
        return val
    built_in = builtin_function.builtin_func.get(node.value, 'error')
    if built_in != 'error':
        return built_in
    return new_error('identifier not found: ' + node.value)


def eval_block_statement(block: ast.BlockStatement, env: environment.Environment) -> object.Object:
    result = object.Object()
    for stmt in block.statements:
        result = evals(stmt, env)
        if result is not None:
            rt = result.type()
            if rt == object.ObjectType.RETURN_VALUE_OBJ or rt == object.ObjectType.ERROR_OBJ:
                return result
    return result


def eval_program(program: ast.Programs, env: environment.Environment) -> object.Object:
    result = object.Object()
    for stmt in program.statements:
        result = evals(stmt, env)
        if isinstance(result, object.ReturnValue):
            return result.value
        elif isinstance(result, object.Error):
            return result
    return result


def eval_ifexpression(ie: ast.IfExpression, env: environment.Environment) -> object.Object:
    condition = evals(ie.condition, env)
    if is_error(condition):
        return condition
    if is_truthy(condition):
        return evals(ie.consequence, env)
    elif ie.alternative is not None:
        return evals(ie.alternative, env)
    else:
        return NULL


def is_truthy(obj: object.Object) -> bool:
    if obj == NULL:
        return False
    elif obj == TRUE:
        return True
    elif obj == FALSE:
        return False
    else:
        return True


def eval_infix_expression(operator: str, left: object.Object, right: object.Object) -> object.Object:
    if left.type() == object.ObjectType.INTEGER_OBJ and right.type() == object.ObjectType.INTEGER_OBJ:
        return eval_integer_infixexpression(operator, left, right)
    elif left.type() == object.ObjectType.STRING_OBJ and right.type() == object.ObjectType.STRING_OBJ:
        return eval_string_infixexpression(operator, left, right)
    elif operator == '==':
        return native_bool_2_boolean_object(left == right)
    elif operator == '!=':
        return native_bool_2_boolean_object(left != right)
    elif left.type() != right.type():
        return new_error('type mismatch: {} {} {}'.format(left.type().value,
                                                          operator,
                                                          right.type().value))
    else:
        return new_error('unknown operator: {} {} {}'.format(left.type().value,
                                                             operator,
                                                             right.type().value))


def eval_indexexpression(left:object.Object, index: object.Object) -> object.Object:
    if left.type() == object.ObjectType.ARRAY_OBJ and index.type() == object.ObjectType.INTEGER_OBJ:
        return eval_arrayindexexpression(left, index)
    elif left.type() == object.ObjectType.HASH_OBJ:
        return eval_hashindexexpression(left, index)
    else:
        return new_error('index operator not supported: {}'.format(left.type().value))


def eval_hashindexexpression(hash: object.Object, index: object.Object) -> object.Object:
    if not isinstance(index, object.Hashable):
        return new_error('unusable as hash key: {}'.format(index.type()))
    pair = hash.pairs.get(index.hash_key(), 'error')
    if pair == 'error':
        return NULL
    return pair.value


def eval_arrayindexexpression(array: object.Object, index: object.Object) -> object.Object:
    ind = index.value
    max = len(array.elements) -1
    if ind <0 or ind > max:
        return NULL
    return array.elements[ind]


def eval_string_infixexpression(operator: str, left: object.Object, right: object.Object) -> object.Object:
    if operator != '+':
        return new_error('unknown operator: {} {} {}'.format(left.type().value, operator, right.type().value))
    left_val = left.value
    right_val = right.value
    return object.String(value=left_val+right_val)


def eval_integer_infixexpression(operator: str, left: object.Object, right: object.Object) -> object.Object:
    left_val = left.value
    right_val = right.value
    if operator == '+':
        return object.Integer(value=left_val + right_val)
    elif operator == '-':
        return object.Integer(value=left_val - right_val)
    elif operator == '*':
        return object.Integer(value=left_val * right_val)
    elif operator == '/':
        return object.Integer(value=left_val / right_val)
    elif operator == '<':
        return native_bool_2_boolean_object(left_val < right_val)
    elif operator == '>':
        return native_bool_2_boolean_object(left_val > right_val)
    elif operator == '==':
        return native_bool_2_boolean_object(left_val == right_val)
    elif operator == '!=':
        return native_bool_2_boolean_object(left_val != right_val)
    else:
        return new_error('unknown operator: {} {} {}'.format(left.type().value,
                                                             operator,
                                                             right.type().value))


def eval_prefix_expression(operator: str, right: object.Object) -> object.Object:
    if operator == '!':
        return eval_bang_operator_expression(right)
    elif operator == '-':
        return eval_minus_prefixoperator_expression(right)
    else:
        return new_error('unknown operator: {}{}'.format(operator, right.type().value))


def eval_bang_operator_expression(right: object.Object) -> object.Object:
    if right == TRUE:
        return FALSE
    elif right == FALSE:
        return TRUE
    elif right == NULL:
        return TRUE
    else:
        return FALSE


def eval_minus_prefixoperator_expression(right: object.Object) -> object.Object:
    if right.type() != object.ObjectType.INTEGER_OBJ:
        return new_error('unknown operator: -{}'.format(right.type().value))
    value = right.value
    return object.Integer(value=-value)


def native_bool_2_boolean_object(input: bool) -> object.Boolean:
    if input:
        return TRUE
    else:
        return FALSE


def eval_statements(stmts: List[ast.Statement], env: environment.Environment) -> object.Object:
    result = object.Object()
    for statement in stmts:
        result = evals(statement, env)

        if isinstance(result, object.ReturnValue):
            return result.value
    return result


def new_error(err_msg: str) -> object.Error:
    return object.Error(msg=err_msg)


def is_error(obj: object.Object) -> bool:
    if obj is not None:
        return obj.type() == object.ObjectType.ERROR_OBJ
    return False


def eval_hashliteral(node: ast.HashLiteral, env: environment.Environment) -> object.Object:
    pairs = {}
    for k, v in node.pairs.items():
        key = evals(k, env)
        if is_error(key):
            return key
        if not isinstance(key, object.Hashable):
            return new_error('unusable as hash key: {}'.format(key.type()))

        value = evals(v, env)
        if is_error(value):
            return value
        hashed = key.hash_key()
        pairs[hashed] = object.HashPair(key=key, value=value)
    return object.Hash(pairs=pairs)

