from sympy import *

# The following two classes are operator nodes in the Expression AST
# The operator's arguments can be one of the following types:
#   * UnaryOperator
#   * BinaryOperator
#   * Variable
#   * Value
#   * Symbol

# Represents a unitary operator node in the Expression AST
class UnaryOperator:
    def __init__(self, literal: str, arg):
        self.literal = literal
        self.arg = arg

    def hasLeafArgument(self):
        return not isinstance(self.arg, UnaryOperator) and not isinstance(self.arg, BinaryOperator)

    def applyTo(self, operand):
        if self.literal == '-':
            return -operand
        elif self.literal == '!':
            return Not(operand)
        elif self.literal == '~':
            return (operand)
        else:
            return operand

    def __str__(self):
        return self.literal


# Represents a binary operator in the Expression AST
class BinaryOperator:
    def __init__(self, literal: str, arg1=None, arg2=None):
        self.literal = literal
        self.arg1 = arg1
        self.arg2 = arg2

    def hasLeafAsFirstArgument(self):
        return not isinstance(self.arg1, UnaryOperator) and not isinstance(self.arg1, BinaryOperator)

    def hasLeafAsSecondArgument(self):
        return not isinstance(self.arg2, UnaryOperator) and not isinstance(self.arg2, BinaryOperator)

    def applyTo(self, operand1, operand2):
        if self.literal == '<':
            return Lt(operand1, operand2)
        elif self.literal == '>':
            return Gt(operand1, operand2)
        elif self.literal == '>=':
            return Ge(operand1, operand2)
        elif self.literal == '<=':
            return Le(operand1, operand2)
        elif self.literal == '==':
            return Eq(operand1, operand2)
        elif self.literal == '!=':
            return Ne(operand1, operand2)
        elif self.literal == '&&':
            return And(operand1, operand2)
        elif self.literal == '||':
            return Or(operand1, operand2)
        elif self.literal == '^':
            return Xor(operand1, operand2)
        elif self.literal == '&':
            return And(operand1, operand2)
        elif self.literal == '<<': # TODO LATER: find a good way to encode bitwise operations in sympy
            return Mul(operand1, Pow(2, operand2))
        elif self.literal == '>>':
            return Mul(operand1, Pow(2, -operand2))
        elif self.literal == '+':
            return Add(operand1, operand2)
        elif self.literal == '-':
            return Add(operand1, -operand2)
        elif self.literal == '*':
            return Mul(operand1, operand2)
        elif self.literal == '/':
            return Mul(operand1, Pow(operand2, -1))
        elif self.literal == '%':
            return Mod(operand1, operand2)

    def __str__(self):
        return self.literal

