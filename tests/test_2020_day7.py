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


def test_bags_with_and_without_contents():
    class Contents(regel("Contents", r"{number,\d+:int} {color,\w+ \w+} bag")):
        pass

    class Bag(regel("Bag", "{color,\w+ \w+} bags contain {contents:Contents._parse_many}.")):
        pass

    bags = Bag._parse_many("""
light red bags contain 1 bright white bag, 2 muted yellow bags.
faded blue bags contain no other bags.
""")

    bag = bags[0]
    assert bag.color == "light red"
    assert len(bag.contents) == 2
    assert bag.contents[0].number == 1
    assert bag.contents[0].color == "bright white"
    assert bag.contents[1].number == 2
    assert bag.contents[1].color == "muted yellow"

    bag = bags[1]
    assert bag.color == "faded blue"
    assert len(bag.contents) == 0


def test_example():
    class Contents(regel("Contents", r"{number,\d+:int} {color,\w+ \w+} bag")):
        pass

    class Bag(regel("Bag", "{color} bags contain {contents:Contents._parse_many}.")):
        pass

    bags = Bag._parse_many("""
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""")

    expected = [
        ["light red", [(1, "bright white"), (2, "muted yellow")]],
        ["dark orange", [(3, "bright white"), (4, "muted yellow")]],
        ["bright white", [(1, "shiny gold")]],
        ["muted yellow", [(2, "shiny gold"), (9, "faded blue")]],
        ["shiny gold", [(1, "dark olive"), (2, "vibrant plum")]],
        ["dark olive", [(3, "faded blue"), (4, "dotted black")]],
        ["vibrant plum", [(5, "faded blue"), (6, "dotted black")]],
        ["faded blue", []],
        ["dotted black", []]
    ]

    actual = get_contents(bags)

    assert expected == actual


def get_contents(bags):
    return [
        [bag.color, [(number, color) for number, color in bag.contents]]
        for bag
        in bags
    ]
