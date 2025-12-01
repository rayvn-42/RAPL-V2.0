from .Lexer import TOKENS, KEYWORDS
from .ErrorHandler import SyntaxError_
from .Result import ParseResult

class NumberNode:
    def __init__(self, token):
        self.tok = token

        self.pos_start = self.tok[2][0]
        self.pos_end = self.tok[2][1]

    def __repr__(self):
        return f'{self.tok[0]}:{self.tok[1]}'

class StringNode:
    def __init__(self, token):
        self.tok = token

        self.pos_start = self.tok[2][0]
        self.pos_end = self.tok[2][1]

    def __repr__(self):
        return f'{self.tok[0]}:{self.tok[1]}'

class BinOpNode:
    def __init__(self, left, op, right):
        self.op = op
        self.left = left
        self.right = right

        self.pos_start = self.left.pos_start
        self.pos_end = self.right.pos_end

    def __repr__(self):
        return f'({self.left}, {self.op[0]}:{self.op[1]}, {self.right})'

class UnaryOpNode:
    def __init__(self, op, node):
        self.op = op
        self.node = node

        self.pos_start = self.op[2][0]
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f'({self.op[0]}:{self.op[1]}, {self.node})'

class VarAssignNode:
    def __init__(self, var_tok, value_node):
        self.var_tok = var_tok
        self.value_node = value_node

        self.pos_start = self.var_tok[2][0]
        self.pos_end = self.value_node.pos_end


class VarAccessNode:
    def __init__(self, var_tok):
        self.var_tok = var_tok

        self.pos_start = self.var_tok[2][0]
        self.pos_end = self.var_tok[2][1]

class IfStatementNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) - 1][0]).pos_start

class ForStatementNode:
    def __init__(self, var_tok, start_val_node, end_val_node, main_node, step_val_node):
        self.var_tok = var_tok
        self.start_node = start_val_node
        self.end_node = end_val_node
        self.step_node = step_val_node
        self.main_node = main_node

        self.pos_start = self.var_tok[2][0]
        self.pos_end = self.main_node.pos_end

class WhileStatementNode:
    def __init__(self, check_node, main_node):
        self.check_node = check_node
        self.main_node = main_node

        self.pos_start = self.check_node.pos_start
        self.pos_end = self.main_node.pos_end

class FuncDefNode:
    def __init__(self, var_tok, arg_toks, main_node):
        self.var_tok = var_tok
        self.arg_toks = arg_toks
        self.main_node = main_node

        if self.var_tok:
            self.pos_start = self.var_tok[2][0]
        elif len(self.arg_toks):
            self.pos_start = self.arg_toks[0][2][0]
        else:
            self.pos_start = self.main_node.pos_start
        self.pos_end = self.main_node.pos_end

class CallNode:
    def __init__(self, call_node, arg_nodes):
        self.call_node = call_node
        self.arg_nodes = arg_nodes

        self.pos_start = self.call_node.pos_start
        if len(self.arg_nodes):
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.call_node.pos_end

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
        self.current_tok = None
        self.error = None
        self.advance()

    def advance(self):
        if self.idx < len(self.tokens):
            self.current_tok = self.tokens[self.idx]
            self.idx += 1
        else:
            self.current_tok = None
        return self.current_tok

    def parse(self):
        result = self.expr()
        if not self.error and self.current_tok and self.current_tok[0] != TOKENS['eof']:
            pos_start = self.current_tok[2][0].copy()
            pos_end = self.current_tok[2][1].copy()
            while pos_end.idx < len(pos_end.fc) and pos_end.fc[pos_end.idx] not in '\n':
                pos_end.advance(pos_end.fc[pos_end.idx])
            return result.fail(SyntaxError_(f"Expected float, int, identifier, 'set', '+', '-' or '('", pos_start=pos_start, pos_end=pos_end))
        return result

    def if_sttmnt(self):
        result = ParseResult()
        cases = []
        else_case = None

        if not (self.current_tok[0] == TOKENS['key'] and self.current_tok[1] == KEYWORDS['IF']):
            return result.fail(SyntaxError_("Expected 'if'", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
        
        result.register_advance()
        self.advance()

        check = result.register(self.expr())
        if result.error: return result

        if not (self.current_tok[0] == TOKENS['key'] and self.current_tok[1] == KEYWORDS['THEN']):
            return result.fail(SyntaxError_("Expected 'do'", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
        
        result.register_advance()
        self.advance()

        expr = result.register(self.expr())
        if result.error: return result
        cases.append((check, expr))

        while self.current_tok[0] == TOKENS['key'] and self.current_tok[1] == KEYWORDS['ELIF']:
            result.register_advance()
            self.advance()

            check = result.register(self.expr())
            if result.error: return result

            if not(self.current_tok[0] == TOKENS['key'] and self.current_tok[1] == KEYWORDS['THEN']):
                return result.fail(SyntaxError_("Expected 'do'", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
            
            result.register_advance()
            self.advance()

            expr = result.register(self.expr())
            if result.error: return result
            cases.append((check, expr))

        if self.current_tok[0] == TOKENS['key'] and self.current_tok[1] == KEYWORDS['ELSE']:
            result.register_advance()
            self.advance()

            else_case = result.register(self.expr())
            if result.error: return result

        return result.ok(IfStatementNode(cases, else_case))

    def for_sttmnt(self):
        result = ParseResult()
        
        if not (self.current_tok[0] == TOKENS['key'] and self.current_tok[1] == KEYWORDS['FOR']):
            return result.fail(SyntaxError_("Expected 'for'", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
        
        result.register_advance()
        self.advance()

        if  self.current_tok[0] != TOKENS['var']:
            return result.fail(SyntaxError_("Expected identifier", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
        
        var = self.current_tok
        result.register_advance()
        self.advance()

        if not (self.current_tok[0] == TOKENS['key'] and self.current_tok[1] == KEYWORDS['FROM']):
            return result.fail(SyntaxError_("Expected 'from'", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
        
        result.register_advance()
        self.advance()

        start_val = result.register(self.expr())
        if result.error: return result

        if not (self.current_tok[0] == TOKENS['key'] and self.current_tok[1] == KEYWORDS['TO']):
            return result.fail(SyntaxError_("Expected 'to'", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
        
        result.register_advance()
        self.advance()

        end_val = result.register(self.expr())
        if result.error: return result

        if self.current_tok[0] == TOKENS['key'] and self.current_tok[1] == KEYWORDS['STEP']:
            result.register_advance()
            self.advance()

            step_val = result.register(self.expr())
            if self.error: return result
        else:
            step_val = None

        if not (self.current_tok[0] == TOKENS['key'] and self.current_tok[1] == KEYWORDS['THEN']):
            return result.fail(SyntaxError_("Expected 'then'", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
        
        result.register_advance()
        self.advance()

        main = result.register(self.expr())
        if result.error: return result

        return result.ok(ForStatementNode(var, start_val, end_val, main, step_val))

    def while_sttmnt(self):
        result = ParseResult()
        
        if not (self.current_tok[0] == TOKENS['key'] and self.current_tok[1] == KEYWORDS['WHILE']):
            return result.fail(SyntaxError_("Expected 'while'", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
        
        result.register_advance()
        self.advance()

        check = result.register(self.expr())
        if result.error: return result

        if not (self.current_tok[0] == TOKENS['key'] and self.current_tok[1] == KEYWORDS['THEN']):
            return result.fail(SyntaxError_("Expected 'then'", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
        
        result.register_advance()
        self.advance()

        main = result.register(self.expr())
        if result.error: return result

        return result.ok(WhileStatementNode(check, main))

    def def_func(self):
        result = ParseResult()

        if not (self.current_tok[0] == TOKENS['key'] and self.current_tok[1] == KEYWORDS['FUNCTION']):
            return result.fail(SyntaxError_("Expected 'if'", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
        
        result.register_advance()
        self.advance()

        if self.current_tok[0] == TOKENS['var']:
            var_tok = self.current_tok
            result.register_advance()
            self.advance()
            if self.current_tok[0] != TOKENS['(']:
                return result.fail(SyntaxError_("Expected '('", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
        else:
            var_tok = None
            if self.current_tok[0] != TOKENS['(']:
                return result.fail(SyntaxError_("Expected identifier or '('", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))

        result.register_advance()
        self.advance()
        arg_toks = []

        if self.current_tok[0] == TOKENS['var']:
            arg_toks.append(self.current_tok)
            result.register_advance()
            self.advance()

            while self.current_tok[0] == TOKENS[',']:
                result.register_advance()
                self.advance()

                if self.current_tok[0] != TOKENS['var']:
                    return result.fail(SyntaxError_("Expected identifier", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
                
                arg_toks.append(self.current_tok)
                result.register_advance()
                self.advance()

            if self.current_tok[0] != TOKENS[')']:
                return result.fail(SyntaxError_("Expected ',' or ')'", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
        else:
            if self.current_tok[0] != TOKENS[')']:
                return result.fail(SyntaxError_("Expected identifier or ')'", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
        
        result.register_advance()
        self.advance()

        if self.current_tok[0] != TOKENS['->']:
            return result.fail(SyntaxError_("Expected '->'", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
        
        result.register_advance()
        self.advance()
        return_node = result.register(self.expr())
        if result.error: return result

        return result.ok(FuncDefNode(var_tok, arg_toks, return_node))

    def call(self):
        result = ParseResult()
        base = result.register(self.base())
        if result.error: return result

        if self.current_tok[0] == TOKENS['(']:
            result.register_advance()
            self.advance()
            arg_nodes = []

            if self.current_tok[0] == TOKENS[')']:
                result.register_advance()
                self.advance()
            else:
                arg_nodes.append(result.register(self.expr()))
                if result.error:
                    return result.fail(SyntaxError_("Expected ')', 'set', 'if', 'for', 'while', 'fn', int, float, identifier, '+', '-', '(' or 'not'", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
                
                while self.current_tok[0] == TOKENS[',']:
                    result.register_advance()
                    self.advance()

                    arg_nodes.append(result.register(self.expr()))
                    if result.error: return result

                if self.current_tok[0] != TOKENS[')']:
                    return result.fail(SyntaxError_("Expected ',' or ')'", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
                
                result.register_advance()
                self.advance()
            return result.ok(CallNode(base, arg_nodes))
        return result.ok(base)

    def base(self):
        result = ParseResult()
        tok = self.current_tok

        if tok[0] in (TOKENS['int'], TOKENS['float']):
            result.register_advance()
            self.advance()
            return result.ok(NumberNode(tok))

        if tok[0] == TOKENS['str']:
            result.register_advance()
            self.advance()
            return result.ok(StringNode(tok))

        if tok[0] == TOKENS['var']:
            result.register_advance()
            self.advance()
            return result.ok(VarAccessNode(tok))

        if tok[0] == TOKENS['(']:
            result.register_advance()
            self.advance()
            node = result.register(self.expr())
            if result.error: return result
            if self.current_tok is None or self.current_tok[0] != TOKENS[')']:
                if self.current_tok and self.current_tok[0] == TOKENS['eof']:
                    pos_start = self.current_tok[2][1].copy()
                    pos_end = pos_start.copy()
                else:
                    pos_start = self.current_tok[2][0].copy()
                    pos_end = self.current_tok[2][1].copy()
                return result.fail(SyntaxError_("Expected ')'", pos_start=pos_start, pos_end=pos_end))
            result.register_advance()
            self.advance()
            return result.ok(node)
        
        if tok[0] == TOKENS['key'] and tok[1] == KEYWORDS['IF']:
            if_state = result.register(self.if_sttmnt())
            if result.error: return result
            return result.ok(if_state)
        
        if tok[0] == TOKENS['key'] and tok[1] == KEYWORDS['FOR']:
            for_state = result.register(self.for_sttmnt())
            if result.error: return result
            return result.ok(for_state)

        if tok[0] == TOKENS['key'] and tok[1] == KEYWORDS['WHILE']:
            while_state = result.register(self.while_sttmnt())
            if result.error: return result
            return result.ok(while_state)
        
        if tok[0] == TOKENS['key'] and tok[1] == KEYWORDS['FUNCTION']:
            func = result.register(self.def_func())
            if result.error: return result
            return result.ok(func)

        pos_start = tok[2][0].copy()
        pos_end = tok[2][1].copy()
        while pos_end.idx < len(pos_end.fc) and pos_end.fc[pos_end.idx] not in '\n':
            pos_end.advance(pos_end.fc[pos_end.idx])
        return result.fail(SyntaxError_(f"Expected int, float, identifier, '+', '-', '('", pos_start=pos_start, pos_end=pos_end))


    def power(self):
        return self.Op(self.call, (TOKENS['^'], ), self.factor)

    def factor(self):
        result = ParseResult()
        tok = self.current_tok

        if tok[0] == TOKENS['-'] or tok[0] == TOKENS['+']:
            result.register_advance()
            self.advance()
            factor_node = result.register(self.factor())
            if result.error: return result
            return result.ok(UnaryOpNode(tok, factor_node))

        return self.power()

    def term(self):
        return self.Op(self.factor, (TOKENS['*'], TOKENS['/']))

    def arithmatic(self):
        return self.Op(self.term, (TOKENS['+'], TOKENS['-']))
    
    def comparison(self):
        result = ParseResult()

        if self.current_tok[0] == TOKENS['key'] and self.current_tok[1] == KEYWORDS['NOT']:
            op = self.current_tok
            result.register_advance()
            self.advance()

            node = result.register(self.comparison())
            if result.error: return result
            return result.ok(UnaryOpNode(op, node))

        node = result.register(self.Op(self.arithmatic, (TOKENS['<'], TOKENS['>'], TOKENS['=='], TOKENS['!='], TOKENS['<='], TOKENS['>='])))

        if result.error:
            return result.fail(SyntaxError_("Expected int, float, identifier, '+', '-', '(' or 'not'", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
        
        return result.ok(node)

    def expr(self):
        result = ParseResult()

        if self.current_tok[0] == TOKENS['key'] and self.current_tok[1] == KEYWORDS['VAR']:
            result.register_advance()
            self.advance()

            if self.current_tok[0] != TOKENS['var']:
                return result.fail(SyntaxError_(f"Expected Identifier", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))

            var = self.current_tok
            result.register_advance()
            self.advance()

            if self.current_tok[0] != TOKENS['=']:
                return result.fail(SyntaxError_(f"Expected '='", pos_start=self.current_tok[2][0], pos_end=self.current_tok[2][1]))
            
            result.register_advance()
            self.advance()
            
            expr = result.register(self.expr())
            if result.error: return result
            return result.ok(VarAssignNode(var, expr))
        
        node = result.register(self.Op(self.comparison, ((TOKENS['key'], KEYWORDS['AND']), (TOKENS['key'], KEYWORDS['OR']))))

        if result.error:
            return result.fail(SyntaxError_("Expected 'set', int, float, '+', '-', '(' or identifier", pos_start=self.current_tok[2][1], pos_end=self.current_tok[2][1]))
        return result.ok(node)

    def Op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        result = ParseResult()
        left = result.register(func_a())
        if result.error: return result
        
        while self.current_tok is not None:
            match_ = False
            for op_check in ops:
                if isinstance(op_check, tuple):
                    if self.current_tok[0] == op_check[0] and self.current_tok[1] == op_check[1]:
                        match_ = True
                        break
                else:
                    if self.current_tok[0] == op_check:
                        match_ = True
                        break
            
            if not match_:break

            op = self.current_tok
            result.register_advance()
            self.advance()
            right = result.register(func_b())
            if result.error: return result
            left = BinOpNode(left, op, right)
        
        return result.ok(left)