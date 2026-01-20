
import sys
from pathlib import Path
from TreePrinter import *
from scanner import Scanner
from mparser import Mparser
from AST import *
from TypeChecker import *

if __name__ == '__main__':

    BASE_DIR = Path(__file__).resolve().parent
    DEFAULT_FILE = BASE_DIR / "lab2" / "example3.m"

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE
        file = open(filename, "r")
        text = file.read()
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    lexer = Scanner()
    parser = Mparser()
    ast = parser.parse(lexer.tokenize(text))
    ast.printTree()

    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    # print(typeChecker.symbol_table)


    # typeChecker = TypeChecker()
    # typeChecker.visit(ast)
