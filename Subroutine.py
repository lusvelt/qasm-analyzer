from Parser import Node
from Variable import ClassicalVariable, QuantumVariable, ClassicalType

# Represents the 'classicalArgument' rule
class ClassicalArgument(ClassicalVariable):
    def __init__(self, node:Node):
        assert node.type == 'classicalArgument'
        identifier = node.getChildByType('association').getChildByType('Identifier').text
        super().__init__(identifier)
        classicalTypeNode = node.getChildByType('classicalType')
        self.classicalType = ClassicalType(classicalTypeNode)
        associationNode = node.getChildByType('association')
        self.identifier = associationNode.getChildByType('Identifier').text

    def hasLimitedDomain(self):
        return self.classicalType.hasLimitedDomain()

# Represents the 'quantumArgument' rule
class QuantumArgument(QuantumVariable):
    def __init__(self, node:Node):
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
    def __init__(self, node:Node):
        assert node.type == 'subroutineDefinition'
        self.node = node
        self.identifier = node.getChildByType('Identifier').text
        self.classicalArguments = []
        self.quantumArguments = []

        self.__analyzeClassicalArguments()
        self.__analyzeQuantumArguments()
        self.__analyzeReturnType()
        self.__analyzeBody()

        self.hasOnlyLimitedArgs = self.__hasOnlyLimitedArgs()
        self.hasInfiniteDomainArgs = not self.hasOnlyLimitedArgs

    def __analyzeClassicalArguments(self):
        classicalArgumentListNode = self.node.getChildByType('classicalArgumentList')
        classicalArgumentNodes = classicalArgumentListNode.getChildrenByType('classicalArgument')
        for classicalArgumentNode in classicalArgumentNodes:
            classicalArgument = ClassicalArgument(classicalArgumentNode)
            self.classicalArguments.append(classicalArgument)

    def __analyzeQuantumArguments(self):
        quantumArgumentListNode = self.node.getChildByType('quantumArgumentList')
        quantumArgumentNodes = quantumArgumentListNode.getChildrenByType('quantumArgument')
        for quantumArgumentNode in quantumArgumentNodes:
            quantumArgument = ClassicalArgument(quantumArgumentNode)
            self.quantumArguments.append(quantumArgument)

    def __analyzeReturnType(self):
        returnSignatureNode = self.node.getChildByType('returnSignature')
        if returnSignatureNode is None:
            return
        returnTypeNode = returnSignatureNode.getChildByType('classicalType')
        self.returnType = ClassicalType(returnTypeNode)

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

# This is a helper class which takes the parse tree as an input and builds
# a dictionary of all subroutines, setting the correct flags for each of them
class SubroutineClassifier:
    def __init__(self, parseTree:Node):
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
                self.subroutines[identifier] = Subroutine(child)
