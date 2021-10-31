import re
import sys
from . import parser

_MODULE = "module"


def regel(typename, pattern):
    def _init(self, text=None):
        if text:
            self._setattrs(self, self._get_match(text))

    try:
        caller = sys._getframe(1)
        globals = dict(caller.f_globals)
        locals = dict(caller.f_locals)
        module = globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        globals = {}
        locals = {}
        module = __name__

    regex, fields = parser.parse(pattern, globals, locals)

    namespace = {
        "__module__": module,
        "__init__": _init,
        "_setattrs": _setattrs,
        "_regex": re.compile(regex),
        "_fields": fields,
        "_parse": _parse,
        "_get_match": _get_match,
        "_parse_many": _parse_many,
        "_pattern": pattern,
    }

    return type(typename, (), namespace)


@classmethod
def _parse(cls, text):
    return cls._setattrs(cls(), cls._get_match(text))


@classmethod
def _get_match(cls, text):
    match = cls._regex.search(text)
    if not match:
        raise ValueError(
            f"Text '{text}' does not match pattern '{cls._pattern}'")
    return match


@classmethod
def _parse_many(cls, text):
    return [cls._setattrs(cls(), m) for m in cls._regex.finditer(text)]


@classmethod
def _setattrs(cls, instance, match):
    for field, text in zip(cls._fields, match.groups()):
        field.set_value(instance, text)
    return instance
