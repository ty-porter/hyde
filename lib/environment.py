from lib.errors import RuntimeError

class Environment:
    def __init__(self):
        self.values = {}

    def assign(self, name, value):
        if name.lexeme not in self.values:
            raise RuntimeError(f'Undefined variable {name.lexeme}')

        self.values[name.lexeme] = value

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name.lexeme not in self.values:
            raise RuntimeError(f'Undefined variable {name.lexeme}')

        return self.values[name.lexeme]