import pytest
from .regel import regel
from .converters import const, eq, ne, split


def test_string_field():
    obj = regel("Obj", "{field}")._parse("value")
    assert obj.field == "value"


def test_string_field_begin():
    obj = regel("Obj", "{field}xxx")._parse("valuexxx")
    assert obj.field == "value"


def test_string_field_middle():
    obj = regel("Obj", "xxx{field}xxx")._parse("xxxvaluexxx")
    assert obj.field == "value"


def test_string_field_end():
    obj = regel("Obj", "xxx{field}")._parse("xxxvalue")
    assert obj.field == "value"


def test_group_in_pattern():
    obj = regel("Obj", "{field} (abc)")._parse("value (abc)")
    assert obj.field == "value"


def test_2015_day13_seating():
    Seating = regel(
        "Seating",
        "{guest1} would {gain:eq('gain')} {happiness:int} happiness units by sitting next to {guest2}."
    )
    seating = Seating._parse(
        "Alice would gain 54 happiness units by sitting next to Bob.")
    assert seating.guest1 == "Alice"
    assert seating.gain == True
    assert seating.happiness == 54
    assert seating.guest2 == "Bob"


def test_local_function():
    def f(x):
        return 1 + int(x)
    obj = regel("Obj", "The number is {number:f}.")._parse("The number is 5.")
    assert obj.number == 6


def test_dictionary():
    obj = regel("Obj", "{dict:lambda x\: \{x\: 5\}}")._parse("five")
    assert "five" in obj.dict
    assert obj.dict["five"] == 5


def test_braces_in_text():
    obj = regel("Obj", "\{not_a_field:int\} {a_field:int}")._parse(
        "{not_a_field:int} 42")
    assert obj.a_field == 42


def test_module_name():
    Obj = regel("Obj", "{field} (abc)")
    assert Obj.__module__ == __name__


def test_constructor():
    Obj = regel("Obj", "{field1:int} {field2:int}")
    obj = Obj("42 43")
    assert obj.field1 == 42
    assert obj.field2 == 43


def test_field_cannot_start_with_underscore():
    with pytest.raises(ValueError):
        regel("Obj", "{_field}")


def test_do_not_use_str_for_no_conversion():
    # Initially str() was used as a no-op string conversion.
    # Which has the below potential problem.
    str = int
    obj = regel("Obj", "{field1}")._parse("42")
    assert obj.field1 == "42"


def test_duplicate_field():
    with pytest.raises(ValueError):
        regel("Obj", "{field} {field}")


def test_split_default_separator():
    obj = regel("Obj", "{fields:split()}.")._parse("one two three.")
    assert obj.fields == ["one", "two", "three"]


def test_split_no_match():
    obj = regel("Obj", "{fields:split(',')}.")._parse("one two three.")
    assert obj.fields == ["one two three"]


def test_split_multiple_delimiters():
    obj = regel("Obj", "{fields:split(', ', ' and ')}.")._parse(
        "one, two and three.")
    assert obj.fields == ["one", "two", "three"]


def test_list_to_ints():
    obj = regel("Obj", "{fields:split()::int}")._parse("1 2 3")
    assert obj.fields == [1, 2, 3]


def test_list_to_ints_to_bools():
    obj = regel("Obj", "{fields:split()::int::eq(2)}")._parse("1 2 3")
    assert obj.fields == [False, True, False]


def test_list_to_ints_to_bools_to_len():
    obj = regel("Obj", "{fields:split()::int::eq(2):len}")._parse("1 2 3")
    assert obj.fields == 3


def test_field_to_list():
    obj = regel("Obj", "{fields::str}")._parse("abc")
    assert obj.fields == ["a", "b", "c"]


def test_colon_in_text():
    obj = regel("Obj", "The value is: {field}")._parse("The value is: 42")
    assert obj.field == "42"


def test_backslash_in_text():
    obj = regel("Obj", r"The path is: {pathname}")._parse(
        r"The path is: c:\temp\readme.txt")
    assert obj.pathname == r"c:\temp\readme.txt"


def test_backslash_before_open_brace():
    obj = regel("Obj", r"The path is: c:\\temp\\{filename}")._parse(
        r"The path is: c:\temp\readme.txt")
    assert obj.filename == "readme.txt"


def test_2020_day7_contains_other():
    class Contents(regel("Contents", "{number:int} {c1} {c2} bag")):
        def __init__(self, row):
            super().__init__(row)
            self.color = f"{self.c1} {self.c2}"

    class Bag(regel("Bag", "{color} bags contain {contents:split(', ', 's, ')::Contents}.")):
        pass

    bag = Bag("light red bags contain 1 bright white bag, 2 muted yellow bags.")

    assert bag.color == "light red"
    assert len(bag.contents) == 2
    assert bag.contents[0].number == 1
    assert bag.contents[0].color == "bright white"
    assert bag.contents[1].number == 2
    assert bag.contents[1].color == "muted yellow"


def test_2020_day7_contains_other():
    class Bag(regel("Bag", "{color} bags contain no {contents:const([])}.")):
        pass

    bag = Bag("faded blue bags contain no other bags.")

    assert bag.color == "faded blue"
    assert len(bag.contents) == 0


@pytest.mark.skip("TODO")
def test_2020_day7_bags_with_and_without_contents():
    pass


def test_parse_many():
    class Number(regel("Number", r"{value,\d+:int}")):
        pass

    numbers = Number._parse_many("1, 2, 3")
    
    assert len(numbers) == 3
    assert numbers[0].value == 1
    assert numbers[1].value == 2
    assert numbers[2].value == 3

# 2020 day 4, passport, dictionary
# 2020 day 7, shiny gold bag, list, object
# 2020 day 14, bitmask program
