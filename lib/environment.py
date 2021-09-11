from lib.errors import BaseError


class RuntimeError(BaseError):
    pass


class Environment:
    def __init__(self, enclosing = None):
        self.values    = {}
        self.enclosing = enclosing

    def assign(self, name, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing is not None:
            return self.enclosing.assign(name, value)

        raise RuntimeError(name, f'Undefined variable {name.lexeme}.')

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise RuntimeError(name, f'Undefined variable {name.lexeme}.')
        