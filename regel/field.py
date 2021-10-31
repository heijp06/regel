from functools import reduce


class Field:
    def __init__(self, name, converters, regex):
        self.name = name
        self.converters = converters
        self.regex = regex

    def __repr__(self):
        return self.name + "".join(repr(converter) for converter in self.converters)

    def convert(self, text):
        return reduce(
            lambda value, converter: converter.convert(value),
            self.converters,
            text)

    def compile(self, globals, locals):
        for converter in self.converters:
            converter.compile(globals, locals)

    def set_value(self, instance, text):
        value = self.convert(text)
        setattr(instance, self.name, value)
