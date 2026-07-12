from __future__ import annotations

import js_ast as ast
from lexer import Token, TokenType

OPERATORS = {
    TokenType.PLUS: ast.Operator.PLUS,
    TokenType.DASH: ast.Operator.MINUS,
    TokenType.STAR: ast.Operator.TIMES,
    TokenType.SLASH: ast.Operator.DIVIDE,
    TokenType.EQEQ: ast.Operator.EQEQ,
    TokenType.NEQ: ast.Operator.NEQ,
    TokenType.GT: ast.Operator.GT,
    TokenType.LT: ast.Operator.LT,
    TokenType.GREQ: ast.Operator.GREQ,
    TokenType.LEEQ: ast.Operator.LEEQ,
    TokenType.OR: ast.Operator.OR,
    TokenType.AND: ast.Operator.AND,
    TokenType.NOT: ast.Operator.NOT,
    TokenType.INC: ast.Operator.INC,
    TokenType.DEC: ast.Operator.DEC,
}


class Parser:
    tokens: list[Token]
    cursor: int

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.cursor = 0

    def parse(self) -> ast.Block:
        block = ast.Block([])
        while self.peek().type is not TokenType.EOF:
            stmt = self.next_statement()
            print(f"[parse] got statement {stmt}")
            block.statements.append(stmt)
        return block

    def next_block(self) -> ast.Block:
        self.require(TokenType.LBRACE)

        block = ast.Block([])
        while self.peek().type is not TokenType.RBRACE:
            block.statements.append(self.next_statement())

        self.require(TokenType.RBRACE)
        return block

    def next_statement(self) -> ast.Statement | ast.Expression:
        token = self.peek()

        if token.type is TokenType.VAR:
            return self.next_var_decl()
        elif token.type is TokenType.IF:
            return self.next_if_statement()
        elif token.type is TokenType.WHILE:
            return self.next_while_statement()

        expression = self.next_expression()
        self.require(TokenType.SEMI)
        return expression

    def next_if_statement(self) -> ast.IfStatement:
        self.require(TokenType.IF)
        self.require(TokenType.LPAREN)
        condition = self.next_expression()
        self.require(TokenType.RPAREN)
        block = self.next_block()

        return ast.IfStatement(condition, block)

    def next_while_statement(self) -> ast.WhileStatement:
        self.require(TokenType.WHILE)
        self.require(TokenType.LPAREN)
        condition = self.next_expression()
        self.require(TokenType.RPAREN)
        block = self.next_block()

        return ast.WhileStatement(condition, block)

    def next_var_decl(self) -> ast.VarDeclarationStatement:
        self.require(TokenType.VAR)
        name = self.expect(TokenType.IDENT).content
        self.require(TokenType.ASSIGN)
        value = self.next_expression()
        self.require(TokenType.SEMI)

        return ast.VarDeclarationStatement(name, value)

    def next_expression(self) -> ast.Expression:
        return self.next_assignment()

    def next_assignment(self) -> ast.Expression:
        expression = self.next_equality()

        if self.peek().type == TokenType.ASSIGN:
            if not (
                isinstance(expression, ast.IdentifierExpression)
                or isinstance(expression, ast.MemberExpression)
            ):
                raise SyntaxError(
                    f"can't assign to value of type {expression.__class__}"
                )

            self.require(TokenType.ASSIGN)
            right = self.next_assignment()
            expression = ast.AssignmentExpression(expression, right)

        return expression

    def next_equality(self) -> ast.Expression:
        expression = self.next_addition()

        while self.peek().type in (
            TokenType.EQEQ,
            TokenType.NEQ,
            TokenType.GT,
            TokenType.LT,
            TokenType.GREQ,
            TokenType.LEEQ,
        ):
            operator = self.next_operator()
            right = self.next_addition()
            expression = ast.BinaryExpression(expression, operator, right)

        return expression

    def next_addition(self) -> ast.Expression:
        expression = self.next_multiplication()

        while self.peek().type in (TokenType.PLUS, TokenType.DASH):
            operator = self.next_operator()
            right = self.next_multiplication()
            expression = ast.BinaryExpression(expression, operator, right)

        return expression

    def next_multiplication(self) -> ast.Expression:
        expression = self.next_postfix()

        while self.peek().type in (TokenType.STAR, TokenType.SLASH):
            operator = self.next_operator()
            right = self.next_postfix()
            expression = ast.BinaryExpression(expression, operator, right)

        return expression

    def next_operator(self) -> ast.Operator:
        token = self.advance()
        op = OPERATORS.get(token.type)
        if op is None:
            raise SyntaxError(f"expected operator; got {token}")
        return op

    def next_postfix(self) -> ast.Expression:
        expression = self.next_primary()
        while True:
            next_token = self.peek()
            if next_token.type == TokenType.DOT:
                self.require(TokenType.DOT)
                name = self.expect(TokenType.IDENT).content
                expression = ast.MemberExpression(
                    expression, ast.IdentifierExpression(name)
                )
            elif next_token.type == TokenType.LPAREN:
                self.require(TokenType.LPAREN)
                fn_args: list[ast.Expression] = []

                while self.peek().type != TokenType.RPAREN:
                    fn_args.append(self.next_expression())
                    if self.peek().type != TokenType.COMMA:
                        break
                    self.advance()

                self.require(TokenType.RPAREN)
                expression = ast.FunctionCallExpression(expression, fn_args)
            else:
                break

        return expression

    def next_primary(self) -> ast.Expression:
        token = self.advance()

        if token.type is TokenType.NUMBER:
            return ast.NumberExpression(float(token.content))
        elif token.type == TokenType.STRING:
            return ast.StringExpression(token.content)
        elif token.type == TokenType.LPAREN:
            expression = self.next_expression()
            self.require(TokenType.RPAREN)
            return expression
        elif token.type == TokenType.IDENT:
            return ast.IdentifierExpression(token.content)

        raise SyntaxError(f"unexpected token {token.type}")

    def peek(self):
        if self.cursor >= len(self.tokens):
            return Token(TokenType.EOF, "eof")
        return self.tokens[self.cursor]

    def advance(self):
        token = self.peek()
        self.cursor += 1
        return token

    def expect(self, type: TokenType):
        token = self.advance()
        if token.type != type:
            raise Exception(f"unexpected token {token.type} - expected {type}")
        return token

    def require(self, type: TokenType):
        _ = self.expect(type)


def parse(tokens: list[Token]) -> ast.Block:
    parser = Parser(tokens)
    return parser.parse()
