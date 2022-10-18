from enum import IntEnum
from typing import Dict

from ast import ast
from ast.ast import *
from lexer.lexer import *


class PrecedencesEnum(IntEnum):
    LOWEST = 1
    EQUALS = 2  # // ==
    LESSGREATER = 3  # // > or <
    SUM = 4  # // +
    PRODUCT = 5  # // *
    PREFIX = 6  # // -X or !X
    CALL = 7  # // myFunction(X)
    INDEX = 8 # arrar[index]


precedences: dict = {TokenType.EQ: PrecedencesEnum.EQUALS,
                     TokenType.NOT_EQ: PrecedencesEnum.EQUALS,
                     TokenType.LT: PrecedencesEnum.LESSGREATER,
                     TokenType.GT: PrecedencesEnum.LESSGREATER,
                     TokenType.PLUS: PrecedencesEnum.SUM,
                     TokenType.MINUS: PrecedencesEnum.SUM,
                     TokenType.SLASH: PrecedencesEnum.PRODUCT,
                     TokenType.ASTERISK: PrecedencesEnum.PRODUCT,
                     TokenType.LPAREN: PrecedencesEnum.CALL,
                     TokenType.LBRACKET: PrecedencesEnum.INDEX
                     }


def prefix_parsefn() -> Expression:
    pass


def infix_parsefn(exp: Expression) -> Expression:
    pass


class Parser:
    def __init__(self,
                 lexer: Lexer,
                 cur_token: Token = Token(TokenType.EOF, ""),
                 peek_token: Token = Token(TokenType.EOF, "")) -> None:
        self.lexer = lexer
        self.cur_token = cur_token
        self.peek_token = peek_token
        self.errs = []
        self.prefix_parsefns: Dict[TokenType, prefix_parsefn] = {}
        self.infix_parsefns: Dict[TokenType, infix_parsefn] = {}

    def next_token(self) -> None:
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self) -> Programs:
        program = Programs()
        while not self.cur_tokenis(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt is not None:
                program.statements.append(stmt)
            self.next_token()
        return program

    def parse_statement(self) -> Statement:
        if self.cur_token.token_type == TokenType.LET:
            return self.parse_letstatement()
        elif self.cur_token.token_type == TokenType.RETURN:
            return self.parse_returnstatement()
        else:
            return self.parse_expressionstatement()

    def parse_letstatement(self) -> LetStatement:
        stmt = LetStatement(token=self.cur_token, name=None, value=None)
        if not self.expect_peek(TokenType.IDENT):
            return None
        stmt.name = Identifier(token=self.cur_token, value=self.cur_token.literal)
        if not self.expect_peek(TokenType.ASSIGN):
            return None
        self.next_token()
        stmt.value = self.parse_expression(PrecedencesEnum.LOWEST)
        if self.peek_tokenis(TokenType.SEMICOLON):
            self.next_token()
        return stmt

    def parse_returnstatement(self) -> ReturnStatement:
        stmt = ReturnStatement(token=self.cur_token, return_value=None)
        self.next_token()
        stmt.return_value = self.parse_expression(PrecedencesEnum.LOWEST)
        if self.peek_tokenis(TokenType.SEMICOLON):
            self.next_token()
        return stmt

    def cur_tokenis(self, t: TokenType) -> bool:
        return self.cur_token.token_type == t

    def peek_tokenis(self, t: TokenType) -> bool:
        return self.peek_token.token_type == t

    def expect_peek(self, t: TokenType) -> bool:
        if self.peek_tokenis(t):
            self.next_token()
            return True
        else:
            self.peek_error(t)
            return False

    def errors(self) -> List[str]:
        return self.errs

    def peek_error(self, t: TokenType) -> None:
        msg = '"expected next token to be {}, got {} instead'.format(t, self.peek_token.token_type)
        self.errs.append(msg)

    def register_prefix(self, token_type: TokenType, fn: prefix_parsefn):
        self.prefix_parsefns[token_type] = fn

    def register_infix(self, token_type: TokenType, fn: infix_parsefn):
        self.infix_parsefns[token_type] = fn

    def parse_expressionstatement(self) -> ExpressionStatement:
        stmt = ExpressionStatement(self.cur_token, None)
        stmt.expression = self.parse_expression(PrecedencesEnum.LOWEST)
        if self.peek_tokenis(TokenType.SEMICOLON):
            self.next_token()
        return stmt

    def no_prefix_parsefnerror(self, t: TokenType):
        msg = 'no prefix parse function for {} found'.format(t)
        self.errs.append(msg)

    def parse_expression(self, precedence: int) -> Expression:
        prefix = self.prefix_parsefns.get(self.cur_token.token_type, None)
        if not prefix:
            self.no_prefix_parsefnerror(self.cur_token.token_type)
            return None
        left_exp = prefix()
        while (not self.peek_tokenis(TokenType.SEMICOLON)) and (precedence < self.peek_precedence()):
            infix = self.infix_parsefns.get(self.peek_token.token_type, None)
            if not infix:
                return left_exp
            self.next_token()
            left_exp = infix(left_exp)
        return left_exp

    def parse_identifier(self) -> Expression:
        return Identifier(token=self.cur_token, value=self.cur_token.literal)

    def parse_integerliteral(self) -> Expression:
        lit = IntegerLiteral(self.cur_token, None)
        try:
            val = int(self.cur_token.literal)
        except ValueError:
            print('"could not parse {} as integer'.format(self.cur_token.literal))
            return None
        lit.value = val
        return lit

    def parse_prefixexpression(self) -> Expression:
        expression = PrefixExpression(self.cur_token, self.cur_token.literal, None)
        self.next_token()
        expression.right = self.parse_expression(PrecedencesEnum.PREFIX)
        return expression

    def parse_infixexpression(self, left: Expression) -> Expression:
        expression = InfixExpression(token=self.cur_token,
                                     operator=self.cur_token.literal,
                                     left=left,
                                     right=None)
        p = self.cur_precedence()
        self.next_token()
        expression.right = self.parse_expression(p)
        return expression

    def peek_precedence(self) -> int:
        p = precedences.get(self.peek_token.token_type, 'error')
        if p and p != 'error':
            return p
        return PrecedencesEnum.LOWEST

    def cur_precedence(self) -> int:
        p = precedences.get(self.cur_token.token_type, 'error')
        if p and p != 'error':
            return p
        return PrecedencesEnum.LOWEST

    def parse_boolean(self) -> Expression:
        return Boolean(token=self.cur_token, value=self.cur_tokenis(TokenType.TRUE))

    def parse_groupedexpression(self) -> Expression:
        self.next_token()
        exp = self.parse_expression(PrecedencesEnum.LOWEST)
        if not self.expect_peek(TokenType.RPAREN):
            return None
        return exp

    def parse_ifexpression(self) -> Expression:
        exp = IfExpression(token=self.cur_token,
                           condition=None,
                           consequence=None,
                           alternative=None)
        if not self.expect_peek(TokenType.LPAREN):
            return None
        self.next_token()

        exp.condition = self.parse_expression(PrecedencesEnum.LOWEST)
        if not self.expect_peek(TokenType.RPAREN):
            return None
        if not self.expect_peek(TokenType.LBRACE):
            return None
        exp.consequence = self.parse_blockstatement()
        if self.peek_tokenis(TokenType.ELSE):
            self.next_token()
            if not self.expect_peek(TokenType.LBRACE):
                return None
            exp.alternative = self.parse_blockstatement()
        return exp

    def parse_blockstatement(self) -> BlockStatement:
        block = BlockStatement(token=self.cur_token)
        self.next_token()
        while not self.cur_tokenis(TokenType.RBRACE):
            stmt = self.parse_statement()
            if stmt is not None:
                block.statements.append(stmt)
            self.next_token()
        return block

    def parse_functionliteral(self) -> Expression:
        lit = FunctionLiteral(token=self.cur_token,
                              parameters=None,
                              body=None)
        if not self.expect_peek(TokenType.LPAREN):
            return None
        lit.parameters = self.parse_functionparameters()
        if not self.expect_peek(TokenType.LBRACE):
            return None
        lit.body = self.parse_blockstatement()
        return lit

    def parse_functionparameters(self) -> List[Identifier]:
        identifiers: List[Identifier] = []
        if self.peek_tokenis(TokenType.RPAREN):
            self.next_token()
            return identifiers
        self.next_token()
        ident = Identifier(token=self.cur_token, value=self.cur_token.literal)
        identifiers.append(ident)
        while self.peek_tokenis(TokenType.COMMA):
            self.next_token()
            self.next_token()
            ident = Identifier(token=self.cur_token,
                               value=self.cur_token.literal)
            identifiers.append(ident)
        if not self.expect_peek(TokenType.RPAREN):
            return None
        return identifiers

    def parse_callexpression(self, function: Expression) -> Expression:
        exp = CallExpression(token=self.cur_token,
                             function=function,
                             arguments=None)
        # exp.arguments = self.parse_callarguments()
        exp.arguments = self.parse_expression_list(TokenType.RPAREN)
        return exp

    def parse_callarguments(self) -> Expression:
        args: List[Expression] = []
        if self.peek_tokenis(TokenType.RPAREN):
            self.next_token()
            return args
        self.next_token()
        args.append(self.parse_expression(PrecedencesEnum.LOWEST))

        while self.peek_tokenis(TokenType.COMMA):
            self.next_token()
            self.next_token()
            args.append(self.parse_expression(PrecedencesEnum.LOWEST))

        if not self.expect_peek(TokenType.RPAREN):
            return None

        return args

    def parse_stringliteral(self) -> ast.Expression:
        return ast.StringLiteral(token=self.cur_token, value=self.cur_token.literal)

    def parse_arrayliteral(self) -> ast.Expression:
        array = ast.ArrayLiteral(token=self.cur_token, elements=None)
        array.elements = self.parse_expression_list(TokenType.RBRACKET)
        return array

    def parse_expression_list(self, end: TokenType) -> ast.Expression:
        list: List[ast.Expression] = []
        if self.peek_tokenis(end):
            self.next_token()
            return list
        self.next_token()
        list.append(self.parse_expression(PrecedencesEnum.LOWEST))
        while self.peek_tokenis(TokenType.COMMA):
            self.next_token()
            self.next_token()
            list.append(self.parse_expression(PrecedencesEnum.LOWEST))
        if not self.expect_peek(end):
            return None
        return list

    def parse_indexexpression(self, left: ast.Expression) -> ast.Expression:
        exp = ast.IndexExpression(token=self.cur_token, left=left, index=None)
        self.next_token()
        exp.index = self.parse_expression(PrecedencesEnum.LOWEST)
        if not self.expect_peek(TokenType.RBRACKET):
            return None
        return exp

    def parse_hashliteral(self) -> ast.Expression:
        hash = ast.HashLiteral(token=self.cur_token)
        while not self.peek_tokenis(TokenType.RBRACE):
            self.next_token()
            key = self.parse_expression(PrecedencesEnum.LOWEST)
            if not self.expect_peek(TokenType.COLON):
                return None
            self.next_token()
            value = self.parse_expression(PrecedencesEnum.LOWEST)
            hash.pairs[key] = value
            if not self.peek_tokenis(TokenType.RBRACE) and not self.expect_peek(TokenType.COMMA):
                return None
        if not self.expect_peek(TokenType.RBRACE):
            return None

        return hash


def new(lexer: Lexer) -> Parser:
    p = Parser(lexer)
    p.register_prefix(TokenType.IDENT, p.parse_identifier)
    p.register_prefix(TokenType.INT, p.parse_integerliteral)
    p.register_prefix(TokenType.STRING, p.parse_stringliteral)
    p.register_prefix(TokenType.BANG, p.parse_prefixexpression)
    p.register_prefix(TokenType.MINUS, p.parse_prefixexpression)
    p.register_prefix(TokenType.TRUE, p.parse_boolean)
    p.register_prefix(TokenType.FALSE, p.parse_boolean)
    p.register_prefix(TokenType.LPAREN, p.parse_groupedexpression)
    p.register_prefix(TokenType.IF, p.parse_ifexpression)
    p.register_prefix(TokenType.FUNCTION, p.parse_functionliteral)
    p.register_prefix(TokenType.LBRACKET, p.parse_arrayliteral)
    p.register_prefix(TokenType.LBRACE, p.parse_hashliteral)

    p.register_infix(TokenType.PLUS, p.parse_infixexpression)
    p.register_infix(TokenType.MINUS, p.parse_infixexpression)
    p.register_infix(TokenType.SLASH, p.parse_infixexpression)
    p.register_infix(TokenType.ASTERISK, p.parse_infixexpression)
    p.register_infix(TokenType.EQ, p.parse_infixexpression)
    p.register_infix(TokenType.NOT_EQ, p.parse_infixexpression)
    p.register_infix(TokenType.LT, p.parse_infixexpression)
    p.register_infix(TokenType.GT, p.parse_infixexpression)

    p.register_infix(TokenType.LPAREN, p.parse_callexpression)
    p.register_infix(TokenType.LBRACKET, p.parse_indexexpression)
    # Read two tokens, so curToken and peekToken are both set
    p.next_token()
    p.next_token()
    return p
