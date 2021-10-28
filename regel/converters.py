import operator
from functools import partial


def eq(value):
    return partial(operator.eq, value)


def ne(value):
    return partial(operator.ne, value)


def split(*args):
    delimiters = args or [' ']

    def _split(value):
        result = [value]
        for delimiter in delimiters:
            result = [
                string
                for fragment in result
                for string in fragment.split(delimiter)
            ]
        return result

    return _split


def const(value):
    return lambda _: value
