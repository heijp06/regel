import re
import sys
from parsec import ParseError, digit, generate, letter, many, none_of, string
from functools import reduce

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
        regex, fields, funcLists = _regel.parse_strict(pattern)
    except ParseError as err:
        raise ValueError(
            f"Error parsing pattern '{pattern}' at position {err.loc()}.")

    seen = set()
    for field in fields:
        if field in seen:
            raise ValueError(f"Duplicate field '{field}'.")
        seen.add(field)

    try:
        caller = sys._getframe(1)
        f_globals = dict(caller.f_globals)
        f_locals = dict(caller.f_locals)
        module = f_globals.get('__name__', '__main__')
    except (AttributeError, ValueError):
        f_globals = {}
        f_locals = {}
        module = __name__

    funcLists = [
        [
            (application, eval(func, f_globals, f_locals))
            for (application, func)
            in funcs
        ]
        for funcs in funcLists
    ]

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


@generate
def _regel():
    head = yield _text
    tail = yield many(_field_with_funcs + _text)
    regex = "(.*)".join([head, *[re.escape(t) for _, t in tail]])
    fields = [f[0] for f, _ in tail]
    funcs = [f[1] for f, _ in tail]
    return regex, fields, funcs


@generate
def _text():
    chars = yield many(_open_brace ^ _close_brace ^ _backslash ^ none_of("{}"))
    return "".join(chars)


@generate
def _open_brace():
    yield string("\{")
    return "{"


@generate
def _close_brace():
    yield string("\}")
    return "}"


@generate
def _backslash():
    yield string("\\\\")
    # A backslash still needs to be escaped in the regex.
    return "\\\\"


@generate
def _func():
    chars = yield many(_open_brace ^ _close_brace ^ _backslash ^ _colon ^ none_of("{:}"))
    return "".join(chars)


@generate
def _colon():
    yield string("\:")
    return ":"


@generate
def _field_with_funcs():
    yield string("{")
    identifier = yield _identifier
    funcs = yield many((string("::") ^ string(":")) + _func)
    yield string("}")
    return identifier, funcs


@generate
def _identifier():
    head = yield letter()
    tail = yield many(string("_") | letter() | digit())
    return head + "".join(tail)
