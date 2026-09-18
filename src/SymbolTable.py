class SymbolTable:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def get(self, name):
        value = self.variables.get(name, None)
        if value == None and self.parent:
            value = self.parent.get(name)
        return value
    
    def set(self, name, value):
        self.variables[name] = value

    def remove(self, name):
        del self.variables[name]