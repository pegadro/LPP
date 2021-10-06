from unittest import TestCase

from lpp.ast import (
    Expression,
    ExpressionStatement,
    Prefix,
    Program,
    LetStatement,
    ReturnStatement,
    Identifier,
    Integer,
    Infix
)

from typing import (
    Any,
    List,
    cast,
    Type,
    Tuple
)

from lpp.lexer import Lexer
from lpp.parser import Parser


class ParserTest(TestCase):

    def test_parse_program(self) -> None:
        source: str = 'variable x = 5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        # Comprobamos que el programa no es nulo y que es una instancia de Program, el cual es devolvido por parser.parse_program()
        self.assertIsNotNone(program)
        self.assertIsInstance(program, Program)

    def test_let_statements(self) -> None:
        source: str = '''
            variable x = 5;
            variable y = 10;
            variable foo = 20;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        # Comprobamos que el número de statements del programa sean 3, que son los del source
        self.assertEqual(len(program.statements), 3)

        # Por cada statement en los statements del program
        for statement in program.statements:
            # comprobamos que la literal del token del statement sea igual a 'variable'
            self.assertEqual(statement.token_literal(), 'variable')
            # comprobamos que el statement sea instancia de LetStatement
            self.assertIsInstance(statement, LetStatement)

    def test_names_in_let_statement(self) -> None:
        source: str = '''
            variable x = 5;
            variable y = 10;
            variable foo = 20;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        # Creamos una listas de str que seran la lista de los nombres
        names: List[str] = []
        for statement in program.statements:
            # Hacemos que el statement sea de tipo LetStatement
            statement = cast(LetStatement, statement)
            assert statement.name is not None # Comprobamos que el name del statement no sea None
            names.append(statement.name.value) # Agregamos el valor del nombre del statement a la lista de nombres

        expected_names: List[str] = ['x', 'y', 'foo']

        # Comprobamos si los names recibidos son los mismos que los esperados
        self.assertEquals(names, expected_names)

    def test_parse_errors(self) -> None:
        source: str = 'variable x 5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        # Comprobamos que el número de errores sea igual a 1
        self.assertEquals(len(parser.errors), 1)

    def test_return_statement(self) -> None:
        source: str = '''
            regresa 5;
            regresa foo;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        # Comprobamos que la longitud de los statements sea de 2 
        self.assertEquals(len(program.statements), 2)

        # Por cada statement en los statements del program
        for statement in program.statements:
            # Comprobamos que la literal del token del statement sea 'regresa'
            # Es decir, comprobamos que si es un return
            self.assertEquals(statement.token_literal(), 'regresa')
            # Comprobamos que el statement es una instancia de ReturnStatement
            self.assertIsInstance(statement, ReturnStatement)

    def test_identifier_expression(self) -> None:
        source: str = 'foobar;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()
        
        # Esta función hace tests, no lo colocamos aquí para dividir el código y que no parezca demasiado abultado
        self._test_program_statements(parser, program)

        # Hacemos que el expression_statement sea de tipo ExpressionStatement
        expression_statement = cast(ExpressionStatement, program.statements[0])

        # Comprobamos si el expression es None
        assert expression_statement.expression is not None 
        # Creamos una serie de test con el expression
        self._test_literal_expression(expression_statement.expression, 'foobar')

    def test_integer_expressions(self) -> None:
        source: str = '5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()
        # Si hay un error en el parser este tests no dirá que hay error
        self._test_program_statements(parser, program)

        # Hacemos que el primer statement del programa sea de tipo ExpressionStatement
        expression_statement = cast(ExpressionStatement, program.statements[0])

        # Nos aseguramos que la expresión no sea None, que es donde debería vivir el 5
        assert expression_statement.expression is not None

        self._test_literal_expression(expression_statement.expression, 5)

    def test_prefix_expression(self) -> None:
        source: str = '!5; -15;'

        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        # Probamos nuestros program statements
        self._test_program_statements(parser, program, expected_statement_count=2)

        # Generamos un loop a lo largo de statements y también cuales son los valores que esperamos.
        # zip nos permite generar un loop a lo largo de 2 listas o iterables.
        # program.statements en la lista de la statements 
        for statement, (expected_operator, expected_value) in zip(
                program.statements, [('!', 5), ('-', 15)]):
            # hacemos un cast para que se vuelva ExpressionStatement
            statement = cast(ExpressionStatement, statement)
            # Nos aseguramos que sea una instancia de prefijo
            self.assertIsInstance(statement.expression, Prefix)

            # Tornamos el expression un Prefix
            prefix = cast(Prefix, statement.expression)
            # Nos aseguramos que el operador que esperamos sea el operador que tiene el prefijo
            self.assertEquals(prefix.operator, expected_operator)

            # Nos aseguramos que el lado derecho del prefijo no sea None (osea, el valor)
            assert prefix.right is not None

            # Probamos que el lado derecho sea el expected_value
            self._test_literal_expression(prefix.right, expected_value)

    def test_infix_expressions(self) -> None:
        source: str = '''
            5 + 5;
            5 - 5;
            5 * 5;
            5 / 5;
            5 > 5;
            5 < 5;
            5 == 5;
            5 != 5;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        # Probamos nuestros program statements
        self._test_program_statements(parser, program, expected_statement_count=8)
        
        # Valores esperados
        expected_operators_and_values: List[Tuple[Any, str, Any]] = [
            (5, '+', 5),
            (5, '-', 5),
            (5, '*', 5),
            (5, '/', 5),
            (5, '>', 5),
            (5, '<', 5),
            (5, '==', 5),
            (5, '!=', 5),
        ]

        for statement, (expected_left, expected_operator, expected_right) in zip(
                program.statements, expected_operators_and_values):
            statement = cast(ExpressionStatement, statement)
            assert statement.expression is not None
            self.assertIsInstance(statement.expression, Infix)

            self._test_infix_expression(statement.expression,
                                        expected_left,
                                        expected_operator,
                                        expected_right)
    
    def _test_infix_expression(self,
                               expression: Expression,
                               expected_left: Any,
                               expected_operator: str,
                               expected_right: Any):
        infix = cast(Infix, expression)

        assert infix.left is not None
        self._test_literal_expression(infix.left, expected_left)

        self.assertEquals(infix.operator, expected_operator)

        assert infix.right is not None
        self._test_literal_expression(infix.right, expected_right)

    def _test_program_statements(
                                self,
                                parser: Parser,
                                program: Program,
                                expected_statement_count: int = 1) -> None:

        if parser.errors:
            print(parser.errors)

        # Comprobamos que los errores del parser sean 0
        self.assertEquals(len(parser.errors), 0)
        # Comprobamos que el número de statements sea de 1 (foobar;)
        self.assertEquals(len(program.statements), expected_statement_count)
        # Comprobamos que el token type del statment es una instancia de expressionStatement
        self.assertIsInstance(program.statements[0], ExpressionStatement)

    def _test_literal_expression(self,
                                expression: Expression,
                                expected_value: Any) -> None:
        # A esta variable asignamos el tipo de valor del literal/expression
        value_type: Type = type(expected_value)

        # Si el tipo de valor es str
        if value_type == str:
            # Volveremos a hacer otros tests, con el expression y el expected_value
            self._test_identifier(expression, expected_value)
        elif value_type == int:
            self._test_integer(expression, expected_value)
        else:
            # Lanzamos un error
            self.fail(f'Unhandled type of expression. Got={value_type}')

    def _test_identifier(self,
                        expression: Expression,
                        expected_value: str) -> None:

        # Comprobamos si la expression es una instancia de Identifier
        self.assertIsInstance(expression, Identifier)
        
        # Crearemos una variable identifier la cual hara que la expression sea de tipo Identifier
        identifier = cast(Identifier, expression)
        # Comprobamos que el valor del identifier sea el expected_value ("foobar")
        self.assertEquals(identifier.value, expected_value)
        # Comprobamos que la literal del token sea el expected_value
        self.assertEquals(identifier.token.literal, expected_value)

    def _test_integer(self,
                    expression: Expression,
                    expected_value: int) -> None:
        # Comprobamos que la expresión sea un Integer en lugar de un Identifier
        self.assertIsInstance(expression, Integer)

        # Hacemos nuestro cast para que podamos acceder a value
        integer = cast(Integer, expression)
        self.assertEquals(integer.value, expected_value)
        self.assertEquals(integer.token.literal, str(expected_value))