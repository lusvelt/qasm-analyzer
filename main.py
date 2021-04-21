from Parser import buildParseTree
from Subroutine import SubroutineClassifier
from Expression import Expression

def getExpression(statementNode):
    expressionNode = statementNode.getChild().getChild().getChild(1).getChild(1).getChild(1)
    assert expressionNode.type == 'expression'
    return Expression(expressionNode)

tree = buildParseTree('test.qasm')
statements = tree.getChildrenByType('statement')
expressions = [ getExpression(statement) for statement in statements]
