import pytest
import re
from regel import regel
from regel.converters import const, eq, ne, split


def test_no_conversions():
    class Field(regel("Field", "{name,\w+}:{value,\S+}")):
        pass

    actual = [dict(Field._parse_many(passport))
              for passport in passports.split("\n\n")]
    # actual = [
    #     dict(match.groups() for match in re.finditer("(\w+):(\S+)", passport))
    #     for passport
    #     in passports.split("\n\n")]

    expected = [
        {"ecl": "gry", "pid": "860033327", "eyr": "2020", "hcl": "#fffffd",
            "byr": "1937", "iyr": "2017", "cid": "147", "hgt": "183cm"},
        {"iyr": "2013", "ecl": "amb", "cid": "350", "eyr": "2023",
            "pid": "028048884", "hcl": "#cfa07d", "byr": "1929"},
        {"hcl": "#ae17e1", "iyr": "2013", "eyr": "2024", "ecl": "brn",
            "pid": "760753108", "byr": "1931", "hgt": "179cm"},
        {"hcl": "#cfa07d", "eyr": "2025", "pid": "166559648",
            "iyr": "2011", "ecl": "brn", "hgt": "59in"}
    ]

    assert actual == expected


passports = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""
