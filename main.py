from Parser import buildParseTree
from Subroutine import SubroutineClassifier
from SymbolicExecutionEngine import SymbolicExecutionEngine

n = 5

tree = buildParseTree('test.qasm')
subroutineClassifier = SubroutineClassifier(tree)
keys = subroutineClassifier.subroutines.keys()
subroutines = [subroutineClassifier.subroutines[key] for key in keys]
symbolicExecutionTrees = [SymbolicExecutionEngine.getSubroutineSymbolicExecutionTree(subroutine) for subroutine in subroutines]
print('End')