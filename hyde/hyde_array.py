from hyde.hyde_callable import HydeCallable
from hyde.hyde_instance import HydeInstance, HydeInstanceError


class HydeArray(HydeInstance):
    name = "Array"

    class ArrayFunction(HydeCallable):
        def __init__(self, array, token):
            self.array = array
            self.token = token


    class ArrayGet(ArrayFunction):
        arity = 1

        def call(self, _interpreter, arguments):
            try:
                index = int(arguments[0])

                return self.array.elements[index]
            except IndexError:
                raise HydeInstanceError(self.token, 'Array index out of range.')

        
    class ArraySet(ArrayFunction):
        arity = 2

        def call(self, _interpreter, arguments):
            try:
                index = int(arguments[0])
                value = arguments[1]
                self.array.elements[index] = value

                return value
            except IndexError:
                raise HydeInstanceError(self.token, 'Array assignment index out of range.')

        
    class ArrayLength(ArrayFunction):
        arity = 0
        
        def call(self, _interpreter, _arguments):
            return float(len(self.array.elements))


    def __init__(self, size):
        self.elements = [None] * size

    def get(self, name):
        if name.lexeme == 'get':
            return HydeArray.ArrayGet(self, name)
        elif name.lexeme == 'set':
            return HydeArray.ArraySet(self, name)
        elif name.lexeme == 'length':
            return HydeArray.ArrayLength(self, name)

        raise HydeInstanceError(name, f'Undefined property {name.lexeme} for {self.klass} instance.')

    def set(self, name, _value):
        raise HydeInstanceError(name, "Can't add properties to arrays.")

    def __str__(self):
        elements = ', '.join(str(element) for element in self.elements)

        return f'[{elements}]'
