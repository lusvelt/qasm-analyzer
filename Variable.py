from Parser import Node
from Expression import Expression


# Represents a classical type
class ClassicalType:
    def __init__(self,
                 typeLiteral: str = None,
                 designatorExpr1: Expression = None,
                 designatorExpr2: Expression = None,
                 node: Node = None):
        assert typeLiteral is None and node is not None or typeLiteral is not None and node is None
        if node is not None:
            self.node = node
            subTypeNode = node.getChild()
            self.subType = subTypeNode.type
            typeLiteralNode = subTypeNode.getChild()
            self.typeLiteral = typeLiteralNode.text
            self.designatorExpr1 = None
            self.designatorExpr2 = None
            designatorNode = node.getChild(1)
            if designatorNode is not None:
                if designatorNode.type == 'designator':
                    self.designatorExpr1 = Expression(designatorNode.getChildByType('expression')).evaluate()
                else:
                    self.designatorExpr1 = Expression(designatorNode.getChildByType('expression', 0)).evaluate()
                    self.designatorExpr2 = Expression(designatorNode.getChildByType('expression', 1)).evaluate()
        else:
            self.typeLiteral = typeLiteral
            self.designatorExpr1 = designatorExpr1
            self.designatorExpr2 = designatorExpr2

    # Checks if the type has a limited domain (bit and creg have {0, 1}, bool has {true, false})
    def hasLimitedDomain(self):
        return self.typeLiteral in ['bit', 'creg', 'bool']  # Maybe also 'fixed'


class Variable:
    def __init__(self, identifier: str, type: ClassicalType = None):
        self.identifier = identifier
        self.type = type

    def __str__(self):
        return self.identifier


class ClassicalVariable(Variable):
    def __init__(self, identifier: str, type: ClassicalType = None, typeNode: Node = None):
        assert typeNode is not None or type is None
        if typeNode is not None:
            type = ClassicalType(node=typeNode)
        super().__init__(identifier, type)


class QuantumVariable(Variable):
    pass


# This class represents a symbol in the symbolic execution state tree
# Instances of Symbol can appear both in SymbolicStore and in SymbolicConstraints
# Symbols are distinguished by their index, which are automatically incremented when new Symbols are instantiated
class Symbol:
    nextIndex = 0

    def __init__(self, type: ClassicalType):
        self.index = Symbol.nextIndex
        Symbol.nextIndex += 1
        self.type = type

    def __str__(self):
        return '$' + str(self.index)


# This class represents an evaluated value resulting from an expression, or from a literal
class Value:
    def __init__(self, value, type: ClassicalType = None, typeLiteral=None):
        assert type is None or typeLiteral is None
        if type is not None or typeLiteral is not None:
            if typeLiteral == 'Integer' or type.typeLiteral == 'Integer':
                self.value = int(value)
            elif typeLiteral == 'RealNumber' or type.typeLiteral == 'Integer':
                self.value = float(value)
            else:
                self.value = value

        if typeLiteral is None and type is None:
            if isinstance(value, int):
                self.typeLiteral = 'Integer'
            elif isinstance(value, float):
                self.typeLiteral = 'RealNumber'
            elif value in ['pi', 'π', 'tau', '𝜏', 'euler', 'ℇ']:
                self.typeLiteral = 'Constant'
            else:
                self.typeLiteral = 'StringLiteral'
        else:
            self.typeLiteral = typeLiteral
        self.type = type

    def __str__(self):
        return self.value
