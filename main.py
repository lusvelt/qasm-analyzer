from Parser import Parser
from Subroutine import SubroutineClassifier
from SymbolicExecutionEngine import SymbolicExecutionEngine

tree = Parser.buildParseTree('test.qasm')
classifier = SubroutineClassifier(tree)
symbolicExecutionTrees = []
for identifier in classifier.subroutines.keys():
    subroutine = classifier.subroutines[identifier]
    symbolicExecutionTree = SymbolicExecutionEngine.getSubroutineSymbolicExecutionTree(subroutine)
    symbolicExecutionTrees.append(symbolicExecutionTree)
pass