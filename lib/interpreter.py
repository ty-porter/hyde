from lib.hyde_function import HydeFunction
from lib.globals import Globals
from lib.hyde_callable import HydeCallable
from lib.environment import Environment
from lib.environment import RuntimeError as EnvironmentRuntimeError
from lib.errors import BaseError, Return
from lib.token import TokenType
from lib.visitor import Visitor


class InterpreterError(BaseError):
    pass


class InterpreterRuntimeError(BaseError):
    pass


class Interpreter(Visitor):
    def __init__(self, runtime):
        self.runtime     = runtime
        self.globals     = Environment()
        self.environment = self.globals

        Globals.define(self.globals)

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except InterpreterError as ex:
            self.runtime.error(ex)
        except (InterpreterRuntimeError, EnvironmentRuntimeError) as ex:
            self.runtime.runtime_error(ex)

    def execute(self, stmt):
        return self.visit(stmt)

    def execute_block(self, statements, environment):
        previous = self.environment

        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    # Visit Expressions
    def visit_assign(self, expr):
        value = self.visit(expr.value)
        self.environment.assign(expr.name, value)

        return value

    def visit_binary(self, expr):
        left  = self.visit(expr.left)
        right = self.visit(expr.right)
        operator = expr.operator

        if operator.type == TokenType.GREATER:
            self.check_number_operands(operator, left, right)
            return float(left) > float(right)
        elif operator.type == TokenType.GREATER_EQUAL:
            self.check_number_operands(operator, left, right)
            return float(left) >= float(right)
        elif operator.type == TokenType.LESS:
            self.check_number_operands(operator, left, right)
            return float(left) < float(right)
        elif operator.type == TokenType.LESS_EQUAL:
            self.check_number_operands(operator, left, right)
            return float(left) <= float(right)
        elif operator.type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif operator.type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)
        elif operator.type == TokenType.MINUS:
            self.check_number_operands(operator, left, right)
            return float(left) - float(right)
        elif operator.type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)

            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)

            self.runtime_error(operator, 'Operands must be two numbers or two strings.')
        elif operator.type == TokenType.SLASH:
            self.check_number_operands(operator, left, right)
            return float(left) / float(right)
        elif operator.type == TokenType.STAR:
            self.check_number_operands(operator, left, right)
            return float(left) * float(right)

    def visit_call(self, expr):
        callee = self.visit(expr.callee)

        if not isinstance(callee, HydeCallable):
            self.error(expr.paren, 'Can only call functions and classes.')

        arguments = []

        for argument in expr.arguments:
            arguments.append(self.visit(argument))


        if len(arguments) != callee.arity:
            self.error(expr.paren, f'Expected {callee.arity} arguments but got {len(arguments)}')

        return callee.call(self, arguments)

    def visit_grouping(self, expr):
        return self.visit(expr.expression)

    def visit_literal(self, expr):
        return expr.value
    
    def visit_logical(self, expr):
        left = self.visit(expr.left)

        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left

        return self.visit(expr.right)

    def visit_unary(self, expr):
        right = self.visit(expr.right)

        if expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)
        elif expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return float(right) * -1

    def visit_variable(self, expr):
        return self.environment.get(expr.name)

    # Visit Statements
    def visit_block(self, stmt):
        self.execute_block(stmt.statements, Environment(enclosing = self.environment))

    def visit_expression(self, stmt):
        self.visit(stmt.expression)

    def visit_function(self, stmt):
        fn = HydeFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, fn)

    def visit_ifstmt(self, stmt):
        if self.is_truthy(self.visit(stmt.condition)):
            self.execute(stmt.then_branch)
        else:
            self.execute(stmt.else_branch)

    def visit_print(self, stmt):
        value = self.visit(stmt.expression)
        print(value)

    def visit_returnstmt(self, stmt):
        value = None

        if stmt.value is not None:
            value = self.visit(stmt.value)

        raise Return(value)

    def visit_whilestmt(self, stmt):
        while self.is_truthy(self.visit(stmt.condition)):
            self.execute(stmt.body)

    def visit_var(self, stmt):
        value = None
        
        if stmt.initializer is not None:
            value = self.visit(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)

    # Helpers
    def is_truthy(self, object):
        if object is None:
            return False
        
        if object in [True, False]:
            return object

        return True

    def is_equal(self, left, right):
        return left == right

    def check_number_operand(self, operator, operand):
        if isinstance(operand, float):
            return

        self.runtime_error(operator, 'Operand must be a number.')

    def check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return

        self.runtime_error(operator, 'Operands must be numbers.')

    def error(self, token, message):
        raise InterpreterError(token, message)

    def runtime_error(self, token, message):
        raise InterpreterRuntimeError(token, message)
