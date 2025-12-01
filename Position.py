# Position.py
# =====================================================================================================================================
# Position Handler for Language, it keeps track of the current index(idx), line(ln), column(col), filename(fn) and filecontent(fc).
# It has an advance method the advances to the next char, and if char is a newline indicator(\n), then it increments the line counter.
# It also has a peek method which looks and retrieves the next char after the current char.
# It has also a copy method, which just copies the Position into a copy of itself.
# =====================================================================================================================================

class Position:
    def __init__(self, idx, ln, col, fn, fc):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.fc = fc

    def advance(self, char=None):
        self.idx += 1
        self.col += 1

        if char == '\n':
            self.ln += 1
            self.col = 0
        return self

    def peek(self):
        return self.fc[self.idx + 1] if self.idx + 1 < len(self.fc) else None

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.fc)