class Converter:
    APPLICATION_SINGLE = 0
    APPLICATION_MANY = 1

    def __init__(self, text, application):
        self.text = text
        self.application = application
        self._function = None
    
    def __repr__(self):
        colons = ":" if self.application == Converter.APPLICATION_SINGLE else "::"
        return colons + self.text

    def compile(self, globals, locals):
        self._function = eval(self.text, globals, locals)

    def convert(self, value):
        if not self._function:
            raise ValueError("Converter is not compiled.")

        return (
            self._function(value) if self.application == Converter.APPLICATION_SINGLE
            else [self._function(elem) for elem in value]
        )
