import copy
from Subroutine import Subroutine
from Parser import Node
from Expression import BooleanExpression, Expression
from Variable import Value, Symbol


# This class represents the store for the symbolic execution engine
# Values are expressions containing symbols, or strings (for aliases)
class Store:
    def __init__(self, store=None):
        if store is None:
            store = {}
        self.store = store

    def clone(self):
        return Store(dict(self.store))

    def add(self, key:str, value):
        assert isinstance(value, Expression) or isinstance(value, str)
        self.store[key] = value

    def get(self, key:str):
        return self.store[key]


# This class is used to manage the sequence of instructions
# The main feature is to clone the execution stack and push the if-then-else program block
# when the symbolic execution engine finds a branching instruction
class ExecutionStack:
    def __init__(self, block:Node):
        assert block.type == 'subroutineBlock'
        self.sequence = [statement.getChild() for statement in block.getChildrenByType('statement')]
        self.sequence.reverse()

    def pop(self):
        return self.sequence.pop()

    def append(self, block:Node):
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
    def __init__(self, node:Node, store:Store, constraints:BooleanExpression):
        self.node = node
        self.store = store
        self.constraints = constraints
        self.children = []

    def addChild(self, childState:'SymbolicState'):
        self.children.append(childState)

    def clone(self):
        return copy.deepcopy(self)

    def addConstraint(self, booleanExpression:BooleanExpression):
        pass


class SymbolicExecutionEngine:
    @staticmethod
    def getSubroutineSymbolicExecutionTree(subroutine:Subroutine):
        # Initialize parameters for the first SymbolicState
        node = subroutine.node
        store = Store()
        constraints = BooleanExpression(tree=Value(1))
        for classicalArgument in subroutine.classicalArguments:
            symbol = Symbol(classicalArgument.classicalType)
            expression = Expression(tree=symbol)
            store.add(classicalArgument.identifier, expression)

        # Instantiate the root state of the symbolic execution tree
        initialState = SymbolicState(node, store, constraints)

        # Get statement sequence and start simulating the sequential execution
        subroutineBlockNode = subroutine.node.getChildByType('subroutineBlock')
        executionStack = ExecutionStack(subroutineBlockNode)
        SymbolicExecutionEngine.__simulateExecution(initialState, executionStack)

        return initialState

    @staticmethod
    def __simulateExecution(currentState:SymbolicState, executionStack:ExecutionStack):
        if not executionStack.isEmpty():
            statementNode = executionStack.pop()
            if statementNode.type == 'expressionStatement':
                newState = currentState.clone()
                SymbolicExecutionEngine.__simulateExpressionStatement(statementNode, newState)
                currentState.addChild(newState)
                SymbolicExecutionEngine.__simulateExecution(newState, executionStack)
            elif statementNode.type == 'assignmentStatement':
                newState = currentState.clone()
                SymbolicExecutionEngine.__simulateAssignmentStatement(statementNode, newState)
                currentState.addChild(newState)
                SymbolicExecutionEngine.__simulateExecution(newState, executionStack)
            elif statementNode.type == 'classicalDeclarationStatement':
                newState = currentState.clone()
                SymbolicExecutionEngine.__simulateClassicalDeclarationStatement(statementNode, newState)
                currentState.addChild(newState)
                SymbolicExecutionEngine.__simulateExecution(newState, executionStack)
            elif statementNode.type == 'branchingStatement':
                booleanExpressionNode = statementNode.getChildByType('booleanExpression')
                booleanExpression = BooleanExpression(booleanExpressionNode).evaluate()

                blockIfTrue = statementNode.getChildByType('programBlock', 0)
                stackIfTrue = executionStack.clone()
                stackIfTrue.append(blockIfTrue)
                newStateIfTrue = currentState.clone()
                newStateIfTrue.addConstraint(booleanExpression)
                SymbolicExecutionEngine.__simulateExecution(newStateIfTrue, stackIfTrue)

                blockIfFalse = statementNode.getChildByType('programBlock', 1)
                if blockIfFalse is not None:
                    stackIfFalse = executionStack.clone()
                    stackIfFalse.append(blockIfFalse)
                    newStateIfFalse = currentState.clone()
                    newStateIfFalse.addConstraint(booleanExpression.negate())
                    SymbolicExecutionEngine.__simulateExecution(newStateIfFalse, stackIfFalse)
            elif statementNode.type == 'aliasStatement':
                pass
            elif statementNode.type == 'quantumStatement':
                pass
            elif statementNode.type == 'loopStatement':
                pass
            elif statementNode.type == 'controlDirectiveStatement':
                pass

    @staticmethod
    def __simulateExpressionStatement(statementNode, newState):
        pass

    @staticmethod
    def __simulateAssignmentStatement(statementNode, newState):
        pass

    @classmethod
    def __simulateClassicalDeclarationStatement(cls, statementNode, newState):
        pass







