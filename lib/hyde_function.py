from lib.environment import Environment
from lib.errors import Return
from lib.hyde_callable import HydeCallable

class HydeFunction(HydeCallable):
    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure     = closure

        # Override from base HydeCallable
        self.arity = len(declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)

        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme,
                               arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            return return_value.value

    def __str__(self):
        return f'<fn {self.declaration.name.lexeme}>'