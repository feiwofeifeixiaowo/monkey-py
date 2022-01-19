import getpass
import sys

import repl


def main():
    print('Hello {}! This is the Monkey programming language!'.format(getpass.getuser()))
    print('Feel free to type in commands')
    repl.start(sys.stdin, sys.stdout)


main()
