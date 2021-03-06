from Parser import Node
from Variable import ClassicalVariable, QuantumVariable, ClassicalType
from Expression import Expression


# Represents the 'classicalArgument' rule
class ClassicalArgument(ClassicalVariable):
    def __init__(self, node: Node):
        assert node.type == 'classicalArgument'
        classicalTypeNode = node.getChildByType('classicalType')
        associationNode = node.getChildByType('association')
        identifier = associationNode.getChildByType('Identifier').text
        super().__init__(identifier, typeNode=classicalTypeNode)

    def hasLimitedDomain(self):
        return self.type.hasLimitedDomain()


# Represents the 'quantumArgument' rule
class QuantumArgument(QuantumVariable):
    def __init__(self, node: Node):
        assert node.type == 'quantumArgument'
        identifier = node.getChildByType('association').getChildByType('Identifier').text
        super().__init__(identifier)
        self.quantumType = node.getChildByType('quantumType').text
        designatorNode = node.getChildByType('designator')
        if designatorNode is not None:
            self.designatorExpr = designatorNode.getChildByType('expression')
        associationNode = node.getChildByType('association')
        self.identifier = associationNode.getChildByType('Identifier').text


# This is the class which operates the analysis on the subroutine, after creating the instance, the following
# attributes are available:
#   hasOnlyLimitedArgs
#   hasInfiniteDomainArgs
#   hasBranchingStatements
#   hasLoops
#   hasSubroutineCalls
#   isPlainSequential
#   hasOnlyBranchingStatements
#   isRecursive
class Subroutine:
    def __init__(self, node: Node, parseTree):
        assert node.type == 'subroutineDefinition'
        self.node = node
        self.parseTree = parseTree
        self.identifier = node.getChildByType('Identifier').text
        self.classicalArguments = []
        self.quantumArguments = []

        # To be filled by SymbolicExecutionEngine
        self.symbolicExecutionTree = None
        self.qubitUpperBound = None
        self.qubitChecks = []  # It's the array of qubit upper bound violations

        self.__setQubitUpperBound()
        self.__analyzeClassicalArguments()
        self.__analyzeQuantumArguments()
        self.__analyzeReturnType()
        self.__analyzeBody()

        self.hasOnlyLimitedArgs = self.__hasOnlyLimitedArgs()
        self.hasInfiniteDomainArgs = not self.hasOnlyLimitedArgs

    def __setQubitUpperBound(self):
        expressionNode = self.node.getChildByType('expression')
        if expressionNode is not None:
            self.qubitUpperBound = Expression(expressionNode).evaluate()

    def __analyzeClassicalArguments(self):
        classicalArgumentListNode = self.node.getChildByType('classicalArgumentList')
        if classicalArgumentListNode is not None:
            classicalArgumentNodes = classicalArgumentListNode.getChildrenByType('classicalArgument')
            for classicalArgumentNode in classicalArgumentNodes:
                classicalArgument = ClassicalArgument(classicalArgumentNode)
                self.classicalArguments.append(classicalArgument)

    def __analyzeQuantumArguments(self):
        quantumArgumentListNode = self.node.getChildByType('quantumArgumentList')
        if quantumArgumentListNode is not None:
            quantumArgumentNodes = quantumArgumentListNode.getChildrenByType('quantumArgument')
            for quantumArgumentNode in quantumArgumentNodes:
                quantumArgument = QuantumArgument(quantumArgumentNode)
                self.quantumArguments.append(quantumArgument)

    def __analyzeReturnType(self):
        returnSignatureNode = self.node.getChildByType('returnSignature')
        if returnSignatureNode is None:
            return
        returnTypeNode = returnSignatureNode.getChildByType('classicalType')
        self.returnType = ClassicalType(node=returnTypeNode)

    def __analyzeBody(self):
        self.hasBranchingStatements = len(self.node.getDescendantsByType('branchingStatement')) > 0
        self.hasLoops = len(self.node.getDescendantsByType('loopSignature')) > 0
        subroutineCallNodes = self.node.getDescendantsByType('subroutineCall')
        self.hasSubroutineCalls = len(subroutineCallNodes) > 0
        self.isPlainSequential = not self.hasBranchingStatements and not self.hasLoops and not self.hasSubroutineCalls
        self.hasOnlyBranchingStatements = self.hasBranchingStatements and not self.hasLoops and not self.hasSubroutineCalls
        # Check if recursive
        self.isRecursive = False
        for subroutineCallNode in subroutineCallNodes:
            identifier = subroutineCallNode.getChildByType('Identifier').text
            if self.identifier == identifier:
                self.isRecursive = True
                break

    def __hasOnlyLimitedArgs(self):
        limitedArguments = True
        for argument in self.classicalArguments:
            limitedArguments = limitedArguments and argument.hasLimitedDomain()
        return limitedArguments

    def addQubitCheck(self, qubitCheck):
        if qubitCheck is not None:
            self.qubitChecks.append(qubitCheck)

    def respectsQubitBound(self):
        for check in self.qubitChecks:
            if not isinstance(check, bool) or check is False:
                return False
        return True


# This is a helper class which takes the parse tree as an input and builds
# a dictionary of all subroutines, setting the correct flags for each of them
class SubroutineClassifier:
    def __init__(self, parseTree: Node):
        self.parseTree = parseTree
        self.subroutines = {}
        self.__buildClassification()

    def __buildClassification(self):
        globalStatements = self.parseTree.getChildrenByType('globalStatement')
        if globalStatements is None:
            return
        for node in globalStatements:
            child = node.getChildByType('subroutineDefinition')
            if child is not None:
                identifier = child.getChildByType('Identifier').text
                self.subroutines[identifier] = Subroutine(child, self.parseTree)
