import sys

from lexer.lexer import *

PROMPT = '>> '


def start(cmd_in: sys.stdin, cmd_out: sys.stdout):
    print(PROMPT, end='', flush=True, file=cmd_out)
    for line in sys.stdin:
        l = new(line)
        tok = l.next_token()
        while (tok.token_type != TokenType.EOF):
            print(tok, file=cmd_out)
            tok = l.next_token()
        print(PROMPT, end='', flush=True, file=cmd_out)
