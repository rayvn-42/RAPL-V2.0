from .Context import Context
from .str_arrow import str_arrow

class Error():
    def __init__(self, name, message, context=None, pos_start=None, pos_end=None):
        self.name = name
        self.message = message
        self.context = context
        self.pos_start = pos_start
        self.pos_end = pos_end

    def build_traceback(self):
        traceback = ''
        pos = self.pos_start
        ctx = self.context

        if not ctx and pos and pos.fn == '<stdin>':
            ctx = Context('<program>', None, None)

        while ctx and pos:
            traceback = f'   File {pos.fn}, line {pos.ln + 1}, in {ctx.trace}\n' + traceback
            pos = ctx.origin_entry_pos
            ctx = ctx.origin

        return 'Traceback (most recent call last):\n' + traceback

    def __str__(self):
        result = self.build_traceback()
        result += f"   {self.name}: {self.message}" if self.message else f"   {self.name}"
        result += '\n' + str_arrow(self.pos_start.fc, self.pos_start, self.pos_end)
        return result

class IllegalCharacter_(Error):
    def __init__(self, message, context=None, pos_start=None, pos_end=None):
        super().__init__("IllegalCharacter", message, context, pos_start, pos_end)


class SyntaxError_(Error):
    def __init__(self, message, context=None, pos_start=None, pos_end=None):
        super().__init__("SyntaxError", message, context, pos_start, pos_end)

class RTError(Error):
    def __init__(self, name, message, context, pos_start, pos_end):
        super().__init__(name if name else "RuntimeError", message, context, pos_start, pos_end)
