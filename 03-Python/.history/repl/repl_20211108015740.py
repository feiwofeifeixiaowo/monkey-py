import sys

from lexer.lexer import *

PROMPT = '>> '


def start(cmd_in: sys.stdin, cmd_out: sys.stdout):
    for line in sys.stdin:
        print(PROMPT)
        l = new(line)
        tok = l.next_token()
        while (tok.token_type != TokenType.EOF):
            print(tok)
            pass
        print(line)
