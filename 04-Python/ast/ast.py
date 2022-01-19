from abc import ABCMeta, abstractmethod
from typing import List, Dict
from tokens import *


class Node:
    __meta_class__ = ABCMeta

    @abstractmethod
    def token_literal(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def string(self) -> str:
        raise NotImplementedError


class Statement(Node):
    @abstractmethod
    def statement_node(self):
        raise NotImplementedError


class Expression(Node):
    @abstractmethod
    def expression_node(self):
        raise NotImplementedError


class Programs(Node):
    def __init__(self) -> None:
        self.statements: List[Statement] = []

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ""

    def string(self) -> str:
        out = ''
        for s in self.statements:
            out += s.string()
        return out


class Identifier(Expression):
    def __init__(self, token: Token, value: str) -> None:
        super(Identifier, self).__init__()
        self.token = token
        self.value = value

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return self.value


class IntegerLiteral(Expression):
    def __init__(self, token: Token, value: int) -> None:
        super(IntegerLiteral, self).__init__()
        self.token = token
        self.value = value

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return self.token.literal


class StringLiteral(Expression):
    def __init__(self, token: Token, value: str) -> None:
        self.token = token
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return self.token.literal


class ArrayLiteral(Expression):
    def __init__(self, token: Token, elements: List[Expression]) -> None:
        super(ArrayLiteral, self).__init__()
        self.token = token
        self. elements = elements

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        out = ''
        elements = []
        for el in self.elements:
            elements.append(el.string())
        out = out + '[' + ', '.join(elements) + ']'
        return out


class IndexExpression(Expression):
    def __init__(self, token: Token, left: Expression, index: Expression) -> None:
        super(IndexExpression, self).__init__()
        self.token = token
        self.left = left
        self.index = index

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        out = '(' + self.left.string() + '[' + self.index.string() + '])'
        return out


class HashLiteral(Expression):
    def __init__(self, token: Token):
        super(HashLiteral, self).__init__()
        self.token = token
        self.pairs: Dict[Expression, Expression] = {}

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def  string(self) -> str:
        out = ''
        pairs = []
        for k,v in self.pairs.items():
            pairs.append(k.string() + ':' + v.string())
        out = '{' + ', '.join(pairs) + '}'
        return out


class Boolean(Expression):
    def __init__(self, token: Token, value: bool):
        super(Boolean, self).__init__()
        self.token = token
        self.value = value

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return self.token.literal


class BlockStatement(Statement):
    def __init__(self, token: Token):
        self.token = token
        self.statements: List[Statement] = []

    def statement_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return ''.join([s.string() for s in self.statements])


class IfExpression(Expression):
    def __init__(self, token: Token, condition: Expression, consequence: BlockStatement,
                 alternative: BlockStatement) -> None:
        super(IfExpression, self).__init__()
        self.token = token
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        ret_str = 'if' + self.condition.string() + ' ' + self.consequence.string()
        return ret_str + 'else ' + self.alternative.string() if self.alternative else ret_str


class FunctionLiteral(Expression):
    def __init__(self, token: Token, parameters: List[Identifier],
                 body: BlockStatement):
        super(FunctionLiteral, self).__init__()
        self.token = token
        self.parameters = parameters
        self.body = body

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        params = ', '.join([p.string() for p in self.parameters])

        return '(' + params + ') ' + self.body.string()


class CallExpression(Expression):
    def __init__(self, token: Token, function: Expression,
                 arguments: List[Expression]):
        super(CallExpression, self).__init__()
        self.token = token
        self.function = function
        self.arguments = arguments

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        args = []
        for a in self.arguments:
            args.append(a.string())
        return self.function.string() + '(' + ', '.join(args) + ')'


class PrefixExpression(Expression):
    def __init__(self, token: Token, operator: str, right: Expression) -> None:
        super(PrefixExpression, self).__init__()
        self.token = token
        self.operator = operator
        self.right = right

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return '(' + self.operator + self.right.string() + ')'


class InfixExpression(Expression):
    def __init__(self, token: Token, left: Expression, operator: str, right: Expression) -> None:
        super(InfixExpression, self).__init__()
        self.token = token
        self.left = left
        self.right = right
        self.operator = operator

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return '(' + self.left.string() + ' ' + self.operator + ' ' + self.right.string() + ')'


class LetStatement(Statement):
    def __init__(self, token: Token, name: Identifier, value: Expression) -> None:
        super(LetStatement, self).__init__()
        self.token = token
        self.name = name
        self.value = value

    def statement_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return '{token_literal} {name} = {value};'.format(token_literal=self.token.literal,
                                                          name=self.name.string(),
                                                          value=self.value.string())


class ReturnStatement(Statement):
    def __init__(self, token: Token, return_value: Expression) -> None:
        super(ReturnStatement, self).__init__()
        self.token = token
        self.return_value = return_value

    def statement_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return '{token_literal} {value};'.format(token_literal=self.token.literal,
                                                 value=self.return_value.string())


class ExpressionStatement(Statement):
    def __init__(self, token: Token, expression: Expression):
        self.token = token
        self.expression = expression

    def statement_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        if self.expression:
            return '{expression}'.format(expression=self.expression.string())
        return ''
