class Context:
    def __init__(self, trace, origin=None, origin_entry_pos=None):
        self.trace = trace
        self.origin = origin
        self.origin_entry_pos = origin_entry_pos
        self.symbol_table = None