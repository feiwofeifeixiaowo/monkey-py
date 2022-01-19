import sys
from typing import List

import lexer
import parser
import evaluator
import environment

PROMPT = '>> '


def start(cmd_in: sys.stdin, cmd_out: sys.stdout):
    print(PROMPT, end='', flush=True, file=cmd_out)
    env = environment.new_environment()
    try:
        for line in sys.stdin:
            if not line.strip():
                print(PROMPT, end='', flush=True, file=cmd_out)
                continue
            l = lexer.new(line)
            p = parser.new(l)

            program = p.parse_program()
            if len(p.errors()) != 0:
                print_parser_errors(cmd_out, p.errors())
                continue
            evaluated = evaluator.evals(program, env)
            if evaluated:
                print(evaluated.inspect(), file=cmd_out)
            print(PROMPT, end='', flush=True, file=cmd_out)
    except KeyboardInterrupt:
        print('\nmeeting ctrl c, quit...')


MONKEY_FACE = r'''
   .--.  .-"     "-.  .--.
  / .. \/  .-. .-.  \/ .. \
 | |  '|  /   Y   \  |'  | |
 | \   \  \ 0 | 0 /  /   / |
  \ '- ,\.-"""""""-./, -' /
   ''-' /_   ^ ^   _\ '-''
       |  \._   _./  |
       \   \ '~' /   /
        '._ '-=-' _.'
           '-----'
'''


def print_parser_errors(out: sys.stdout, errors: List[str]):
    print(MONKEY_FACE, file=out)
    print('Woops! We ran into some monkey business here!\n', file=out)
    print(' parser errors:\n')
    for msg in errors:
        print(msg + '\t' + '\n', file=out)
