import ast
import object
import environment
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

    # expressions
    elif isinstance(node, ast.IntegerLiteral):
        return object.Integer(value=node.value)
    elif isinstance(node, ast.Boolean):
        return native_bool_2_boolean_object(node.value)
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
    if not isinstance(fn, object.Function):
        return new_error('not a function: {}'.format(fn.type()))
    extended_env = extend_function_env(fn, args)
    evaluated = evals(fn.body, extended_env)
    return unwrap_return_value(evaluated)


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
    if not ok:
        return new_error('identifier not found: ' + node.value)
    return val


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
