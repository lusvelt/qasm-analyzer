import copy
from sympy import Ne, Or
from Solver import Solver


class CReg:
    def __init__(self, identifier=None, size=1):
        self.identifier = identifier
        self.size = size
        self.content = []

    @staticmethod
    def fromStringLiteral(stringLiteral):
        creg = CReg(size=len(stringLiteral))
        for i in range(len(stringLiteral)):
            value = 0 if stringLiteral[i] == '0' else 1
            bit = Bit(creg, i, value)
            creg.content.append(bit)
        return creg


class BitRange:
    def __init__(self, creg, start, end, symbol=None):
        self.creg = creg
        self.start = start
        self.end = end
        self.symbol = symbol
        self.value = None


class Bit(BitRange):
    def __init__(self, creg, index, value):
        assert value == 0 or value == 1
        super().__init__(creg, index, index)
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

