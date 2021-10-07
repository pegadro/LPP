
from typing import List

from lpp.ast import Program
from lpp.evaluator import evaluate
from lpp.lexer import Lexer
from lpp.parser import Parser
from lpp.object import Environment

import readline

from lpp.token import (
    Token,
    TokenType,
)

from lpp.lexer import Lexer

EOF_TOKEN: Token = Token(TokenType.EOF, '')

def _print_parse_errors(errors: List[str]):
    for error in errors:
        print(error)


def start_repl() -> None:
    while (source := input('>> ')) != 'salir()':
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()
        env: Environment = Environment()

        if len(parser.errors) > 0:
            _print_parse_errors(parser.errors)
            continue
            
        evaluated = evaluate(program, env)

        if evaluated is not None:
            print(evaluated.inspect())