from Variable import Symbol, Value, Variable
from Parser import Node

# The following two classes are operator nodes in the Expression AST
# The operator's arguments can be one of the following types:
#   * UnaryOperator
#   * BinaryOperator
#   * Variable
#   * Value
#   * Symbol

# Represents a unitary operator node in the Expression AST
class UnaryOperator:
    def __init__(self, literal:str, arg):
        self.literal = literal
        self.arg = arg

    def __str__(self):
        return self.literal

# Represents a binary operator in the Expression AST
class BinaryOperator:
    def __init__(self, literal:str, arg1, arg2):
        self.literal = literal
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self):
        return self.literal

class SetDeclaration:
    def __init__(self, node:Node):
        assert node.type == 'setDeclaration'
        self.node = node
        child = node.getChild()
        if child.type == 'LBRACE':
            self.items = []
            expressionListNode = node.getChildByType('expressionList')
            expressionNodes = expressionListNode.getChildrenByType('expression')
            for expressionNode in expressionNodes:
                expression = Expression.buildExpressionAST(expressionNode)
                self.items.append(expression)
        elif child.type == 'rangeDefinition':
            expressionNodes = child.getChildrenByType('expression')
            self.start = Expression.buildExpressionAST(expressionNodes[0])
            self.end = Expression.buildExpressionAST(expressionNodes[1])
            self.step = Value('1', 'Integer')
            if expressionNodes[2]:
                self.step = Expression.buildExpressionAST(expressionNodes[2])
        else:
            self.identifier = child.text

class Expression:
    def __init__(self, node:Node):
        assert node.type == 'expression'
        self.node = node
        self.tree = Expression.buildExpressionAST(node)

    @staticmethod
    def buildExpressionAST(node:Node):
        assert node.type == 'expression'
        child = node.getChild()
        if child.type == 'expression':
            expressionNode = child
            literal = node.children[1].text
            subExpressionNode = node.getChildByType('xOrExpression')
            expression = Expression.buildExpressionAST(expressionNode)
            subExpression = Expression.__buildSubExpressionAST(subExpressionNode)
            return BinaryOperator(literal, expression, subExpression)
        elif child.type == 'xOrExpression':
            return Expression.__buildSubExpressionAST(child)
        elif child.type == 'unaryExpression':
            return Expression.__buildUnaryExpressionAST(child)
        else:
            return Expression.__buildExpressionTerminatorAST(child)

    @staticmethod
    def __buildSubExpressionAST(node):
        assert node.type in ['xOrExpression', 'bitAndExpression', 'bitShiftExpression', 'additiveExpression', 'multiplicativeExpression']
        child = node.getChild()
        if node.type != 'multiplicativeExpression':
            if len(node.children) == 1:
                return Expression.__buildSubExpressionAST(child)
            else:
                leftExpressionNode = node.children[0]
                literal = node.children[1].text
                rightExpressionNode = node.children[2]
                leftExpression = Expression.__buildSubExpressionAST(leftExpressionNode)
                rightExpression = Expression.__buildSubExpressionAST(rightExpressionNode)
                return BinaryOperator(literal, leftExpression, rightExpression)
        else:
            if child.type == 'multiplicativeExpression':
                multiplicativeExpression = Expression.__buildSubExpressionAST(child)
                literal = node.children[1].text
                rightExpressionNode = node.children[2]
                if rightExpressionNode.type == 'expressionTerminator':
                    rightExpression = Expression.__buildExpressionTerminatorAST(rightExpressionNode)
                else:
                    rightExpression = Expression.__buildUnaryExpressionAST(rightExpressionNode)
                return BinaryOperator(literal, multiplicativeExpression, rightExpression)
            elif child.type == 'unaryExpression':
                return Expression.__buildUnaryExpressionAST(child)
            else:
                return Expression.__buildExpressionTerminatorAST(child)

    @staticmethod
    def __buildUnaryExpressionAST(node:Node):
        assert node.type == 'unaryExpression'
        unaryOperatorNode = node.getChildByType('unaryOperator')
        literal = unaryOperatorNode.getChild().text
        expressionTerminatorNode = node.getChildByType('expressionTerminator')
        expressionTerminator = Expression.__buildExpressionTerminatorAST(expressionTerminatorNode)
        return UnaryOperator(literal, expressionTerminator)

    @staticmethod
    def __buildExpressionTerminatorAST(node):
        assert node.type == 'expressionTerminator'
        child = node.getChild()
        if child.type == 'Identifier':
            return Variable(child.text)
        elif child.type in ['Constant', 'Integer', 'RealNumber', 'StringLiteral']:
            return Value(child.text, child.type)
        elif child.type in ['buildInCall', 'subroutineCall']:
            pass
        elif child.type == 'MINUS':
            expressionTerminatorNode = node.getChildByType('expressionTerminator')
            expressionTerminator = Expression.__buildExpressionTerminatorAST(expressionTerminatorNode)
            return UnaryOperator('-', expressionTerminator)
        elif child.type == 'LPAREN':
            expressionNode = node.getChildByType('expression')
            return Expression.buildExpressionAST(expressionNode)
        elif node.children[1].type == 'LBRACKET':
            expressionTerminatorNode = child
            literal = '[]'
            expressionNode = node.getChildByType('expression')
            expressionTerminator = Expression.__buildExpressionTerminatorAST(expressionTerminatorNode)
            expression = Expression.buildExpressionAST(expressionNode)
            return BinaryOperator(literal, expressionTerminator, expression)
        else:
            expressionTerminatorNode = child
            literal = node.getChildByType('incrementor').text
            expressionTerminator = Expression.__buildExpressionTerminatorAST(expressionTerminatorNode)
            return UnaryOperator(literal, expressionTerminator)


class BooleanExpression:
    def __init__(self, node:Node):
        assert node.type == 'booleanExpression'
        self.node = node
        self.tree = BooleanExpression.__buildBooleanExpressionAST(node)

    @staticmethod
    def __buildBooleanExpressionAST(node: Node):
        assert node.type == 'booleanExpression'
        child = node.getChild()
        if child.type == 'booleanExpression':
            booleanExpressionNode = child
            literal = node.children[1].text
            comparisonExpressionNode = node.getChildByType('comparisonExpression')
            booleanExpression = BooleanExpression.__buildBooleanExpressionAST(booleanExpressionNode)
            comparisonExpression = BooleanExpression.__buildComparisonExpressionAST(comparisonExpressionNode)
            return BinaryOperator(literal, booleanExpression, comparisonExpression)
        elif child.type == 'comparisonExpression':
            return BooleanExpression.__buildComparisonExpressionAST(child)
        else:
            return BooleanExpression.__buildMembershipTestAST(child)

    @staticmethod
    def __buildComparisonExpressionAST(node:Node):
        assert node.type == 'comparisonExpression'
        child = node.getChild()
        if len(node.children) == 1:
            literal = '!!' # JavaScript-equivalent for truthy value (non-zero for integers, non-empty for strings, true for booleans and so on)
            expressionNode = child
            expression = Expression.buildExpressionAST(expressionNode)
            return UnaryOperator(literal, expression)
        else:
            leftExpressionNode = child
            literal = node.children[1].text
            rightExpressionNode = node.children[2]
            leftExpression = Expression.buildExpressionAST(leftExpressionNode)
            rightExpression = Expression.buildExpressionAST(rightExpressionNode)
            return BinaryOperator(literal, leftExpression, rightExpression)

    @staticmethod
    def __buildMembershipTestAST(node:Node):
        assert node.type == 'membershipTest'
        identifierLiteral = node.getChildByType('Identifier').text
        identifier = Variable(identifierLiteral)
        literal = 'in'
        setDeclarationNode = node.getChildByType('setDeclaration')
        setDeclaration = SetDeclaration(setDeclarationNode)
        return BinaryOperator(literal, identifier, setDeclaration)
