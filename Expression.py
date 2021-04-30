import copy
from sympy import *
from Variable import Value, Variable
from Parser import Node
from Operator import UnaryOperator, BinaryOperator

class SetDeclaration:
    def __init__(self, node: Node):
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
            self.step = Value(1)
            if expressionNodes[2]:
                self.step = Expression.buildExpressionAST(expressionNodes[2])
        else:
            self.identifier = child.text


class Expression:
    def __init__(self, node: Node = None, tree=None, isBoolean=False):
        assert node is None or node.type == 'expression' or node.type == 'booleanExpression'
        if node is not None:
            self.node = node
            self.tree = Expression.buildExpressionAST(node)
        else:
            self.tree = tree
        self.isBoolean = isBoolean

    @staticmethod
    def buildExpressionAST(node: Node):
        assert node.type == 'expression' or node.type == 'booleanExpression'
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
        elif child.type == 'expressionTerminator':
            return Expression.__buildExpressionTerminatorAST(child)
        elif child.type == 'booleanExpression':
            booleanExpressionNode = child
            literal = node.children[1].text
            comparisonExpressionNode = node.getChildByType('comparisonExpression')
            booleanExpression = Expression.buildExpressionAST(booleanExpressionNode)
            comparisonExpression = Expression.__buildComparisonExpressionAST(comparisonExpressionNode)
            return BinaryOperator(literal, booleanExpression, comparisonExpression)
        elif child.type == 'comparisonExpression':
            return Expression.__buildComparisonExpressionAST(child)
        elif child.type == 'membershipTest':
            return Expression.__buildMembershipTestAST(child)

    @staticmethod
    def __buildSubExpressionAST(node):
        assert node.type in ['xOrExpression', 'bitAndExpression', 'bitShiftExpression', 'additiveExpression',
                             'multiplicativeExpression']
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
    def __buildUnaryExpressionAST(node: Node):
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
        elif child.type in ['builtInCall', 'subroutineCall']:
            # TODO
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

    @staticmethod
    def __buildComparisonExpressionAST(node: Node):
        assert node.type == 'comparisonExpression'
        child = node.getChild()
        if len(node.children) == 1:
            literal = '!!'  # JavaScript-equivalent for truthy value
            expressionNode = child
            expression = Expression.buildExpressionAST(expressionNode)
            return UnaryOperator(literal, expression)
        else:
            leftExpressionNode = child
            literal = node.children[1].getChild().text
            rightExpressionNode = node.children[2]
            leftExpression = Expression.buildExpressionAST(leftExpressionNode)
            rightExpression = Expression.buildExpressionAST(rightExpressionNode)
            return BinaryOperator(literal, leftExpression, rightExpression)

    @staticmethod
    def __buildMembershipTestAST(node: Node):
        assert node.type == 'membershipTest'
        identifierLiteral = node.getChildByType('Identifier').text
        identifier = Variable(identifierLiteral)
        literal = 'in'
        setDeclarationNode = node.getChildByType('setDeclaration')
        setDeclaration = SetDeclaration(setDeclarationNode)
        return BinaryOperator(literal, identifier, setDeclaration)

    def applyBinaryOperator(self, literal: str, secondOperand: 'Expression'):
        self.tree = BinaryOperator(literal, self.tree, secondOperand.tree)

    def clone(self):
        return copy.deepcopy(self)

    def evaluate(self, context):
        expression = self.clone()
        expression.tree = Expression.__evaluate(expression.tree, context, isBoolean=self.isBoolean)
        return expression.tree

    @staticmethod
    def __evaluate(exprNode, context, isBoolean):
        if isinstance(exprNode, UnaryOperator):
            operand = exprNode.arg
            identifier = operand.identifier
            operand = Expression.__evaluate(operand, context, isBoolean)
            if exprNode.literal in ['++', '--']:
                if exprNode.literal == '++':
                    operand += 1
                elif exprNode.literal == '--':
                    operand -= 1
                context.setValue(identifier, operand)
            return exprNode.applyTo(operand)
        elif isinstance(exprNode, BinaryOperator):
            operand1 = Expression.__evaluate(exprNode.arg1, context, isBoolean)
            operand2 = Expression.__evaluate(exprNode.arg2, context, isBoolean)
            return exprNode.applyTo(operand1, operand2)
        elif isinstance(exprNode, Variable):
            identifier = exprNode.identifier
            value = context.getValue(identifier)
            return value
        elif isinstance(exprNode, Value):
            return Expression.__getValueForSymbolicExpression(exprNode, isBoolean)
        else:
            return exprNode

    @staticmethod
    def __getValueForSymbolicExpression(value: Value, isBoolean):
        if value.typeLiteral == 'Integer':
            if isBoolean:
                return bool(value.value)
            else:
                return value.value
        elif value.typeLiteral == 'RealNumber':
            return value.value
        elif value.typeLiteral == 'Constant':
            if value.value in ['pi', 'π']:
                return 3.14159
            elif value.value in ['tau', '𝜏']:
                return 6.28318
            elif value.value in ['euler', 'ℇ']:
                return 2.71828
        elif value.typeLiteral == 'StringLiteral':
            return Value.stringToNumber(value.value)