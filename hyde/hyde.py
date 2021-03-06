from hyde.interpreter import Interpreter
from hyde.parser import Parser
from hyde.resolver import ResolutionError, Resolver
from hyde.tokenizer import Tokenizer

import os
import sys


class Hyde:
    NATIVE_FUNCTION_FILES = [
        'native/array.hy'
    ]

    def __init__(self):
        self.debug_enabled     = False
        self.had_error         = False
        self.had_runtime_error = False
        self.interpreter       = Interpreter(self)

    def run(self):
        args = self.parse_args()
        
        if len(args) > 2:
            print('Usage: hyde [script]')
            sys.exit(64)
        
        self.load_native_functions()

        if len(args) == 1:
            self.run_file(args[0])
        else:
            self.run_prompt()

    def run_file(self, filepath):
        with open(filepath, 'r') as file:
            code = file.read()

        if self.had_error:
            sys.exit(65)
        elif self.had_runtime_error:
            sys.exit(75)

        self.execute(code)
    
    def run_prompt(self):
        while True:
            try:
                line = input("> ")

                self.execute(line)
            except (EOFError, KeyboardInterrupt):
                print() # print a newline
                sys.exit()

    def execute(self, expr):
        tokenizer  = Tokenizer(self, expr)
        tokens     = tokenizer.scan_tokens()
        parser     = Parser(self, tokens)
        statements = parser.parse()
        
        if self.handle_errors():
            return

        try:
            resolver = Resolver(self.interpreter)
            resolver.resolve(statements)
        except ResolutionError as ex:
            self.error(ex)

        if self.handle_errors():
            return

        self.interpreter.interpret(statements)

        if self.handle_errors():
            return

    def error(self, error):
        self.report(error.token.line, type(error).__name__, error.token.lexeme, error.message)
        self.had_error = True

    def runtime_error(self, error):
        self.report(error.token.line, type(error).__name__, error.token.lexeme, error.message)
        self.had_runtime_error = True

    def report(self, line, error_type, location, message):
        error_description = f'{error_type} at {location}' if location else error_type
        print(f'[Line {line}] {error_description}: {message}')

    def parse_args(self):
        args = sys.argv[1:]

        return args

    def handle_errors(self):
        if self.had_error or self.had_runtime_error:
            self.had_error         = False
            self.had_runtime_error = False

            return True

        return False

    def load_native_functions(self):
        for relpath in self.NATIVE_FUNCTION_FILES:
            self.load_native_function(relpath)

    def load_native_function(self, hyde_relpath):
        file_abs_path = os.path.abspath(os.path.dirname(__file__))
        hyde_path = os.path.join(file_abs_path, hyde_relpath)

        self.run_file(hyde_path)

    