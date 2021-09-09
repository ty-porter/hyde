from lib.interpreter import Interpreter
from lib.parser import Parser
from lib.tokenizer import Tokenizer

import sys


class PyLang:
    def __init__(self):
        self.debug_enabled     = False
        self.had_error         = False
        self.had_runtime_error = False
        self.interpreter       = Interpreter(self)

    def run(self):
        args = self.parse_args()
        
        if len(args) > 2:
            print('Usage: python main.py [script]')
            sys.exit(64)
        elif len(args) == 1:
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

        if self.had_error or self.had_runtime_error:
            self.had_error         = False
            self.had_runtime_error = False
            return

        self.interpreter.interpret(statements)

    def error(self, error):
        self.report(error.token.line, type(error).__name__, error.message)
        self.had_error = True

    def runtime_error(self, error):
        self.report(error.token.line, type(error).__name__, error.message)
        self.had_runtime_error = True

    def report(self, line, error_type, message):
        print(f'[Line {line}] {error_type}: {message}')

    def parse_args(self):
        args = sys.argv[1:]

        return args


lang = PyLang()
lang.run()