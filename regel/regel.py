import re
import sys
from functools import reduce
from . import parser

_MODULE = "module"


def regel(typename, pattern):
    def _init(self, text):
        match = self._regex.match(text)
        if not match:
            raise ValueError(
                f"Text '{text}' does not match pattern '{self._pattern}'")
        strings = match.groups()
        values = [
            self._apply_many(funcs, string)
            for funcs, string
            in zip(self._funcLists, strings)
        ]
        for field, value in zip(self._fields, values):
            setattr(self, field, value)

    def _apply_many(self, funcs, string):
        return reduce(self._apply, funcs, string)

    def _apply(self, value, applFunc):
        application, func = applFunc
        return func(value) if application == ':' else [func(elem) for elem in value]

    try:
        caller = sys._getframe(1)
        globals = dict(caller.f_globals)
        locals = dict(caller.f_locals)
        module = globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        globals = {}
        locals = {}
        module = __name__

    regex, fields, funcLists = parser.parse(pattern, globals, locals)

    namespace = {
        "__module__": module,
        "__init__": _init,
        "_apply_many": _apply_many,
        "_apply": _apply,
        "_regex": re.compile(regex),
        "_fields": fields,
        "_funcLists": funcLists,
        "_parse": _parse,
        "_pattern": pattern,
    }

    return type(typename, (), namespace)


@classmethod
def _parse(cls, text):
    return cls(text)
