import getpass

from repl.repl import *


def main():
    print('Hello {}! This is the Monkey programming language!'.format(getpass.getuser()))
    print('Feel free to type in commands')
    start()


main()
