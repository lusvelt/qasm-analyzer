from Parser import buildParseTree
from Subroutine import SubroutineClassifier
from SymbolicExecutionEngine import SymbolicExecutionEngine

tree = buildParseTree('test.qasm')
subroutineClassifier = SubroutineClassifier(tree)
subroutine = subroutineClassifier.subroutines['func1']
symbolicExecutionTree = SymbolicExecutionEngine.getSubroutineSymbolicExecutionTree(subroutine)
print('End')