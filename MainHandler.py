from . import Lexer
from . import Parser
from . import Interpreter
from . import Context

def Run(fn, source):
    lexer = Lexer.Lexer(fn, source)
    tokens, error = lexer.tokenize()

    if error: return None, error

    parser = Parser.Parser(tokens)
    ast = parser.parse()

    if ast.error: return None, ast.error

    interpreter = Interpreter.Interpreter()
    context = Context.Context('<program>')
    context.symbol_table = Interpreter.Global_Symbol_Table
    result, error = interpreter.exec(ast.node, context)

    return result, error