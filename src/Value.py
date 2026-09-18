from .ErrorHandler import RTError

class Value:
    def __init__(self):
        self.set_Pos()
        self.set_Context()

    def set_Pos(self, start_pos=None, end_pos=None):
        self.start_pos = start_pos
        self.end_pos = end_pos
        return self
    
    def get_Pos(self):
        return self.start_pos, self.end_pos
    
    def set_Context(self, context=None):
        self.context = context
        return self
    
    def get_Context(self):
        return self.context
    
    def add(self, other):
        return None, self.illegal_op(other)
        
    def sub(self, other):
        return None, self.illegal_op(other)
    
    def mul(self, other):
        return None, self.illegal_op(other)
    
    def div(self, other):
        return None, self.illegal_op(other)

    def pow(self, other):
        return None, self.illegal_op(other)

    def compare_ee(self, other):
        return None, self.illegal_op(other)
        
    def compare_ne(self, other):
        return None, self.illegal_op(other)
        
    def compare_lt(self, other):
        return None, self.illegal_op(other)
        
    def compare_gt(self, other):
        return None, self.illegal_op(other)
        
    def compare_le(self, other):
        return None, self.illegal_op(other)
        
    def compare_ge(self, other):
        return None, self.illegal_op(other)

    def and_(self, other):
        return None, self.illegal_op(other)
        
    def or_(self, other):
        return None, self.illegal_op(other)

    def not_(self):
        return None, self.illegal_op()

    def true_(self):
        return False
    
    def execute(self, args):
        return None, self.illegal_op()
    
    def copy(self):
        raise Exception("copy method undefined")
    
    def illegal_op(self, other=None):
        if not other: other = self
        return RTError(None, 'Illegal operation', self.context, self.start_pos, other.end_pos)