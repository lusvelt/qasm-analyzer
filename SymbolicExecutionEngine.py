import copy
from sympy import *

from Register import QReg, Qubit, CReg
from Subroutine import Subroutine
from Parser import Node
from Expression import Expression
from Operator import BinaryOperator
from Variable import Variable, ClassicalType
from Solver import Solver


# This class represents the store for the symbolic execution engine
# Values are expressions containing symbols, or strings (for aliases)
class Store:
    def __init__(self, store=None):
        if store is None:
            store = {}
        self.store = store

    def clone(self):
        newStore = {}
        for key in self.store.keys():
            newStore[key] = {}
            if 'value' in self.store[key].keys():
                newValue = copy.deepcopy(self.store[key]['value'])
                newStore[key]['value'] = newValue
            if 'type' in self.store[key].keys():
                newStore[key]['type'] = self.store[key]['type']
        return Store(newStore)

    def set(self, key: str, value=None, type=None):
        if key in self.store.keys():
            if self.store[key]['type'] is not None and type is None:
                type = self.store[key]['type']
        if type.typeLiteral in ['bit', 'creg'] and not isinstance(value, CReg):
            size = Expression(type.designatorExpr1).evaluate(self.store)
            value = CReg.fromSymbolAndSize(key, value, size)
        self.store[key] = {'value': value, 'type': type}

    def get(self, key: str):
        return self.store[key]

    def getValue(self, key: str):
        if 'value' not in self.get(key).keys():
            return None
        return self.get(key)['value']

    def setValue(self, key: str, value):
        if key not in self.store.keys():
            self.store[key] = {'value': value, 'type': None}
        else:
            self.store[key]['value'] = value

    def setType(self, key: str, type):
        if key not in self.store.keys():
            self.store[key] = {'type': type}
        else:
            self.store[key]['type'] = type

    def getType(self, key: str):
        return self.get(key)['type']

    def evaluate(self, indexIdentifierNode):
        child = indexIdentifierNode.getChildByType('indexIdentifier')
        if child is not None:
            sibling = indexIdentifierNode.getChildByType('indexIdentifier', 1)
            evaluatedLeft = self.evaluate(child)
            evaluatedRight = self.evaluate(sibling)
            return CReg.concat(evaluatedLeft, evaluatedRight)
        else:
            identifier = indexIdentifierNode.getChildByType('Identifier').text
            value = self.getValue(identifier)
            if isinstance(value, CReg):
                creg = value
                rangeDefinitionNode = indexIdentifierNode.getChildByType('rangeDefinition')
                expressionListNode = indexIdentifierNode.getChildByType('expressionList')
                if rangeDefinitionNode is not None:
                    rangeDefinition = Range(rangeDefinitionNode)
                    return creg.getRange(rangeDefinition)
                elif expressionListNode is not None:
                    expressionNodes = expressionListNode.getChildrenByType('expression')
                    expressions = [Expression(node).evaluate(self.store) for node in expressionNodes]
                    return creg.getList(expressions)
                else:
                    return creg
            else:
                return value

    def assign(self, indexIdentifierNode, value):
        identifier = indexIdentifierNode.getChildByType('Identifier').text
        oldValue = self.getValue(identifier)
        if isinstance(oldValue, CReg):
            creg = oldValue
            rangeDefinitionNode = indexIdentifierNode.getChildByType('rangeDefinition')
            expressionListNode = indexIdentifierNode.getChildByType('expressionList')
            if rangeDefinitionNode is not None:
                rangeDefinition = Range(rangeDefinitionNode)
                creg.setRange(rangeDefinition, value)
            elif expressionListNode is not None:
                expressionNodes = expressionListNode.getChildrenByType('expression')
                expressions = [Expression(node).evaluate(self.store) for node in expressionNodes]
                creg.setList(expressions, value)
            else:
                self.setValue(identifier, value)
        else:
            self.setValue(identifier, value)

    def evaluateType(self, indexIdentifierNode):
        child = indexIdentifierNode.getChildByType('indexIdentifier')
        if child is not None:
            sibling = indexIdentifierNode.getChildByType('indexIdentifier', 1)
            leftSize = self.evaluateType(child).size
            rightSize = self.evaluateType(sibling).size
            return ClassicalType('creg', leftSize + rightSize)
        else:
            identifier = indexIdentifierNode.getChildByType('Identifier').text
            value = self.getValue(identifier)
            if isinstance(value, CReg):
                creg = value
                rangeDefinitionNode = indexIdentifierNode.getChildByType('rangeDefinition')
                expressionListNode = indexIdentifierNode.getChildByType('expressionList')
                if rangeDefinitionNode is not None:
                    rangeDefinition = Range(rangeDefinitionNode)
                    return ClassicalType('creg', rangeDefinition.getSize())
                elif expressionListNode is not None:
                    expressionNodes = expressionListNode.getChildrenByType('expression')
                    return ClassicalType('creg', len(expressionNodes))
                else:
                    return ClassicalType('creg', creg.size)
            else:
                return self.getType(identifier)


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
        seq = [statement.getChild() for statement in block.getChildrenByType('statement')]
        seq.reverse()
        for statement in seq:
            self.sequence.append(statement)

    def isEmpty(self):
        return len(self.sequence) == 0

    def clone(self):
        return copy.deepcopy(self)


class QRegManager:
    def __init__(self, quantumRegisters=None, potentialEntanglements=None, effectiveQubits=None):
        if potentialEntanglements is None:
            potentialEntanglements = []
        if quantumRegisters is None:
            quantumRegisters = {}
        if effectiveQubits is None:
            effectiveQubits = set()
        self.quantumRegisters = quantumRegisters
        self.potentialEntanglements = potentialEntanglements
        self.effectiveQubits = effectiveQubits

    @staticmethod
    def fromParseTree(parseTree):
        quantumRegisters = {}
        globalStatements = parseTree.getChildrenByType('globalStatement')
        if globalStatements is None:
            return
        for node in globalStatements:
            child = node.getChildByType('quantumDeclarationStatement')
            if child is not None:
                quantumDeclarationNode = child.getChildByType('quantumDeclaration')
                indexIdentifierListNode = quantumDeclarationNode.getChildByType('indexIdentifierList')
                indexIdentifierNodes = indexIdentifierListNode.getChildrenByType('indexIdentifier')
                for indexIdentifierNode in indexIdentifierNodes:
                    identifier = indexIdentifierNode.getChildByType('Identifier').text
                    size = 1
                    expressionListNode = indexIdentifierNode.getChildByType('expressionList')
                    if expressionListNode is not None:
                        expressionNode = expressionListNode.getChildByType('expression', 0)
                        expression = Expression(node=expressionNode)
                        size = expression.evaluate()
                    qreg = QReg(identifier, size)
                    quantumRegisters[identifier] = qreg
        return QRegManager(quantumRegisters)

    def addQReg(self, identifier, size):
        if size is None:
            size = 1
        qreg = QReg(identifier, size)
        self.quantumRegisters[identifier] = qreg

    def markAsMeasured(self, indexIdentifierNode, context):
        child = indexIdentifierNode.getChildByType('indexIdentifier', 0)
        if child is not None:
            sibling = indexIdentifierNode.getChildByType('indexIdentifier', 1)
            self.markAsMeasured(child, context)
            self.markAsMeasured(sibling, context)
        else:
            identifier = indexIdentifierNode.getChildByType('Identifier').text
            qreg = self.quantumRegisters[identifier]
            rangeDefinitionNode = indexIdentifierNode.getChildByType('rangeDefinition')
            if rangeDefinitionNode is not None:
                rangeDefinition = Range(rangeDefinitionNode, context, qreg.size)
                if rangeDefinition.step == 1 and (
                        not isinstance(rangeDefinition.start, int) or not isinstance(rangeDefinition.end, int)):
                    qubitRange = qreg.getRange(rangeDefinition.start, rangeDefinition.end)
                    self.__addToEffectiveQubits(qubitRange)
                else:
                    for i in range(rangeDefinition.start, rangeDefinition.end, rangeDefinition.step):
                        qubit = qreg.getQubit(i)
                        self.__addToEffectiveQubits(qubit)
            else:
                expressionListNode = indexIdentifierNode.getChildByType('expressionList')
                if expressionListNode is not None:
                    expressionNodes = expressionListNode.getChildrenByType('expression')
                    for expressionNode in expressionNodes:
                        expression = Expression(expressionNode).evaluate(context)
                        qubit = qreg.getQubit(expression)
                        self.__addToEffectiveQubits(qubit)
                else:
                    qubits = qreg.getAll()
                    for qubit in qubits:
                        self.__addToEffectiveQubits(qubit)

    def addPotentialEntanglement(self, indexIdentifierNodes, context):
        entanglements = []
        if len(indexIdentifierNodes) > 1:
            for indexIdentifierNode in indexIdentifierNodes:
                identifier = indexIdentifierNode.getChildByType('Identifier').text
                qreg = self.quantumRegisters[identifier]
                rangeDefinitionNode = indexIdentifierNode.getChildByType('rangeDefinition')
                if rangeDefinitionNode is not None:
                    rangeDefinition = Range(rangeDefinitionNode, context, qreg.size)
                    if rangeDefinition.step == 1 and (
                            not isinstance(rangeDefinition.start, int) or not isinstance(rangeDefinition.end, int)):
                        entanglements.append(qreg.getRange(rangeDefinition.start, rangeDefinition.end))
                    else:
                        if len(entanglements) == 0:
                            for i in range(rangeDefinition.start, rangeDefinition.end, rangeDefinition.step):
                                qubit = qreg.getQubit(i)
                                entanglement = set()
                                entanglement.add(qubit)
                                entanglements.append(entanglement)
                        else:
                            j = 0
                            for i in range(rangeDefinition.start, rangeDefinition.end, rangeDefinition.step):
                                entanglements[j].add(qreg.getQubit(i))
                                j += 1
                else:
                    expressionListNode = indexIdentifierNode.getChildByType('expressionList')
                    expressionNodes = expressionListNode.getChildrenByType('expression')
                    if len(entanglements) == 0:
                        for expressionNode in expressionNodes:
                            expression = Expression(expressionNode).evaluate(context)
                            entanglements.append({qreg.getQubit(expression)})
                    else:
                        i = 0
                        for expressionNode in expressionNodes:
                            expression = Expression(expressionNode).evaluate(context)
                            entanglements[i].add(qreg.getQubit(expression))
                            i += 1
        for entanglement in entanglements:
            self.__mergeEntanglement(entanglement)

    def clone(self):
        quantumRegisters = {}
        for key in self.quantumRegisters.keys():
            qreg = self.quantumRegisters[key].clone()
            quantumRegisters[qreg.identifier] = qreg
        potentialEntanglements = copy.deepcopy(self.potentialEntanglements)
        effectiveQubits = copy.deepcopy(self.effectiveQubits)
        return QRegManager(quantumRegisters, potentialEntanglements, effectiveQubits)

    def findEntanglementContainingQubit(self, qubit):
        for entanglement in self.potentialEntanglements:
            for entangledQubit in entanglement:
                if entangledQubit == qubit:
                    return entanglement
        return None

    def checkQubitBound(self, bound):
        if bound is None:
            return True
        return len(self.effectiveQubits) <= bound

    def __addToEffectiveQubits(self, qubit):
        assert isinstance(qubit, Qubit)
        entanglement = self.findEntanglementContainingQubit(qubit)
        if entanglement is None:
            self.effectiveQubits.add(qubit)
        else:
            for qubit in entanglement:
                self.effectiveQubits.add(qubit)
            entanglement.remove(qubit)

    def __mergeEntanglement(self, entanglement):
        oldEntanglements = set()
        newEntanglement = set()
        for qubit in entanglement:
            oldEntanglement = self.findEntanglementContainingQubit(qubit)
            if oldEntanglement is not None:
                self.potentialEntanglements.remove(oldEntanglement)
                oldEntanglements.add(oldEntanglement)
            else:
                newEntanglement.add(qubit)
        for oldEntanglement in oldEntanglements:
            for qubit in oldEntanglement:
                newEntanglement.add(qubit)
        self.potentialEntanglements.append(newEntanglement)


class Range:
    def __init__(self, node, context, size):
        self.node = node
        numColons = len(node.getChildrenByType('COLON'))
        cursor = 1
        self.step = 1
        if node.children[cursor].type == 'expression':
            self.start = Expression(node.children[cursor]).evaluate(context)
            cursor += 1
        else:
            self.start = 0
        cursor += 1
        if node.children[cursor].type == 'expression':
            if numColons > 1:
                self.step = Expression(node.children[cursor]).evaluate(context)
                cursor += 1
            else:
                self.end = Expression(node.children[cursor]).evaluate(context)
        elif node.children[cursor].type == 'COLON':
            self.step = 1
        else:
            self.end = size
        if numColons > 1:
            cursor += 1
            if node.children[cursor].type == 'expression':
                self.end = Expression(node.children[cursor].type).evaluate(context)
            else:
                self.end = size


# This class represents a Symbolic State in the symbolic execution tree
# Each state consists in a triple (node, store, constraints)
# node is the parser Node which represents the current instruction
# store is a dictionary which maps each program variable name into its concrete or symbolic value
# constraints is a BooleanExpression
class SymbolicState:
    def __init__(self, subroutine: Subroutine, node: Node, store: Store, constraints, qregManager):
        self.subroutine = subroutine
        self.node = node
        self.store = store
        self.constraints = constraints
        self.qregManager = qregManager
        self.children = []

    def addChild(self, childState: 'SymbolicState'):
        self.children.append(childState)

    def clone(self, newNode: Node):
        return SymbolicState(self.subroutine, newNode, self.store.clone(), self.constraints, self.qregManager.clone())

    def addConstraint(self, booleanExpression):
        self.constraints = And(self.constraints, booleanExpression)

    def __str__(self):
        return self.store.__str__() + ' | ' + self.constraints.__str__()


class SymbolicExecutionEngine:
    @staticmethod
    def analyzeSubroutine(subroutine: Subroutine):
        # Initialize parameters for the first SymbolicState
        node = subroutine.node
        store = Store()
        constraints = True

        for classicalArgument in subroutine.classicalArguments:
            symbol = Variable.getNewSymbol(classicalArgument.type)
            store.set(classicalArgument.identifier, symbol, classicalArgument.type)

        qregManager = QRegManager.fromParseTree(subroutine.parseTree)
        for quantumArgument in subroutine.quantumArguments:
            size = Expression(quantumArgument.designatorExpr).evaluate()
            qregManager.addQReg(quantumArgument.identifier, size)

        # Instantiate the root state of the symbolic execution tree
        initialState = SymbolicState(subroutine, node, store, constraints, qregManager)

        # Get statement sequence and start simulating the sequential execution
        subroutineBlockNode = subroutine.node.getChildByType('subroutineBlock')
        executionStack = ExecutionStack(subroutineBlockNode)
        SymbolicExecutionEngine.__simulateExecution(initialState, executionStack)

        subroutine.symbolicExecutionTree = initialState

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
                booleanExpression = Expression(booleanExpressionNode, isBoolean=True).evaluate(currentState.store)

                blockIfTrue = statementNode.getChildByType('programBlock', 0)
                stackIfTrue = executionStack.clone()
                stackIfTrue.append(blockIfTrue)
                newStateIfTrue = currentState.clone(statementNode)
                newStateIfTrue.addConstraint(booleanExpression)
                if Solver.isSat(newStateIfTrue.constraints):
                    SymbolicExecutionEngine.__simulateExecution(newStateIfTrue, stackIfTrue)
                    currentState.addChild(newStateIfTrue)

                blockIfFalse = statementNode.getChildByType('programBlock', 1)
                if blockIfFalse is not None:
                    stackIfFalse = executionStack.clone()
                    stackIfFalse.append(blockIfFalse)
                    newStateIfFalse = currentState.clone(statementNode)
                    newStateIfFalse.addConstraint(~booleanExpression)
                    if Solver.isSat(newStateIfFalse.constraints):
                        SymbolicExecutionEngine.__simulateExecution(newStateIfFalse, stackIfFalse)
                        currentState.addChild(newStateIfFalse)
            elif statementNode.type == 'aliasStatement':
                # TODO LATER: implement alias statement execution
                pass
            elif statementNode.type == 'quantumStatement':
                newState = currentState.clone(statementNode)
                SymbolicExecutionEngine.__simulateQuantumStatement(statementNode, newState)
                currentState.addChild(newState)
                SymbolicExecutionEngine.__simulateExecution(newState, executionStack)
            elif statementNode.type == 'loopStatement':
                guardExpressionNode = statementNode.getChildByType('booleanExpression', 0)
                guardExpression = Expression(guardExpressionNode, isBoolean=True).evaluate(currentState.store)
                invariantExpressionNode = statementNode.getChildByType('booleanExpression', 1)
                invariantExpression = None
                if invariantExpressionNode is not None:
                    invariantExpression = Expression(invariantExpressionNode, isBoolean=True).evaluate(currentState.store)
                # TODO: simulate loop
            elif statementNode.type == 'controlDirectiveStatement':
                # TODO LATER: implement control directive statement execution
                pass
        else:
            qubitCheck = currentState.qregManager.checkQubitBound(currentState.subroutine.qubitUpperBound)
            currentState.subroutine.addQubitCheck(qubitCheck)

    @staticmethod
    def __simulateExpressionStatement(statementNode: Node, state: SymbolicState):
        assert statementNode.type == 'expressionStatement'
        expressionNode = statementNode.getChildByType('expression')
        Expression(expressionNode).evaluate(state.store)

    @staticmethod
    def __simulateAssignmentStatement(statementNode, state):
        assert statementNode.type == 'assignmentStatement'
        assignmentNode = statementNode.getChild()
        if assignmentNode.type == 'classicalAssignment':
            indexIdentifierNode = assignmentNode.getChild()

            rightHandSideNode = assignmentNode.getChild(2)
            rightHandSide = None
            if rightHandSideNode.type == 'expression':
                rightHandSide = Expression(rightHandSideNode).evaluate(state.store)
            elif rightHandSideNode.type == 'indexIdentifier':
                rightHandSide = state.store.evaluate(rightHandSideNode)

            assignmentOperatorNode = assignmentNode.getChildByType('assignmentOperator')
            if assignmentOperatorNode.hasChildren():
                assignmentOperator = assignmentOperatorNode.getChild().text
            else:
                assignmentOperator = assignmentOperatorNode.text
            if len(assignmentOperator) > 1:
                leftHandSide = state.store.evaluate(indexIdentifierNode)
                operator = assignmentOperator[0]
                if operator == '<' or operator == '>':
                    operator *= 2
                binaryOperator = BinaryOperator(operator)
                rightHandSide = binaryOperator.applyTo(leftHandSide, rightHandSide)

            state.store.assign(indexIdentifierNode, rightHandSide)
        elif assignmentNode.type == 'quantumMeasurementAssignment':
            indexIdentifierListNode = assignmentNode.getChildByType('indexIdentifierList')
            if indexIdentifierListNode is not None:
                indexIdentifierNodes = indexIdentifierListNode.getChildrenByType('indexIdentifier')
                for indexIdentifierNode in indexIdentifierNodes:
                    type = state.store.evaluateType(indexIdentifierNode)
                    symbol = Variable.getNewSymbol(type)
                    state.store.assign(indexIdentifierNode, symbol)
            quantumMeasurementNode = assignmentNode.getChildByType('quantumMeasurement')
            indexIdentifierListNode = quantumMeasurementNode.getChildByType('indexIdentifierList')
            indexIdentifierNodes = indexIdentifierListNode.getChildrenByType('indexIdentifier')
            for indexIdentifierNode in indexIdentifierNodes:
                state.qregManager.markAsMeasured(indexIdentifierNode, state.store)

    @staticmethod
    def __simulateClassicalDeclarationStatement(statementNode, state: SymbolicState):
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
                        state.store.setType(identifier, type)
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
                        state.store.setType(identifier, type)
                else:
                    equalsExpressionNodes = identifierOrEqualsListNode.getChildrenByType('equalsExpression')
                    for i in range(len(identifierNodes)):
                        identifier = identifierNodes[i].text
                        expression = Expression(equalsExpressionNodes[i].getChildByType('expression')).evaluate(state.store)
                        state.store.set(identifier, expression, type)
        elif declarationNode.type == 'constantDeclaration':
            equalsAssignmentListNode = declarationNode.getChildByType('equalsAssignmentList')
            identifierNodes = equalsAssignmentListNode.getChildrenByType('Identifier')
            equalsExpressionNodes = equalsAssignmentListNode.getChildrenByType('equalsExpression')
            for i in range(len(identifierNodes)):
                identifier = identifierNodes[i].text
                expressionNode = equalsExpressionNodes[i].getChildByType('expression')
                expression = Expression(expressionNode).evaluate(state.store)
                state.store.setValue(identifier, expression)

    @staticmethod
    def __simulateQuantumStatement(statementNode, state: SymbolicState):
        quantumInstructionNode = statementNode.getChildByType('quantumInstruction')
        child = quantumInstructionNode.getChild()
        if child.type == 'quantumGateCall':
            indexIdentifierListNode = child.getChildByType('indexIdentifierList')
            indexIdentifierNodes = indexIdentifierListNode.getChildrenByType('indexIdentifier')
            state.qregManager.addPotentialEntanglement(indexIdentifierNodes, state.store)
        elif child.type == 'quantumMeasurement':
            indexIdentifierListNode = child.getChildByType('indexIdentifierList')
            indexIdentifierNodes = indexIdentifierListNode.getChildrenByType('indexIdentifier')
            for indexIdentifierNode in indexIdentifierNodes:
                state.qregManager.markAsMeasured(indexIdentifierNode, state.store)
