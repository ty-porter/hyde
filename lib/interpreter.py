from lib.environment import Environment
from lib.errors import Error as InterpreterError
from lib.errors import RuntimeError as InterpreterRuntimeError
from lib.token import TokenType
from lib.visitor import Visitor


class Interpreter(Visitor):
    def __init__(self, runtime):
        self.runtime     = runtime
        self.environment = Environment()

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except InterpreterError as ex:
            self.runtime.error(ex)
        except InterpreterRuntimeError as ex:
            self.runtime.runtime_error(ex)

    def execute(self, stmt):
        self.visit(stmt)

    # Visit Expressions
    def visit_assign(self, assign):
        value = self.visit(assign.value)
        self.environment.assign(assign.name, value)

        return value

    def visit_binary(self, binary):
        left  = self.visit(binary.left)
        right = self.visit(binary.right)
        operator = binary.operator

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

    def visit_grouping(self, grouping):
        return self.visit(grouping.expression)

    def visit_literal(self, literal):
        return literal.value

    def visit_unary(self, unary):
        right = self.visit(unary.right)

        if unary.operator.type == TokenType.BANG:
            return not self.is_truthy(right)
        elif unary.operator.type == TokenType.MINUS:
            self.check_number_operand(unary.operator, right)
            return float(right) * -1

        return None

    def visit_variable(self, variable):
        return self.environment.get(variable.name)

    # Visit Statements
    def visit_expression(self, stmt):
        self.visit(stmt.expression)

        return None

    def visit_print(self, stmt):
        value = self.visit(stmt.expression)
        print(value)

        return None

    def visit_var(self, stmt):
        value = None
        
        if stmt.initializer is not None:
            value = self.visit(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)

        return None

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
