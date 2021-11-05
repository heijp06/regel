import re
import sys
from . import parser

_MODULE = "module"


def regel(typename, pattern):
    def _init(self, text=None):
        if text:
            self._rule.apply(lambda: self, text)
    
    def _iter(self):
        return self._items

    try:
        caller = sys._getframe(1)
        globals = dict(caller.f_globals)
        locals = dict(caller.f_locals)
        module = globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        globals = {}
        locals = {}
        module = __name__

    rule = parser.parse(pattern, globals, locals)

    namespace = {
        "__module__": module,
        "__init__": _init,
        "__iter__": _iter,
        "_rule": rule,
        "_parse": _parse,
        "_parse_many": _parse_many,
    }

    return type(typename, (), namespace)


@classmethod
def _parse(cls, text):
    return cls._rule.apply(cls, text)


@classmethod
def _parse_many(cls, text):
    return cls._rule.apply_many(cls, text)