from enum import (
    auto, # nos permite que automaticamente se asigne un valor al enum
    Enum,
    unique, # nos permite definir que nuestros enum son unicos
)

from typing import (
    Dict,
    NamedTuple
)

@unique
class TokenType(Enum):
    ASSIGN = auto()
    COMMA = auto()
    DIVISION = auto()
    ELSE = auto() # sino
    EOF = auto() # Enf Of File
    EQ = auto()
    FALSE = auto()
    FUNCTION = auto()
    GT = auto()
    IDENT = auto() # Identificador
    IF = auto()
    ILLEGAL = auto() # Cuando un caracter no pertenece al lenguaje
    INT = auto()
    LBRACE = auto() # Llave izquierda {
    LET = auto() # Definición de variables
    LPAREN = auto() # Paréntesis izquierdo (
    LT = auto() # menor que
    MINUS = auto()
    MULTIPLICATION = auto()
    NEGATION = auto()
    NOT_EQ = auto()
    PLUS = auto() # Suma
    RBRACE = auto() # Llave derecha 
    RETURN = auto()
    RPAREN = auto() # Paréntesis derecho )
    SEMICOLON = auto() # PUnto y coma
    STRING = auto()
    TRUE = auto()


class Token(NamedTuple):
    token_type: TokenType
    literal: str

    def __str__(self) -> str:
        return f'Type: {self.token_type}, Literal: {self.literal}'


def lookup_token_type(literal: str) -> TokenType:

    # Una variable keyword que es un diccionario que tiene como llaves strngs y como valores TokenType
    keywords: Dict[str, TokenType] = {
        'falso': TokenType.FALSE,
        'procedimiento': TokenType.FUNCTION,
        'regresa': TokenType.RETURN,
        'si': TokenType.IF,
        'si_no': TokenType.ELSE,
        'variable': TokenType.LET,
        'verdadero': TokenType.TRUE
    }

    # Miramos si es una palabra reservada de nuestro lenguaje, si no lo es, entonces es un identificadir (un nombre de variable p.ej)
    return keywords.get(literal, TokenType.IDENT)