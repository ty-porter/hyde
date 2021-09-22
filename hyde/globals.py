from hyde.hyde_array import HydeArray
from hyde.hyde_callable import HydeCallable


class Globals:
    class GlobalHydeCallable(HydeCallable):
        capitalized = False

        def __str__(self):
            return f'<fn {self.__name__}>'


    class Array(GlobalHydeCallable):
        arity = 1
        capitalized = True

        def call(self, _interpreter, arguments):
            size = int(arguments[0])

            return HydeArray(size)


    class Clock(GlobalHydeCallable):
        from time import time

        arity = 0

        def call(self, _interpreter, _arguments):
            return round(self.time() * 1000)


    GLOBAL_FUNCTIONS = [
        Array,
        Clock
    ]

    @classmethod
    def define(cls, environment):
        for fn in cls.GLOBAL_FUNCTIONS:
            name = fn.__name__.lower() if not fn.capitalized else fn.__name__
            environment.define(name, fn())