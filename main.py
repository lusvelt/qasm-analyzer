from Parser import buildParseTree
from Subroutine import SubroutineClassifier

tree = buildParseTree('test.qasm')
classifier = SubroutineClassifier(tree)