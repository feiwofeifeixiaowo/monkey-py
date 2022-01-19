import unittest
from typing import NamedTuple


class TestNextToken(unittest.TestCase):
    def test_next_token(self):
        input = '=+(){},;'

        class Token:
            def __init__(self, type_name, literal) -> None:
                self.token_type = TokenType(type_name)
                self.literal = literal

        expToken = NamedTuple('expToken', 'expected_type expected_literal')
        tests = [expToken()]
        pass


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    unittest.main()

func
TestNextToken(t * testing.T)
{
    input := ` = +()
{},;
`
tests := []
struct
{
    expectedType
token.TokenType
expectedLiteral
string
}{
    {token.ASSIGN, "="}, {token.PLUS, "+"}, {token.LPAREN, "("}, {token.RPAREN, ")"}, {token.LBRACE, "{"},
    {token.RBRACE, "}"}, {token.COMMA, ","}, {token.SEMICOLON, ";"}, {token.EOF, ""},
}
l := New(input)
for i, tt := range tests {tok := l.NextToken()
if tok.Type != tt.expectedType {
t.Fatalf("tests[%d] - tokentype wrong. expected=%q, got=%q",
}
i, tt.expectedType, tok.Type)
}}
}
