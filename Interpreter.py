from .ErrorHandler import RTError
from .SymbolTable import SymbolTable
from .Value import Value
from .Context import Context
from .Lexer import TOKENS, KEYWORDS

class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def add(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_Context(self.context), None
        else:
            return None, Value.illegal_op(self.start_pos, other.end_pos)
        
    def sub(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_Context(self.context), None
        else:
            return None, Value.illegal_op(self.start_pos, other.end_pos)
    
    def mul(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_Context(self.context), None
        else:
            return None, Value.illegal_op(self.start_pos, other.end_pos)
    
    def div(self, other):
        if isinstance(other, Number):
            if other.value != 0:
                return Number(self.value / other.value).set_Context(self.context), None
            else:
                start, end = other.get_Pos()
                self.error = RTError("ZeroDivisionError", "Division By Zero" ,context=self.context, pos_start=start, pos_end=end)
                return None, self.error
        else:
            return None, Value.illegal_op(self.start_pos, other.end_pos)

    def pow(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_Context(self.context), None
        else:
            return None, Value.illegal_op(self.start_pos, other.end_pos)

    def compare_ee(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_Context(self.context), None
        else:
            return None, Value.illegal_op(self.start_pos, other.end_pos)
        
    def compare_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_Context(self.context), None
        else:
            return None, Value.illegal_op(self.start_pos, other.end_pos)
        
    def compare_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_Context(self.context), None
        else:
            return None, Value.illegal_op(self.start_pos, other.end_pos)
        
    def compare_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_Context(self.context), None
        else:
            return None, Value.illegal_op(self.start_pos, other.end_pos)
        
    def compare_le(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_Context(self.context), None
        else:
            return None, Value.illegal_op(self.start_pos, other.end_pos)
        
    def compare_ge(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_Context(self.context), None
        else:
            return None, Value.illegal_op(self.start_pos, other.end_pos)

    def and_(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_Context(self.context), None
        else:
            return None, Value.illegal_op(self.start_pos, other.end_pos)
        
    def or_(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_Context(self.context), None
        else:
            return None, Value.illegal_op(self.start_pos, other.end_pos)

    def not_(self):
        return Number(1 if self.value == 0 else 0).set_Context(self.context), None

    def true_(self):
        return self.value != 0

    def copy(self):
        copy = Number(self.value)
        copy.set_Pos(self.end_pos, self.end_pos)
        copy.set_Context(self.context)

        return copy

    def __repr__(self):
        return str(self.value)

class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def add(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_Context(self.context), None
        else:
            return None, Value.illegal_op(self, other)
        
    def mul(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_Context(self.context), None
        else:
            return None, Value.illegal_op(self, other)
        
    def true_(self):
        return len(self.value) > 0
    
    def copy(self):
        copy = String(self.value)
        copy.set_Pos(self.start_pos, self.end_pos)
        copy.set_Context(self.context)
        return copy
    
    def __repr__(self):
        return f'"{self.value}"'

class Function(Value):
    def __init__(self, fn_name, main_node, args):
        super().__init__()
        self.name = fn_name or '<lambda>'
        self.main_node = main_node
        self.args = args

    def execute(self, args):
        interpreter = Interpreter()
        new_context = Context(self.name, self.context, self.start_pos)
        new_context.symbol_table = SymbolTable(new_context.origin.symbol_table)

        if len(args) > len(self.args):
            return None, RTError(None, f"{len(args) - len(self.args)} extra args passed to '{self.name}'", self.context, self.start_pos, self.end_pos)
        
        if len(args) < len(self.args):
            return None, RTError(None, f"{len(self.args) - len(args)} not enough args passed to '{self.name}'", self.context, self.start_pos, self.end_pos)
        
        for idx in range(len(args)):
            arg = self.args[idx]
            arg_val = args[idx]
            arg_val.set_Context(new_context)
            new_context.symbol_table.set(arg, arg_val)

        value, error = interpreter.exec(self.main_node, new_context)
        if error:
            return None, error
        return value, None
    
    def copy(self):
        copy = Function(self.name, self.main_node, self.args)
        copy.set_Context(self.context)
        copy.set_Pos(self.start_pos, self.end_pos)
        return copy
    
    def __repr__(self):
        return f"<function {self.name}>"

Global_Symbol_Table = SymbolTable()
Global_Symbol_Table.set("nil", Number(0))
Global_Symbol_Table.set("false", Number(0))
Global_Symbol_Table.set("true", Number(1))

class Interpreter:
    def exec(self, node, context):
        method_name = f"handle_{type(node).__name__}"
        method = getattr(self, method_name, self.no_hdl_method)
        return method(node, context)
    
    def no_hdl_method(self, node, context):
        raise Exception(f"No handle_{type(node).__name__} method defined")
    
    def handle_NumberNode(self, node, context):
        return Number(node.tok[1]).set_Context(context).set_Pos(node.pos_start, node.pos_end), None

    def handle_StringNode(self, node, context):
        return String(node.tok[1]).set_Context(context).set_Pos(node.pos_start, node.pos_end), None

    def handle_BinOpNode(self, node, context):
        left, error = self.exec(node.left, context)
        if error: return None, error

        right, error = self.exec(node.right, context)
        if error: return None, error

        if node.op[0] == TOKENS['+']:
            result, error = left.add(right)
        elif node.op[0] == TOKENS['-']:
            result, error = left.sub(right)
        elif node.op[0] == TOKENS['*']:
            result, error = left.mul(right)
        elif node.op[0] == TOKENS['/']:
            result, error = left.div(right)
        elif node.op[0] == TOKENS['^']:
            result, error = left.pow(right)
        elif node.op[0] == TOKENS['==']:
            result, error = left.compare_ee(right)
        elif node.op[0] == TOKENS['!=']:
            result, error = left.compare_ne(right)
        elif node.op[0] == TOKENS['<']:
            result, error = left.compare_lt(right)
        elif node.op[0] == TOKENS['>']:
            result, error = left.compare_gt(right)
        elif node.op[0] == TOKENS['<=']:
            result, error = left.compare_le(right)
        elif node.op[0] == TOKENS['>=']:
            result, error = left.compare_ge(right)
        elif node.op[0] == TOKENS['key'] and node.op[1] == KEYWORDS['AND']:
            result, error = left.and_(right)
        elif node.op[0] == TOKENS['key'] and node.op[1] == KEYWORDS['OR']:
            result, error = left.or_(right)

        if error:
            return None, error
        else:
            return result.set_Pos(node.pos_start, node.pos_end), None

    def handle_UnaryOpNode(self, node, context):
        number, error = self.exec(node.node, context)
        if error: return None, error

        if node.op[0] == TOKENS['-']:
            number, error = number.mul(Number(-1))
        elif node.op[0] == TOKENS['key'] and node.op[1] == KEYWORDS['NOT']:
            number, error = number.not_()

        if error:
            return None, error
        else:
            return number.set_Pos(node.pos_start, node.pos_end), None
        
    def handle_VarAccessNode(self, node, context):
        var = node.var_tok[1]
        value = context.symbol_table.get(var)

        if not value:
            error = RTError("Runtime Error", f"{var} is not defined", context, node.pos_start, node.pos_end)
            return None, error
        
        value = value.copy().set_Pos(node.pos_start, node.pos_end)
        return value, None
    
    def handle_VarAssignNode(self, node, context):
        var = node.var_tok[1]
        value, error = self.exec(node.value_node, context)
        if error: return None, error

        context.symbol_table.set(var, value)
        return value, None

    def handle_IfStatementNode(self, node, context):
        for check, expr in node.cases:
            check_result, error = self.exec(check, context)
            if error: return None, error

            if check_result.true_():
                expr_result, error = self.exec(expr, context)
                if error: return None, error
                return expr_result, error
            
        if node.else_case:
            else_result, error = self.exec(node.else_case, context)
            if error: return None, error
            return else_result, error

        return None, None

    def handle_ForStatementNode(self, node, context):
        start_val, error = self.exec(node.start_node, context)
        if error: return None, error

        end_val, error = self.exec(node.end_node, context)
        if error: return None, error

        if node.step_node:
            step_val, error = self.exec(node.step_node, context)
            if error: return None, error
        else:
            step_val = Number(1)

        idx = start_val.value

        if step_val.value >= 0:
            check = lambda: idx < end_val.value
        else:
            check = lambda: idx > end_val.value

        while check():
            context.symbol_table.set(node.var_tok[1], Number(idx))
            idx += step_val.value

            _, error = self.exec(node.main_node, context)
            if error: return None, error

        return None, None
    
    def handle_WhileStatementNode(self, node, context):
        while True:
            check, error = self.exec(node.check_node, context)
            if error: return None, error

            if not check.true_(): break

            _, error = self.exec(node.main_node, context)
            if error: return None, error

        return None, None

    def handle_FuncDefNode(self, node, context):
        func = node.var_tok[1] if node.var_tok else None
        main_node = node.main_node
        args = [arg[1] for arg in node.arg_toks]
        func_val = Function(func, main_node, args).set_Context(context).set_Pos(node.pos_start, node.pos_end)

        if node.var_tok:
            context.symbol_table.set(func, func_val)

        return func_val, None
    
    def handle_CallNode(self, node, context):
        args = []

        call_val, error = self.exec(node.call_node, context)
        if error: return None, error

        call_val = call_val.copy().set_Pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            arg, error = self.exec(arg_node, context)
            args.append(arg)
            if error: return None, error

        return_val, error = call_val.execute(args)
        if error: return None, error
        return return_val, None

