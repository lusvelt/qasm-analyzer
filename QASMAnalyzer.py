from Parser import Parser
from Subroutine import SubroutineClassifier
from SymbolicExecutionEngine import SymbolicExecutionEngine


class QASMAnalyzer:
    @staticmethod
    def checkQubitBound(programPath, upperBound):
        tree = Parser.buildParseTree(programPath)
        classifier = SubroutineClassifier(tree)

