from Parser import Node

class Variable:
    def __init__(self, identifier:str):
        self.identifier = identifier

    def __str__(self):
        return self.identifier

class ClassicalVariable(Variable):
    pass

class QuantumVariable(Variable):
    pass

# Represents the 'classicalType' rule
class ClassicalType:
    def __init__(self, node:Node):
        self.node = node
        subTypeNode = node.getChild()
        self.subType = subTypeNode.type
        literalTypeNode = subTypeNode.getChild()
        self.literalType = literalTypeNode.text
        self.designatorExpr1 = None
        self.designatorExpr2 = None
        designatorNode = node.getChild(1)
        if designatorNode is not None:
            if designatorNode.type == 'designator':
                self.designatorExpr1 = designatorNode.getChildByType('expression')
            else:
                self.designatorExpr1 = designatorNode.getChildByType('expression', 0)
                self.designatorExpr2 = designatorNode.getChildByType('expression', 1)

    # Checks if the type has a limited domain (bit and creg have {0, 1}, bool has {true, false})
    def hasLimitedDomain(self):
        return self.literalType in ['bit', 'creg', 'bool']  # Maybe also 'fixed'

# This class represents a symbol in the symbolic execution state tree
# Instances of Symbol can appear both in SymbolicStore and in SymbolicConstraints
# Symbols are distinguished by their index, which are automatically incremented when new Symbols are instantiated
class Symbol:
    nextIndex = 0
    def __init__(self, type):
        self.index = Symbol.nextIndex
        Symbol.nextIndex += 1
        self.type = type

    def __str__(self):
        return '$' + str(self.index)


# This class represents an evaluated value resulting from an expression, or from a literal
class Value:
    def __init__(self, value, type=None):
        if type == 'Integer':
            self.value = int(value)
        elif type == 'RealNumber':
            self.value = float(value)
        else:
            self.value = value

        if type is None:
            if isinstance(value, int):
                self.type = 'Integer'
            elif isinstance(value, float):
                self.type = 'RealNumber'
            elif value in ['pi', 'π', 'tau', '𝜏', 'euler', 'ℇ']:
                self.type = 'Constant'
            else:
                self.type = 'StringLiteral'
        else:
            self.type = type

    def __str__(self):
        return self.value
