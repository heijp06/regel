import re


class Rule:
    def __init__(self, regex, fields, pattern):
        self.regex = re.compile(regex)
        self.fields = fields
        self.pattern = pattern

    def apply(self, cls_factory, text):
        return self._setattrs(cls_factory(), self._get_match(text))

    def apply_many(self, cls_factory, text):
        return [
            self._setattrs(cls_factory(), match)
            for match
            in self.regex.finditer(text)
        ]

    def _get_match(self, text):
        match = self.regex.search(text)
        if not match:
            raise ValueError(
                f"Text '{text}' does not match pattern '{self._pattern}'")
        return match

    def _setattrs(self, instance, match):
        items = []
        for field, text in zip(self.fields, match.groups()):
            field.set_value(instance, text)
            items.append(field.get_value(instance))
        instance._items = tuple(items)
        return instance
