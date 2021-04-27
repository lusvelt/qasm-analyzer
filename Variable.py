from sympy import symbols

# Represents a classical type
class ClassicalType:
    def __init__(self,
                 typeLiteral: str = None,
                 designatorExpr1 = None,
                 designatorExpr2 = None,
                 node = None):
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
                    self.designatorExpr1 = designatorNode.getChildByType('expression')
                else:
                    self.designatorExpr1 = designatorNode.getChildByType('expression', 0)
                    self.designatorExpr2 = designatorNode.getChildByType('expression', 1)
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
    def __init__(self, identifier: str, type: ClassicalType = None, typeNode = None):
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
    types = {}

    @staticmethod
    def getNewSymbol(type: ClassicalType):
        index = Symbol.nextIndex
        label = '$' + str(index)
        symbol = symbols(label)
        Symbol.types[label] = type
        Symbol.nextIndex += 1
        return symbol


# This class represents an evaluated value resulting from an expression, or from a literal
class Value:
    def __init__(self, value, type: ClassicalType = None, typeLiteral=None):
        assert type is None or typeLiteral is None
        if type is not None or typeLiteral is not None:
            if typeLiteral == 'Integer' or type.typeLiteral == 'Integer':
                self.value = int(value)
            elif typeLiteral == 'RealNumber' or type.typeLiteral == 'RealNumber':
                self.value = float(value)
            elif typeLiteral == 'StringLiteral' or type.typeLiteral == 'StringLiteral':
                self.value = Value.__stringToNumber(value)
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

    @staticmethod
    def __stringToNumber(stringLiteral):
        num = 0
        for i in range(len(stringLiteral)-1, -1, -1):
            num += pow(2, i)
        return num


    def __str__(self):
        return self.value
