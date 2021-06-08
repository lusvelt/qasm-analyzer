import copy
from sympy import Ne, Or
from Solver import Solver
from Variable import Variable, ClassicalType


class CReg:
    def __init__(self, identifier=None, size=1, symbol=None):
        self.identifier = identifier
        self.size = size
        self.symbol = symbol
        self.content = []

    @staticmethod
    def fromStringLiteral(stringLiteral):
        creg = CReg(size=len(stringLiteral))
        for i in range(len(stringLiteral)):
            value = 0 if stringLiteral[i] == '0' else 1
            bit = Bit(creg, i, value)
            creg.content.append(bit)
        return creg

    @staticmethod
    def fromSymbolAndSize(identifier, symbol, size):
        creg = CReg(identifier, size, symbol)
        if isinstance(size, int) or size.is_Integer:
            for i in range(size):
                symbol = Variable.getNewSymbol(ClassicalType('int', 1))
                bit = Bit(creg, i, symbol)
                creg.content.append(bit)
        else:
            symbol = Variable.getNewSymbol(ClassicalType('creg', size))
            bitRange = BitRange(creg, 0, size, symbol)
            creg.content.append(bitRange)
        return creg

    @staticmethod
    def concat(lreg, rreg):
        size = lreg.size + rreg.size
        creg = CReg(size=size)
        lcontent = copy.deepcopy(lreg.content)
        rcontent = copy.deepcopy(rreg.content)
        content = [*lcontent, *rcontent]
        creg.content = content
        return creg

    def findBit(self, index):
        for bitRange in self.content:
            if isinstance(bitRange, Bit):
                if Solver.isUnsat(Ne(index, bitRange.start)):
                    return bitRange
        return None

    def getBit(self, index):
        bit = self.findBit(index)
        if bit is None:
            bit = Bit(self, index)
        return bit

    def findRange(self, rangeDefinition):
        for bitRange in self.content:
            if bitRange.start == rangeDefinition.start and bitRange.end == rangeDefinition.end:
                return bitRange
        return None

    def getRange(self, rangeDefinition):
        bitRange = self.findRange(rangeDefinition)
        if bitRange is None:
            bitRange = BitRange(self, rangeDefinition.start, rangeDefinition.end)
        return bitRange

    def getList(self, expressions):
        creg = CReg(size=len(expressions))
        for expression in expressions:
            creg.content.append(self.getBit(expression))
        if creg.size == 1:
            return creg.content[0].value
        else:
            return creg

    def setRange(self, rangeDefinition, value):
        bitRange = self.getRange(rangeDefinition)
        bitRange.value = value

    def setList(self, expressions, value):
        assert isinstance(value, CReg) and len(expressions) == value.size
        for i in range(len(expressions)):
            expression = expressions[i]
            bit = self.getBit(expression)
            bit.value = value.content[i].value

    def getSymbolicExpression(self):
        if isinstance(self.size, int):
            value = 0
            for i in range(self.size):
                bit = self.getBit(i)
                value += bit.value * 2**i
            return value
        else:
            if self.symbol is None:
                self.symbol = Variable.getNewSymbol(ClassicalType('creg', self.size))
            return self.symbol


class BitRange:
    def __init__(self, creg, start, end, symbol=None):
        self.creg = creg
        self.start = start
        self.end = end
        self.symbol = symbol
        self.value = None


class Bit(BitRange):
    def __init__(self, creg, index, value=None):
        super().__init__(creg, index, index+1)
        self.value = value

    def getIndex(self):
        return self.start


class QReg:
    def __init__(self, identifier: str, size):
        self.identifier = identifier
        self.size = size
        self.content = []

    def addItem(self, item):
        self.content.append(item)

    def findQubit(self, index):
        for item in self.content:
            if isinstance(item, Qubit):
                if Solver.isUnsat(Ne(item.start, index)):
                    return item
        return None

    def findRange(self, start, end):
        for item in self.content:
            if isinstance(item, QubitRange) and not isinstance(item, Qubit):
                if Solver.isUnsat(Or(Ne(item.start, start), Ne(item.end, end))):
                    return item
        return None

    def getRange(self, start, end):
        qubitRange = self.findRange(start, end)
        if qubitRange is not None:
            return qubitRange
        else:
            qubitRange = QubitRange(self, start, end)
            self.addItem(qubitRange)
            return qubitRange

    def getQubit(self, index):
        qubit = self.findQubit(index)
        if qubit is not None:
            return qubit
        else:
            qubit = Qubit(self, index)
            self.addItem(qubit)
            return qubit

    def getAll(self):
        qubits = []
        if isinstance(self.size, int):
            for i in range(self.size):
                qubits.append(self.getQubit(i))
        else:
            qubits = self.getRange(0, self.size)
        return qubits

    def clone(self):
        return copy.deepcopy(self)


class QubitRange:
    def __init__(self, qreg, start, end):
        self.qreg = qreg
        self.start = start
        self.end = end

    def __eq__(self, qubitRange):
        return self.qreg.identifier == qubitRange.qreg.identifier and self.start == qubitRange.start and self.end == qubitRange.end

    def __hash__(self):
        return hash(self.qreg.identifier + str(self.start) + str(self.end))

    def __str__(self):
        return self.qreg.identifier + '[' + str(self.start) + ':' + str(self.end) + ']'


class Qubit(QubitRange):
    def __init__(self, qreg, index):
        super().__init__(qreg, index, index)

    def __str__(self):
        return self.qreg.identifier + '[' + str(self.start) + ']'

