
from typing import Optional
from lpp.ast import Identifier, LetStatement, Program, Statement
from lpp.lexer import Lexer
from lpp.token import Token, TokenType


class Parser:

    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._current_token: Optional[Token] = None
        self._peek_token: Optional[Token] = None
        
    def parse_program(self) -> Program:
        program: Program = Program(statements=[])

        assert self._current_token is not None
        # Mientras aún haya tokens se va a mandar a generar un statement
        while self._current_token.token_type != TokenType.EOF:
            statement = self._parse_statement()
            if statement is not None:
                program.statements.append(statement)
        
        return program

    def _parse_let_statement(self) -> Optional(LetStatement):
        assert self._current_token is not None
        let_statement = LetStatement(token=self._current_token)

        # En dado caso que el expected token sí haya sido un IDENT, procederemos a crear una instancia de Identifier con este identificador
        if not self._expected_token(TokenType.IDENT):
            return None

        let_statement.name = Identifier(token=self._current_token, value=self._current_token.literal)

        #después del identificador debe haber un “=”, así que comparamos que el siguiente token sea uno de asignación, 
        # si no lo es, misma historia, hay un error de sintaxis así que retornamos None, si sí lo es, 
        # entonces continuamos revisando los tokens hasta que encontremos el “;”

        if not self._expected_token(TokenType.ASSIGN):
            return None

        # TODO terminar cuando sepamos parsear expresiones

        while self._current_token.token_type != TokenType.SEMICOLON:
            self._advance_tokens()

        return let_statement


    def _parse_statement(self) -> Optional[Statement]:
        assert self._current_token is not None
        # Si el token es LET significa que se quiere declarar una variable
        if self._current_token.token_type == TokenType.LET:
            return self._parse_let_statement()
        else:
            return None