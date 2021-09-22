class ASTGenerator:

    EXPRESSIONS_PATH = 'hyde/expressions.py'
    STATEMENTS_PATH = 'hyde/statements.py'

    EXPRESSIONS = {
        'Expression': None,
        'Assign': ['name', 'value'],
        'Binary': ['left', 'operator', 'right'],
        'Call': ['callee', 'paren', 'arguments'],
        'Get': ['object', 'name'],
        'Grouping': ['expression'],
        'Literal': ['value'],
        'Logical': ['left', 'operator', 'right'],
        'Set': ['object', 'name', 'value'],
        'Super': ['keyword', 'method'],
        'This': ['keyword'],
        'Unary': ['operator', 'right'],
        'Variable': ['name']
    }

    STATEMENTS = {
        # class, if, return, and while are reserved words in Python
        'Statement': None,
        'Block': ['statements'],
        'ClassDef': ['name', 'superclass', 'methods'],
        'Expression': ['expression'],
        'Function': ['name', 'params', 'body'],
        'IfStmt': ['condition', 'then_branch', 'else_branch'],
        'Print': ['expression'],
        'ReturnStmt': ['keyword', 'value'],
        'Var': ['name', 'initializer'],
        'WhileStmt': ['condition', 'body']
    }

    @classmethod
    def define_expressions(cls):
        ASTGenerator.define_ast(cls.EXPRESSIONS, cls.EXPRESSIONS_PATH)

    @classmethod
    def define_statements(cls):
        ASTGenerator.define_ast(cls.STATEMENTS, cls.STATEMENTS_PATH)

    @classmethod
    def define_ast(cls, data, output_path):
        lines = []
        parent_class = list(data.keys())[0]

        for class_name in data:
            attributes = data[class_name]
            initializer = ASTGenerator.generate_initializer(attributes)

            class_definition = f'{class_name}({parent_class})' if class_name != parent_class else class_name
            klass = f'''\
class {class_definition}:
    {initializer}
'''
            
            lines.append(klass)

        visitor_class = ASTGenerator.generate_visitor_class(data, without = [parent_class])
        lines.append(visitor_class)

        code = '\n'.join(lines)

        ASTGenerator.write(output_path, code)

    @classmethod
    def generate_initializer(cls, attributes):
        if attributes is None:
            return f'''\
pass
'''

        param_list = ', '.join(attributes)
        initializer_attributes = ''

        for attribute in attributes:
            initializer_attributes += f'''\
        self.{attribute} = {attribute}
'''

        initializer = f'''\
def __init__(self, {param_list}):
{initializer_attributes}'''

        return initializer

    @classmethod
    def generate_visitor_class(cls, other_classes, without = []):
        base = '''\
class Visitor:
    # Base methods to be overridden in child classes
'''

        method_count = 0
        for klass in other_classes:
            if klass in without:
                continue

            method = f'''\
    def visit_{klass.lower()}(self, {klass.lower()}):
        raise NotImplementedError('visit_{klass.lower()}')

'''

            base += method
            method_count += 1

        if method_count == 0:
            base += '''\
    pass
'''

        return base

    @classmethod
    def write(cls, path, code):
        with open(path, 'w') as file:
            file.write(code)


ASTGenerator.define_expressions()
ASTGenerator.define_statements()