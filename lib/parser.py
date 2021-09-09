from lib.token import TokenType
import lib.expressions as Expressions
import lib.statements as Statements
from lib.errors import Error as ParserError

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
        try:
            statements = []

            while not self.is_at_end():
                statements.append(self.statement())

            return statements
        except ParserError as ex:
            self.runtime.error(ex)

    # Grammar rules
    def expression(self):
        return self.equality()

    def statement(self):
        if self.match(TokenType.PRINT):
            return self.print_statement()

        return self.expression_statement()

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
        elif self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")

            return Expressions.Grouping(expr)

        self.error('Expected an expression.')

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Expressions.Binary(expr, operator, right)

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

        self.error(message)

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

    def error(self, message):
        raise ParserError(self.peek(), message)
