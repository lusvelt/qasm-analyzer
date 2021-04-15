from Parser import Node

# In this file we declare some classes which map the grammar rules that appear in the parse tree
# Each class is initialized by passing the Node of the parse tree as parameter in the constructor
# The variables having 'Node' as suffix in their name represent nodes in the parse tree

# Represents the 'classicalType' rule
class ClassicalType:
    def __init__(self, node:Node):
        self.node = node
        subTypeNode = node.getChild()
        self.subType = subTypeNode.nodeType
        literalTypeNode = subTypeNode.getChild()
        self.literalType = literalTypeNode.text
        self.designatorExpr1 = None
        self.designatorExpr2 = None
        designatorNode = node.getChild(1)
        if designatorNode is not None:
            if designatorNode.nodeType == 'designator':
                self.designatorExpr1 = designatorNode.getChildByType('expression')
            else:
                self.designatorExpr1 = designatorNode.getChildByType('expression', 0)
                self.designatorExpr2 = designatorNode.getChildByType('expression', 1)

    # Checks if the type has a limited domain (bit and creg have {0, 1}, bool has {true, false})
    def hasLimitedDomain(self):
        return self.literalType in ['bit', 'creg', 'bool']  # Maybe also 'fixed'

# Represents the 'classicalArgument' rule
class ClassicalArgument:
    def __init__(self, node:Node):
        classicalTypeNode = node.getChildByType('classicalType')
        self.classicalType = ClassicalType(classicalTypeNode)
        associationNode = node.getChildByType('association')
        self.identifier = associationNode.getChildByType('Identifier')

    def hasLimitedDomain(self):
        return self.classicalType.hasLimitedDomain()

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
        self.node = node
        self.identifier = node.getChildByType('Identifier').text
        self.classicalArguments = []
        self.quantumArguments = []

        self.__analyzeClassicalArguments()
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
        for node in globalStatements:
            child = node.getChildByType('subroutineDefinition')
            if child is not None:
                identifier = child.getChildByType('Identifier').text
                self.subroutines[identifier] = Subroutine(child)
