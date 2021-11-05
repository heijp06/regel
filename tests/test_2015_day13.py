import pytest
from regel import regel
from regel.converters import const, eq, ne, split


def test_seating():
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
