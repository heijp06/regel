import re
from parsec import ParseError, digit, generate, letter, many, none_of, string


def parse(pattern, globals, locals):
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

    funcLists = [
        [
            (application, eval(func, globals, locals))
            for (application, func)
            in funcs
        ]
        for funcs in funcLists
    ]

    return regex, fields, funcLists


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
