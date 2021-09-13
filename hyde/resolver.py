from enum import Enum, auto, unique
from hyde.errors import BaseError
from hyde.visitor import Visitor


@unique
class FunctionType(Enum):
    NONE     = auto()
    FUNCTION = auto()


class ResolutionError(BaseError):
    pass


class Resolver(Visitor):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes      = [{}]
        self.current_fn  = FunctionType.NONE

    # Visit Expressions
    def visit_assign(self, expr):
        self.resolve_single(expr.value)
        self.resolve_local(expr, expr.name)

    def visit_binary(self, expr):
        self.resolve_single(expr.left)
        self.resolve_single(expr.right)

    def visit_call(self, expr):
        self.resolve_single(expr.callee)

        for argument in expr.arguments:
            self.resolve_single(argument)

    def visit_grouping(self, expr):
        self.resolve_single(expr.expression)

    def visit_literal(self, expr):
        pass

    def visit_logical(self, expr):
        self.resolve_single(expr.left)
        self.resolve_single(expr.right)

    def visit_unary(self, expr):
        self.resolve_single(expr.right)

    def visit_variable(self, expr):
        if len(self.scopes) != 0 and self.scopes[-1].get(expr.name.lexeme) == False:
            raise ResolutionError(expr.name, "Can't read local variable in its own initializer.")
    
        self.resolve_local(expr, expr.name)

    # Visit Statements
    def visit_block(self, stmt):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()

    def visit_expression(self, stmt):
        self.resolve_single(stmt.expression)

    def visit_ifstmt(self, stmt):
        self.resolve_single(stmt.condition)
        self.resolve_single(stmt.then_branch)

        if stmt.else_branch is not None:
            self.resolve_single(stmt.else_branch)

    def visit_function(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt, FunctionType.FUNCTION)

    def visit_print(self, stmt):
        self.resolve_single(stmt.expression)

    def visit_returnstmt(self, stmt):
        if (self.current_fn == FunctionType.NONE):
            raise ResolutionError(stmt.keyword, "Can't return from top-level code.")

        if stmt.value is not None:
            self.resolve_single(stmt.value)

    def visit_var(self, stmt):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve_single(stmt.initializer)

        self.define(stmt.name)

    def visit_whilestmt(self, stmt):
        self.resolve_single(stmt.condition)
        self.resolve_single(stmt.body)

    # Helpers
    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def resolve(self, statements):
        for statement in statements:
            self.resolve_single(statement)

    def resolve_single(self, other):
        self.visit(other)

    def resolve_local(self, expr, name):
        distance = len(self.scopes) - 1
        for i in range(len(self.scopes)):
            if name.lexeme in self.scopes[i]:
                distance = len(self.scopes) - 1 - i
        
        self.interpreter.resolve(expr, distance)

    def resolve_function(self, function, fn_type):
        enclosing_fn    = self.current_fn
        self.current_fn = fn_type

        self.begin_scope()

        for param in function.params:
            self.declare(param)
            self.define(param)

        self.resolve(function.body)

        self.end_scope()

        self.current_fn = enclosing_fn

    def declare(self, name):
        if len(self.scopes) == 0:
            return

        scope = self.scopes[-1]

        if name.lexeme in scope:
            raise ResolutionError(name, 'Already a variable with this name in this scope.')

        scope[name.lexeme] = False

    def define(self, name):
        if len(self.scopes) == 0:
            return

        self.scopes[-1][name.lexeme] = True