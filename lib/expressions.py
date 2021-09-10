class Expression:
    pass


class Binary(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Grouping(Expression):
    def __init__(self, expression):
        self.expression = expression


class Literal(Expression):
    def __init__(self, value):
        self.value = value


class Unary(Expression):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right


class Visitor:
    # Base methods to be overridden in child classes
    def visit_binary(self, binary):
        raise NotImplementedError('visit_binary')

    def visit_grouping(self, grouping):
        raise NotImplementedError('visit_grouping')

    def visit_literal(self, literal):
        raise NotImplementedError('visit_literal')

    def visit_unary(self, unary):
        raise NotImplementedError('visit_unary')

