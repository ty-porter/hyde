from lib.expressions import Visitor as ExpressionVisitor
from lib.statements import Visitor as StatementVisitor


class Visitor(ExpressionVisitor, StatementVisitor):
    def visit(self, other):
        visit_fn_name = f'visit_{type(other).__name__.lower()}'
        visit_fn = getattr(self, visit_fn_name)

        return visit_fn(other)