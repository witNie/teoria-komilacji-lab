#!/usr/bin/python


class Symbol:
    def __init__(self, name, type, size):
        self.name = name
        self.type = type
        self.size = size

    def __str__(self):
        return f"Symbol(name={self.name}, type={self.type}, size={self.size})"



# class VariableSymbol(Symbol):
#
#     def __init__(self, name, type):
#         super.__init__(name)
#         self.type = type
#     #


class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.symbols = {}
    #

    def __str__(self):
        lines = [f"SymbolTable: {self.name}"]
        for symbol in self.symbols.values():
            lines.append(str(symbol))
        return "\n".join(lines)

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol
    #

    def get(self, name): # get variable symbol or fundef from <name> entry
        if name in self.symbols.keys():
            return self.symbols[name]
        elif self.parent is not None:
            return self.parent.get(name)
        else:
            return None
    #

    def getParentScope(self):
        return self.parent
    #

    def pushScope(self, name):
        return SymbolTable(self, name)
    #

    def popScope(self):
        return self.parent
    #


