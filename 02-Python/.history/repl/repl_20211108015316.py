import sys

from lexer.lexer import *

PROMPT = '>> '


def start(cmd_in: sys.stdin, cmd_out: sys.stdout):
    for line in sys.stdin:
        print(PROMPT)
        new(line)
        print(line)
