class Statement:
    pass


class Block(Statement):
    def __init__(self, statements):
        self.statements = statements


class Expression(Statement):
    def __init__(self, expression):
        self.expression = expression


class Print(Statement):
    def __init__(self, expression):
        self.expression = expression


class Var(Statement):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer


class Visitor:
    # Base methods to be overridden in child classes
    def visit_block(self, block):
        raise NotImplementedError('visit_block')

    def visit_expression(self, expression):
        raise NotImplementedError('visit_expression')

    def visit_print(self, print):
        raise NotImplementedError('visit_print')

    def visit_var(self, var):
        raise NotImplementedError('visit_var')

