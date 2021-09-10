from lib.token import TokenType
import lib.expressions as Expressions
import lib.statements as Statements
from lib.errors import Error as ParseError

class Parser:

    STATEMENT_BOUNDARY_TOKENS = [
        TokenType.CLASS,
        TokenType.FUN,
        TokenType.VAR,
        TokenType.FOR,
        TokenType.IF,
        TokenType.WHILE,
        TokenType.PRINT,
        TokenType.RETURN
    ]

    def __init__(self, runtime, tokens):
        self.runtime = runtime
        self.tokens  = tokens
        
        self.current = 0

    def parse(self):
        statements = []

        while not self.is_at_end():
            statements.append(self.declaration())

        return statements

    # Grammar rules
    def declaration(self):
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()

            return self.statement()
        except ParseError as _ex:
            self.synchronize()

    def expression(self):
        return self.assignment()

    def statement(self):
        if self.match(TokenType.PRINT):
            return self.print_statement()

        return self.expression_statement()

    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, 'Expected variable name.')

        initializer = None

        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expected ';' after variable definition.")

        return Statements.Var(name, initializer)

    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after value.")

        return Statements.Print(value)

    def expression_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after value.")

        return Statements.Expression(value)

    def comparison(self):
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Expressions.Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Expressions.Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.factor()
            expr = Expressions.Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()

            return Expressions.Unary(operator, right)

        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE):
            return Expressions.Literal(False)
        elif self.match(TokenType.TRUE):
            return Expressions.Literal(True)
        elif self.match(TokenType.NIL):
            return Expressions.Literal(None)
        elif self.match(TokenType.NUMBER, TokenType.STRING):
            return Expressions.Literal(self.previous().literal)
        elif self.match(TokenType.IDENTIFIER):
            return Expressions.Variable(self.previous())
        elif self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")

            return Expressions.Grouping(expr)

        self.error(self.peek(), 'Expected an expression.')

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Expressions.Binary(expr, operator, right)

        return expr

    def assignment(self):
        expr = self.equality()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Expressions.Variable):
                name = expr.name
                
                return Expressions.Assign(name, value)

            self.error(equals, 'Invalid assignment target.')

        return expr

    # Primitive operations for managing stack pointer
    def match(self, *token_types):
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                
                return True
        
        return False

    def check(self, token_type):
        if self.is_at_end():
            return False
        
        return self.peek().type == token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1

        return self.previous()

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()

        self.error(self.peek(), message)

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous() == TokenType.SEMICOLON:
                return

            if self.peek() in self.STATEMENT_BOUNDARY_TOKENS:
                return

            self.advance()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def error(self, token, message):
        raise ParseError(token, message)
