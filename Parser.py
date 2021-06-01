from antlr4 import *
from types import SimpleNamespace
from qasm3sub.qasm3subLexer import qasm3subLexer
from qasm3sub.qasm3subParser import qasm3subParser
from qasm3sub.qasm3subListener import qasm3subListener


# This class is the core of our custom parse tree, it defines
# which syntax data about the QASM program are stored in the tree
class Node:
    def __init__(self, type: str, text: str = None):
        self.type = type if 'T__' not in type else None  # if it's an unnamed token set the type to None
        self.text = text
        self.parent = None
        self.children = []  # list of children rules (order does matter)
        self.position = None  # index of the current Node in parent.children list
        self.rules = {}  # dict which maps a rule type with the (ordered) list of all child rules matching that type
        self.index = None  # index of the current node in parent.rules[self.type]
        self.nextSibling = None  # reference to the next sibling Node, i.e. parent.children[self.position+1] if exists

    def appendChild(self, child: 'Node'):
        child.parent = self
        if len(self.children) > 0:
            self.children[-1].nextSibling = child
        child.position = len(self.children)
        self.children.append(child)
        if child.type not in self.rules.keys():
            self.rules[child.type] = []
        child.index = len(self.rules[child.type])
        self.rules[child.type].append(child)

    def getChildByType(self, type: str, index: int = 0):
        if type not in self.rules.keys():
            return None
        if index >= len(self.rules[type]):
            return None
        return self.rules[type][index]

    def getChildrenByType(self, type: str):
        if type not in self.rules.keys():
            return None
        return self.rules[type]

    def getChild(self, index: int = 0):
        if len(self.children) <= index:
            return None
        return self.children[index]

    def getDescendantsByType(self, type):
        descendants = []
        for child in self.children:
            if child.type == type:
                descendants.append(child)
            descendants += child.getDescendantsByType(type)
        return descendants

    def getSiblingByType(self, type):
        for sibling in self.parent.children:
            if sibling != self and sibling.type == type:
                return sibling

    def getLastChild(self):
        return self.children[len(self.children) - 1]

    def hasChildren(self):
        return len(self.children) > 0

    def __str__(self):
        return (self.type if self.type is not None else 'TOKEN') + ': ' + self.text


# This class works as an interface between the ANTLR generated parse tree
# and our custom tree defined by the `Node` class.
# This listener will be passed to the ANTLR tree walker, and its methods will
# be called as the walker enters or exits nodes or terminators, therefore
# the methods are implemented such that a new, simplified tree is built
# on the way
class ExtractorListener(qasm3subListener):
    def __init__(self, output: SimpleNamespace, parser: qasm3subParser):
        self.output = output  # `output` is a simple object needed to pass the output up to the caller
        self.current = None  # current pointed node in the newly-generated tree
        self.parser = parser  # we need to get some info from the parser to abstract from its references in the tree
        # In the ANTLR-generated parsing tree rules are labeled by an internal index
        self.ruleNames = parser.ruleNames  # we need these so that in our tree every node is labeled with its rule name
        # the same we do with lexer tokens, but tokens info is stored in a file generated by ANTLR which has the form:
        # token1=1
        # token2=2
        # ...
        # so we need to "parse" that file and use its content to build a dict
        self.tokenNames = {}
        with open('qasm3sub/qasm3sub.tokens', 'r') as tokens:
            while True:
                line = tokens.readline().strip()
                if not line:
                    break
                assoc = line.split('=')
                name = ''.join(assoc[0:-1])
                index = int(assoc[-1])
                if index not in self.tokenNames.keys():
                    self.tokenNames[index] = name

    def enterEveryRule(self, ctx: ParserRuleContext):
        ruleName = self.ruleNames[ctx.getRuleIndex()]
        child = Node(ruleName, ctx.getText())
        if self.current is None:
            self.current = self.output.tree = child
        else:
            self.current.appendChild(child)
            self.current = child

    def exitEveryRule(self, ctx: ParserRuleContext):
        self.current = self.current.parent

    def visitTerminal(self, node):
        tokenName = self.tokenNames[node.symbol.type]
        child = Node(tokenName, node.symbol.text)
        self.current.appendChild(child)


# This is the actual function which shall be called from outside
# It accepts a file path as an argument (the QASM source file)
# and it returns our simplified parsing tree
class Parser:
    @staticmethod
    def buildParseTree(filePath: str):
        file = FileStream(filePath)
        lexer = qasm3subLexer(file)
        stream = CommonTokenStream(lexer)
        parser = qasm3subParser(stream)
        tree = parser.program()

        output = SimpleNamespace()
        listener = ExtractorListener(output, parser)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        return output.tree
