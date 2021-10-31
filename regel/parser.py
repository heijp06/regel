import re
from parsec import ParseError, digit, generate, letter, many, none_of, string
from .converter import Converter
from .field import Field


def parse(pattern, globals, locals):
    try:
        regex, fields = _regel.parse_strict(pattern)
    except ParseError as err:
        raise ValueError(
            f"Error parsing pattern '{pattern}' at position {err.loc()}.")

    seen = set()
    for field in fields:
        if field.name in seen:
            raise ValueError(f"Duplicate field name '{field.name}'.")
        seen.add(field.name)

        field.compile(globals, locals)

    return regex, fields


@generate
def _regel():
    head = yield _text
    tail = yield many(_field_with_funcs + _text)
    fields, texts = zip(*tail)
    regex = "(.*)".join([head, *(re.escape(text) for text in texts)])
    return regex, fields


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
    funcs = yield many(_converter)
    yield string("}")
    return Field(identifier, funcs)


@generate
def _converter():
    colons, text = yield (string("::") ^ string(":")) + _func
    application = (
        Converter.APPLICATION_SINGLE if len(colons) == 1
        else Converter.APPLICATION_MANY)
    return Converter(text, application)


@generate
def _identifier():
    head = yield letter()
    tail = yield many(string("_") | letter() | digit())
    return head + "".join(tail)
