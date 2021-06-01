from sympy import symbols


# Represents a classical type
class ClassicalType:
    def __init__(self,
                 typeLiteral: str = None,
                 designatorExpr1=None,
                 designatorExpr2=None,
                 node=None):
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

    def getTypeForSolver(self):
        if self.typeLiteral == 'bool':
            return 'Bool'
        elif self.typeLiteral in ['int', 'uint']:
            return 'Integer'
        elif self.typeLiteral in ['float', 'angle', 'fixed']:
            return 'Real'
        else:  # self.typeLiteral in ['bin', 'creg']
            return 'BitVector'

    def __str__(self):
        s = self.typeLiteral
        if self.designatorExpr1 is not None:
            s += '[' + self.designatorExpr1
            if self.designatorExpr2 is not None:
                s += ', ' + self.designatorExpr2
            s += ']'
        return s


class Variable:
    nextIndex = 0
    symbolTypes = {}

    def __init__(self, identifier: str, type: ClassicalType = None):
        self.identifier = identifier
        self.type = type

    @staticmethod
    def getNewSymbol(type: ClassicalType):
        index = Variable.nextIndex
        Variable.nextIndex += 1
        label = '$' + str(index)
        Variable.symbolTypes[label] = type
        return symbols(label)

    @staticmethod
    def getSymbolType(label):
        return Variable.symbolTypes[label]

    def __str__(self):
        return self.identifier


class ClassicalVariable(Variable):
    def __init__(self, identifier: str, type: ClassicalType = None, typeNode=None):
        assert typeNode is not None or type is None
        if typeNode is not None:
            type = ClassicalType(node=typeNode)
        super().__init__(identifier, type)


class QuantumVariable(Variable):
    pass


# This class represents a value hardcoded in an expression
class Value:
    def __init__(self, value, typeLiteral=None):
        if typeLiteral is not None:
            if typeLiteral == 'Integer':
                self.value = int(value)
            elif typeLiteral == 'RealNumber':
                self.value = float(value)
            elif typeLiteral == 'StringLiteral':
                self.value = value
            else:
                self.value = value

        if typeLiteral is None:
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

    @staticmethod
    def stringToNumber(stringLiteral):
        num = 0
        for i in range(len(stringLiteral) - 1, -1, -1):
            num += pow(2, i)
        return num

    def __str__(self):
        return self.value
