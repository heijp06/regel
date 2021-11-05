import pytest
from regel import regel
from regel.converters import const, eq, ne, split


def test_bag_contains_other():
    class Contents(regel("Contents", r"{number,\d+:int} {color,\w+ \w+} bag")):
        pass

    class Bag(regel("Bag", "{color} bags contain {contents:Contents._parse_many}.")):
        pass

    bag = Bag("light red bags contain 1 bright white bag, 2 muted yellow bags.")

    assert bag.color == "light red"
    assert len(bag.contents) == 2
    assert bag.contents[0].number == 1
    assert bag.contents[0].color == "bright white"
    assert bag.contents[1].number == 2
    assert bag.contents[1].color == "muted yellow"


def test_bag_contains_no_other():
    class Bag(regel("Bag", "{color} bags contain no {contents:const([])}.")):
        pass

    bag = Bag("faded blue bags contain no other bags.")

    assert bag.color == "faded blue"
    assert len(bag.contents) == 0


@pytest.mark.skip("TODO")
def test_bags_with_and_without_contents():
    pass

