import sys

PROMPT = '>> '


def start(cmd_in: sys.stdin, cmd_out: sys.stdout):
    for line in sys.stdin:
        print(PROMPT)
        print(line)
