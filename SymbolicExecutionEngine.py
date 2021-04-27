import copy
from Subroutine import Subroutine
from Parser import Node
from Expression import Expression, BinaryOperator
from Variable import Symbol, ClassicalType


# This class represents the store for the symbolic execution engine
# Values are expressions containing symbols, or strings (for aliases)
class Store:
    def __init__(self, store=None):
        if store is None:
            store = {}
        self.store = store

    def clone(self):
        return Store(dict(self.store))

    def set(self, key: str, value=None, type=None):
        if key in self.store.keys():
            if self.store[key]['type'] is not None and type is None:
                type = self.store[key]['type']
        self.store[key] = {'value': value, 'type': type}

    def get(self, key: str):
        return self.store[key]

    def getValue(self, key: str):
        return self.get(key)['value']

    def setValue(self, key: str, value):
        if self.store[key] is None:
            self.store[key] = {'value': value, 'type': None}
        else:
            self.store[key]['value'] = value


# This class is used to manage the sequence of instructions
# The main feature is to clone the execution stack and push the if-then-else program block
# when the symbolic execution engine finds a branching instruction
class ExecutionStack:
    def __init__(self, block: Node):
        assert block.type == 'subroutineBlock'
        self.sequence = [statement.getChild() for statement in block.getChildrenByType('statement')]
        self.sequence.reverse()

    def pop(self):
        return self.sequence.pop()

    def append(self, block: Node):
        assert block.type == 'programBlock'
        sequence = [statement.getChild() for statement in block.getChildrenByType('statement')]
        sequence.reverse()
        for statement in sequence:
            self.sequence.append(statement)

    def isEmpty(self):
        return len(self.sequence) == 0

    def clone(self):
        return copy.deepcopy(self)


# This class represents a Symbolic State in the symbolic execution tree
# Each state consists in a triple (node, store, constraints)
# node is the parser Node which represents the current instruction
# store is a dictionary which maps each program variable name into its concrete or symbolic value
# constraints is a BooleanExpression
class SymbolicState:
    def __init__(self, node: Node, store: Store, constraints):
        self.node = node
        self.store = store
        self.constraints = constraints
        self.children = []

    def addChild(self, childState: 'SymbolicState'):
        self.children.append(childState)

    def clone(self, newNode: Node):
        return SymbolicState(newNode, self.store.clone(), self.constraints)

    def addConstraint(self, booleanExpression):
        self.constraints = self.constraints & booleanExpression

    def __str__(self):
        return self.store.__str__() +  ' | ' + self.constraints.__str__()


class SymbolicExecutionEngine:
    @staticmethod
    def getSubroutineSymbolicExecutionTree(subroutine: Subroutine):
        # Initialize parameters for the first SymbolicState
        node = subroutine.node
        store = Store()
        constraints = True
        for classicalArgument in subroutine.classicalArguments:
            symbol = Symbol.getNewSymbol(classicalArgument.type)
            store.set(classicalArgument.identifier, symbol)

        # Instantiate the root state of the symbolic execution tree
        initialState = SymbolicState(node, store, constraints)

        # Get statement sequence and start simulating the sequential execution
        subroutineBlockNode = subroutine.node.getChildByType('subroutineBlock')
        executionStack = ExecutionStack(subroutineBlockNode)
        SymbolicExecutionEngine.__simulateExecution(initialState, executionStack)

        return initialState

    @staticmethod
    def __simulateExecution(currentState: SymbolicState, executionStack: ExecutionStack):
        if not executionStack.isEmpty():
            statementNode = executionStack.pop()
            if statementNode.type == 'expressionStatement':
                newState = currentState.clone(statementNode)
                SymbolicExecutionEngine.__simulateExpressionStatement(statementNode, newState)
                currentState.addChild(newState)
                SymbolicExecutionEngine.__simulateExecution(newState, executionStack)
            elif statementNode.type == 'assignmentStatement':
                newState = currentState.clone(statementNode)
                SymbolicExecutionEngine.__simulateAssignmentStatement(statementNode, newState)
                currentState.addChild(newState)
                SymbolicExecutionEngine.__simulateExecution(newState, executionStack)
            elif statementNode.type == 'classicalDeclarationStatement':
                newState = currentState.clone(statementNode)
                SymbolicExecutionEngine.__simulateClassicalDeclarationStatement(statementNode, newState)
                currentState.addChild(newState)
                SymbolicExecutionEngine.__simulateExecution(newState, executionStack)
            elif statementNode.type == 'branchingStatement':
                booleanExpressionNode = statementNode.getChildByType('booleanExpression')
                booleanExpression = Expression(booleanExpressionNode).evaluate(currentState.store)

                blockIfTrue = statementNode.getChildByType('programBlock', 0)
                stackIfTrue = executionStack.clone()
                stackIfTrue.append(blockIfTrue)
                newStateIfTrue = currentState.clone(statementNode)
                newStateIfTrue.addConstraint(booleanExpression)
                SymbolicExecutionEngine.__simulateExecution(newStateIfTrue, stackIfTrue)

                blockIfFalse = statementNode.getChildByType('programBlock', 1)
                newStateIfFalse = None
                if blockIfFalse is not None:
                    stackIfFalse = executionStack.clone()
                    stackIfFalse.append(blockIfFalse)
                    newStateIfFalse = currentState.clone(statementNode)
                    newStateIfFalse.addConstraint(~booleanExpression)
                    SymbolicExecutionEngine.__simulateExecution(newStateIfFalse, stackIfFalse)

                currentState.addChild(newStateIfTrue)
                if newStateIfFalse is not None:
                    currentState.addChild(newStateIfFalse)

            elif statementNode.type == 'aliasStatement':
                pass
            elif statementNode.type == 'quantumStatement':
                pass
            elif statementNode.type == 'loopStatement':
                pass
            elif statementNode.type == 'controlDirectiveStatement':
                pass

    @staticmethod
    def __simulateExpressionStatement(expressionNode: Node, state):
        assert expressionNode.type == 'expressionStatement'
        Expression(expressionNode).evaluate(state.store)

    @staticmethod
    def __simulateAssignmentStatement(statementNode, state):
        assert statementNode.type == 'assignmentStatement'
        assignmentNode = statementNode.getChild()
        if assignmentNode.type == 'classicalAssignment':
            indexIdentifierNode = assignmentNode.getChild()
            identifier = indexIdentifierNode.getChildByType('Identifier').text
            assignmentOperatorNode = assignmentNode.getChildByType('assignmentOperator')
            if assignmentOperatorNode.hasChildren():
                assignmentOperator = assignmentOperatorNode.getChild().text
            else:
                assignmentOperator = assignmentOperatorNode.text
            rightHandSideNode = assignmentNode.getChild(2)
            if rightHandSideNode.type == 'expression':
                expression = Expression(rightHandSideNode).evaluate(state.store)
                if len(assignmentOperator) > 1:
                    currentExpression = state.store.getValue(identifier)
                    operator = assignmentOperator[0]
                    if operator == '<' or operator == '>':
                        operator *= 2
                    binaryOperator = BinaryOperator(operator)
                    expression = binaryOperator.applyTo(currentExpression, expression)
                state.store.set(identifier, expression)
            else:
                pass
        else:
            pass

    @staticmethod
    def __simulateClassicalDeclarationStatement(statementNode, state):
        assert statementNode.type == 'classicalDeclarationStatement'
        declarationNode = statementNode.getChild()
        if declarationNode.type == 'classicalDeclaration':
            classicalDeclarationNode = declarationNode.getChild()
            typeLiteral = classicalDeclarationNode.getChild().getChild().text
            if classicalDeclarationNode.type == 'bitDeclaration':
                identifierOrEqualsListNode = classicalDeclarationNode.getChild(1)
                indexIdentifierNodes = identifierOrEqualsListNode.getChildrenByType('indexIdentifier')
                if identifierOrEqualsListNode.type == 'indexIdentifierList':
                    for indexIdentifierNode in indexIdentifierNodes:
                        identifier = indexIdentifierNode.getChildByType('Identifier').text
                        expressionListNode = indexIdentifierNode.getChildByType('expressionList')
                        designatorExpr = None
                        if expressionListNode is not None:
                            designatorExpr = Expression(expressionListNode.getChildByType('expression')).evaluate(state.store)
                        type = ClassicalType(typeLiteral, designatorExpr)
                        state.store.set(identifier, type=type)
                else:
                    equalsExpressionNodes = identifierOrEqualsListNode.getChildrenByType('equalsExpression')
                    for i in range(len(indexIdentifierNodes)):
                        identifier = indexIdentifierNodes[i].getChildByType('Identifier').text
                        equalsExpressionNode = equalsExpressionNodes[i]
                        expression = Expression(equalsExpressionNode.getChildByType('expression')).evaluate(state.store)
                        expressionListNode = indexIdentifierNodes[i].getChildByType('expressionList')
                        designatorExpr = None
                        if expressionListNode is not None:
                            designatorExpr = Expression(expressionListNode.getChildByType('expression')).evaluate(state.store)
                        type = ClassicalType(typeLiteral, designatorExpr)
                        state.store.set(identifier, expression, type)
            else:
                designatorExpr1 = None
                designatorExpr2 = None
                if classicalDeclarationNode.type == 'singleDesignatorDeclaration':
                    designatorNode = classicalDeclarationNode.getChildByType('designator')
                    designatorExpr1 = Expression(designatorNode.getChildByType('expression')).evaluate(state.store)
                elif classicalDeclarationNode.type == 'doubleDesignatorDeclaration':
                    designatorNode = classicalDeclarationNode.getChildByType('doubleDesignator')
                    designatorExpr1 = Expression(designatorNode.getChildByType('expression', 0)).evaluate(state.store)
                    designatorExpr2 = Expression(designatorNode.getChildByType('expression', 1)).evaluate(state.store)
                type = ClassicalType(typeLiteral, designatorExpr1, designatorExpr2)
                identifierOrEqualsListNode = classicalDeclarationNode.getLastChild()
                identifierNodes = identifierOrEqualsListNode.getChildrenByType('Identifier')
                if identifierOrEqualsListNode.type == 'identifierList':
                    for identifierNode in identifierNodes:
                        identifier = identifierNode.text
                        state.store.set(identifier, type=type)
                else:
                    equalsExpressionNodes = identifierOrEqualsListNode.getChildrenByType('equalsExpression')
                    for i in range(len(identifierNodes)):
                        identifier = identifierNodes[i].text
                        expression = Expression(equalsExpressionNodes[i].getChildByType('expression')).evaluate(state.store)
                        state.store.set(identifier, expression, type)
        else:
            equalsAssignmentListNode = declarationNode.getChildByType('equalsAssignmentList')
            identifierNodes = equalsAssignmentListNode.getChildrenByType('Identifier')
            equalsExpressionNodes = equalsAssignmentListNode.getChildrenByType('equalsExpression')
            for i in range(len(identifierNodes)):
                identifier = identifierNodes[i].text
                expressionNode = equalsExpressionNodes[i].getChildByType('expression')
                expression = Expression(expressionNode).evaluate(state.store)
                state.store(identifier, expression)
