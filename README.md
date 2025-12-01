# RAPL V2.0

**Robust Application Programming Language**

> A dynamically-typed interpreted programming language built with Python

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: In Development](https://img.shields.io/badge/Status-In%20Development-orange.svg)]()
[![Python: 3.x](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)

## About

RAPL (Robust Application Programming Language) is a custom interpreted programming language designed for learning and experimentation. Version 2.0 represents a complete implementation featuring a full lexer, parser, and interpreter with support for variables, functions, control flow, and more.

## Features

- **Dynamic Typing**: Variables automatically infer types (integers, floats, strings)
- **First-Class Functions**: Define and pass functions as values, including anonymous functions
- **Control Flow**: Full support for `if/elif/else`, `for`, and `while` statements
- **Operators**: Arithmetic (`+`, `-`, `*`, `/`, `^`), comparison (`==`, `!=`, `<`, `>`, `<=`, `>=`), and logical (`and`, `or`, `not`)
- **String Operations**: String concatenation and repetition
- **Comprehensive Error Handling**: Detailed error messages with traceback and visual indicators
- **Clean Syntax**: Intuitive keywords and structure inspired by modern languages

### Current Status

- [x] Lexer with full tokenization
- [x] Complete parser with AST generation
- [x] Interpreter with expression evaluation
- [x] Variable assignment and access
- [x] Control flow structures (if/elif/else, for, while)
- [x] Function definitions and calls
- [x] String and numeric data types
- [x] Comprehensive error handling
- [ ] Standard library functions
- [ ] File I/O operations
- [ ] More data structures (lists, dictionaries)

## Requirements

- Python 3.13 or higher

No external dependencies required!

## Installation

```bash
# Clone the repository
git clone https://github.com/rayvn-42/RAPL-V2.0.git
cd RAPL-V2.0

# Run directly using python (A custom shell will be implemented in the future)
>>> from MainHandler import Run
>>> result, error = Run('<stdin>', 'set x = 10')
```

## Quick Start

### Hello World

```rapl
"Hello, World!"
```

print built-in function not yet implemented

### Variables

```rapl
set x = 42
set name = "RAPL"
set pi = 3.14159
```

### Arithmetic

```rapl
set result = (10 + 5) * 2 - 3
set power = 2 ^ 8
```

### Conditionals

```rapl
set age = 18
if age >= 18 do "Adult" else "Minor"
```

### Loops

```rapl
# For loop
for i from 1 to 10 do i * i

# For loop with step
for i from 0 to 100 by 10 do i

# While loop
set x = 0
while x < 5 do set x = x + 1
```

### Functions

```rapl
# Named function
fn greet(name) -> "Hello, " + name
greet("World")

# Anonymous function (lambda)
set double = fn(x) -> x * 2
double(5)

# Function with multiple parameters
fn add(a, b) -> a + b
add(10, 20)
```

## Language Syntax

### Data Types

| Type | Example | Description |
|------|---------|-------------|
| **Integer** | `42`, `-10` | Whole numbers |
| **Float** | `3.14`, `-0.5` | Decimal numbers |
| **String** | `"hello"` | Text in double quotes |
| **Boolean** | `true`, `false` | Represented as 1 and 0 |

### Operators

#### Arithmetic
| Operator | Description | Example |
|----------|-------------|---------|
| `+` | Addition | `5 + 3` → `8` |
| `-` | Subtraction | `5 - 3` → `2` |
| `*` | Multiplication | `5 * 3` → `15` |
| `/` | Division | `6 / 2` → `3.0` |
| `^` | Exponentiation | `2 ^ 3` → `8` |

#### Comparison
| Operator | Description | Example |
|----------|-------------|---------|
| `==` | Equal to | `5 == 5` → `1` |
| `!=` | Not equal to | `5 != 3` → `1` |
| `<` | Less than | `3 < 5` → `1` |
| `>` | Greater than | `5 > 3` → `1` |
| `<=` | Less than or equal | `5 <= 5` → `1` |
| `>=` | Greater than or equal | `5 >= 3` → `1` |

#### Logical
| Operator | Description | Example |
|----------|-------------|---------|
| `and` | Logical AND | `true and false` → `0` |
| `or` | Logical OR | `true or false` → `1` |
| `not` | Logical NOT | `not true` → `0` |

### Keywords

- `set` - Variable declaration
- `if`, `elif`, `else` - Conditional statements
- `do` - Marks the body of control structures
- `for`, `from`, `to`, `by` - For loop components
- `while` - While loop
- `fn` - Function definition
- `and`, `or`, `not` - Logical operators
- `true`, `false`, `nil` - Built-in constants

### String Operations

```rapl
# Concatenation
"Hello " + "World"  # "Hello World"

# Repetition
"Ha" * 3  # "HaHaHa"

# Escape sequences
"Line 1\nLine 2\tTabbed"
```


## Examples

### Fibonacci Sequence

```rapl
fn fib(n) -> if n <= 1 do n else fib(n-1) + fib(n-2)
fib(10)
```

### Factorial

```rapl
fn factorial(n) -> if n <= 1 do 1 else n * factorial(n-1)
factorial(5)
```

### Sum of Range

```rapl
set sum = 0
for i from 1 to 100 do set sum = sum + i
sum
```

### String Manipulation

```rapl
fn repeat_greeting(name, times) -> ("Hello, " + name + "! ") * times
repeat_greeting("Alice", 3)
```

## Error Handling

RAPL provides detailed error messages with:
- Error type and description
- Full traceback showing execution path
- Visual indicator pointing to the error location

Example error output:
```
Traceback (most recent call last):
   File <stdin>, line 1, in <program>
   SyntaxError: Expected ')'
	set x = (10 + 5
	               ^
```

## Architecture

### Three-Stage Interpretation

1. **Lexer** (`Lexer.py`): Converts source code into tokens
2. **Parser** (`Parser.py`): Builds an Abstract Syntax Tree (AST) from tokens
3. **Interpreter** (`Interpreter.py`): Traverses the AST and executes the code

### Key Components

- **Context**: Manages execution scope and traceback information
- **SymbolTable**: Handles variable storage with parent scope support
- **Value Classes**: Represent runtime values (Number, String, Function)
- **Error System**: Comprehensive error types with detailed formatting

## Contributing

Contributions are welcome! This is a learning project and I'm open to suggestions and improvements.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution

- Standard library functions (print, input, math operations)
- Additional data structures (lists, dictionaries)
- File I/O operations
- Better REPL/shell interface
- Documentation and examples
- Performance optimizations

## Known Issues

- No built-in print/input functions yet
- Limited data structures (only numbers and strings, tho I'm gonna add lists very soon)
- No module/import system
- No list or dictionary support yet

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- GitHub: [@rayvn-42](https://github.com/rayvn-42)

---

⭐ Star this repository if you find it interesting or useful for learning!

**Try RAPL**: Clone the repo and start experimenting with your own programming language!