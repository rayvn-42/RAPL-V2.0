# Lexer.py
# =====================================================================================================================================
# This is the first part of this language, it takes in the raw text and converts it into seperate tokens, (You can find all the supported tokens in TOKENS dictionary) and handles IllegalCharacter error and Some Syntax error too.
# =====================================================================================================================================

import string

from .ErrorHandler import IllegalCharacter_, SyntaxError_
from . import Position

# TOKENS
TOKENS = {
    '+': "PLUS",
    '-': "MINUS",
    '*': "TIMES",
    '/': "DIVIDED",
    '(': "LPAREN",
    ')': "RPAREN",
    '^': "POW",
    '=': "EQ",
    '==': "EE",
    '!=': "NE",
    '<=': "LE",
    '>=': "GE",
    '<': "LT",
    '>': "GT",
    '->': "FNARROW",
    ',': "SEP",
    'key': "KEY",
    'int': "INT",
    'float': "FLOAT",
    'str': "STRING",
    'var': "IDENT",
    'eof': "EOF"
}

KEYWORDS = {
    'VAR': "set",
    'NOT': "not",
    'OR': "or",
    'AND': "and",
    'IF': "if",
    'THEN': "do",
    'ELIF': "elif",
    'ELSE': "else",
    'FOR': "for",
    'FROM': "from",
    'TO': "to",
    'STEP': "by",
    'WHILE': "while",
    'FUNCTION': "fn"
}

NUMBERS = string.digits
LETTERS = string.ascii_letters
NUM_LET = NUMBERS + LETTERS + '_'

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position.Position(0, 0, 0, fn, text)
        self.tokens = []
        self.current_char = None
        self.error = None
        self.keyword_vals = KEYWORDS.values()
    
    def number_lex(self):
        num = ''
        dot_count = 0
        pos_start = self.pos.copy()
        
        while self.pos.idx < len(self.text) and self.text[self.pos.idx] in NUMBERS + '.':
            self.current_char = self.text[self.pos.idx]
            if dot_count == 1 and self.current_char == '.':
                self.pos.advance(self.current_char)
                pos_end = self.pos.copy()
                self.error = SyntaxError_("multiple decimal points", pos_start, pos_end)
                return
            elif self.current_char == '.':
                next_char = self.pos.peek()
                if next_char is None or next_char not in NUMBERS:
                    self.pos.advance(self.current_char)
                    self.error = SyntaxError_("invalid syntax", pos_start, self.pos)
                    return
                dot_count += 1
            num += self.text[self.pos.idx]
            self.pos.advance(self.current_char)
        
        if dot_count == 1:
            self.tokens.append((TOKENS['float'], float(num), (pos_start, self.pos)))
        else:
            self.tokens.append((TOKENS['int'], int(num), (pos_start, self.pos)))

    def string_lex(self):
        str_val = ''
        pos_start = self.pos.copy()
        escape = False
        self.pos.advance()
        escape_lst = {
            'n': "\n",
            't': "\t",
            '\\': "\\",
            "'": "\'",
            '"': "\""
        }

        while self.pos.idx < len(self.text):
            self.current_char = self.text[self.pos.idx]
            if self.current_char == '"' and not escape:
                break

            if escape:
                str_val += escape_lst.get(self.current_char, self.current_char)
                escape = False
            elif self.current_char == '\\':
                escape = True
            else:
                str_val += self.current_char

            self.pos.advance(self.current_char)

        if self.pos.idx >= len(self.text):
            self.error = SyntaxError_("Unterminated string", pos_start, self.pos)
            return

        self.pos.advance(self.current_char)
        self.tokens.append((TOKENS['str'], str_val, (pos_start, self.pos)))

    def identifier_lex(self):
        ident = ''
        pos_start = self.pos.copy()
        
        if self.text[self.pos.idx] == '_':
            self.pos.advance(self.current_char)
            self.error = SyntaxError_("variable cannot begin with '_'", pos_start, self.pos)
            return

        while self.pos.idx < len(self.text) and self.text[self.pos.idx] in NUM_LET:
            self.current_char = self.text[self.pos.idx]
            ident += self.text[self.pos.idx]
            self.pos.advance(self.current_char)
        
        if ident in self.keyword_vals:
            self.tokens.append((TOKENS['key'], ident, (pos_start, self.pos)))
        else:
            self.tokens.append((TOKENS['var'], ident, (pos_start, self.pos)))

    def tokenize(self):
        while self.pos.idx < len(self.text):
            self.current_char = self.text[self.pos.idx]
            
            if self.current_char.isspace():
                self.pos.advance(self.current_char)
                continue

            if self.current_char in NUMBERS + '.':
                self.number_lex()
                if self.error:
                    break
                continue

            if self.current_char in LETTERS + "_":
                self.identifier_lex()
                continue

            if self.current_char in ('"'):
                self.string_lex()
                if self.error:
                    break
                continue

            if self.current_char in TOKENS:
                pos_start = self.pos.copy()
                token = self.current_char
                if self.current_char in ('<', '>', '=', '!', '-'):
                    next_char = self.pos.peek()
                    if next_char in ('=', '>'):
                        token = self.current_char + next_char
                        self.pos.advance(self.current_char)
                self.pos.advance(self.current_char)
                self.tokens.append((TOKENS[token], token, (pos_start, self.pos)))
                continue

            pos_start = self.pos.copy()
            illegal_str = self.current_char
            self.pos.advance(self.current_char)

            while self.pos.idx < len(self.text) and self.text[self.pos.idx] not in (NUMBERS + '.' + LETTERS + '_' + ' \t\n') and self.text[self.pos.idx] not in TOKENS:
                illegal_str += self.text[self.pos.idx]
                self.pos.advance(self.text[self.pos.idx])

            pos_end = self.pos.copy()
            self.error = IllegalCharacter_(f"'{illegal_str}'", pos_start, pos_end)
            break
        
        self.tokens.append((TOKENS['eof'], None, (self.pos.copy(), self.pos.copy())))
        return self.tokens, self.error