import sympy
from pysmt import shortcuts as pysmt
from pysmt.environment import get_env
from Variable import Variable

get_env().enable_infix_notation = True


class Type:
    def __init__(self, literal, size=None):
        self.literal = literal
        self.size = size


class Solver:
    @staticmethod
    def getConvertedExpression(symbolicExpression):
        expression, type = Solver.__getExpressionTree(symbolicExpression)
        return expression, type

    @staticmethod
    def solve(symbolicExpression):
        expression, type = Solver.getConvertedExpression(symbolicExpression)
        return expression.solve()

    @staticmethod
    def isSat(symbolicExpression):
        if isinstance(symbolicExpression, bool):
            return symbolicExpression
        expression, type = Solver.getConvertedExpression(symbolicExpression)
        return pysmt.is_sat(expression)

    @staticmethod
    def isUnsat(symbolicExpression):
        if isinstance(symbolicExpression, bool) or symbolicExpression.is_Boolean:
            return not symbolicExpression
        expression, type = Solver.getConvertedExpression(symbolicExpression)
        return pysmt.is_unsat(expression)

    @staticmethod
    def __getExpressionTree(symbolicExpression):
        # TODO LATER: take into account bitwise shift operations
        args = []
        castType = None
        if len(symbolicExpression.args) > 0:
            for symbolicArg in symbolicExpression.args:
                arg, type = Solver.__getExpressionTree(symbolicArg)
                args.append(arg)
                if castType is None:
                    castType = type
                else:
                    if castType.literal == 'Integer':
                        if type.literal == 'Real':
                            castType = type
                    # TODO LATER: consider other possible castings
            if castType.literal == 'Real':
                for i in range(len(args)):
                    args[i] = pysmt.ToReal(args[i])

        if isinstance(symbolicExpression, sympy.Not):
            if castType.literal == 'Integer':
                return pysmt.Equals(args[0], pysmt.Int(0)), Type('Bool')
            elif castType.literal == 'Real':
                return pysmt.Equals(args[0], pysmt.Real(0)), Type('Bool')
            elif castType.literal == 'Bool':
                return pysmt.Not(args[0]), Type('Bool')
            else: # castType.literal == 'BitVector'
                return pysmt.BVNot(args[0]), Type('BitVector')
        elif isinstance(symbolicExpression, sympy.Lt):
            return pysmt.LT(args[0], args[1]), Type('Bool')
        elif isinstance(symbolicExpression, sympy.Gt):
            return pysmt.GT(args[0], args[1]), Type('Bool')
        elif isinstance(symbolicExpression, sympy.Ge):
            return pysmt.GE(args[0], args[1]), Type('Bool')
        elif isinstance(symbolicExpression, sympy.Le):
            return pysmt.LE(args[0], args[1]), Type('Bool')
        elif isinstance(symbolicExpression, sympy.Eq):
            return pysmt.Equals(args[0], args[1]), Type('Bool')
        elif isinstance(symbolicExpression, sympy.Ne):
            return pysmt.NotEquals(args[0], args[1]), Type('Bool')
        elif isinstance(symbolicExpression, sympy.And):
            if castType.literal == 'Bool':
                return pysmt.And(args[0], args[1]), Type('Bool')
            else: # type.literal == 'BitVector'
                return pysmt.BVAnd(args[0], args[1]), castType
        elif isinstance(symbolicExpression, sympy.Or):
            if castType.literal == 'Bool':
                return pysmt.Or(args[0], args[1]), Type('Bool')
            else:  # type.literal == 'BitVector'
                return pysmt.BVOr(args[0], args[1]), castType
        elif isinstance(symbolicExpression, sympy.Xor):
            return pysmt.BVXor(args[0], args[1]), castType
        elif isinstance(symbolicExpression, sympy.Add):
            return pysmt.Plus(args), castType
        elif isinstance(symbolicExpression, sympy.Mul):
            return pysmt.Times(args), castType
        elif isinstance(symbolicExpression, sympy.Pow):
            return pysmt.Pow(args[0], args[1]), castType
        # TODO LATER: deal with missing modulo operator from pysmt
        else:
            if isinstance(symbolicExpression, sympy.Symbol):
                symbolType = Variable.symbolTypes[symbolicExpression.name]
                literal = symbolType.getTypeForSolver()
                designator = symbolType.designatorExpr1
                type = Type(literal, designator)
                return Solver.__encodeTerminal(symbolicExpression, type), type
            elif isinstance(symbolicExpression, sympy.Integer):
                type = Type('Integer')
                return Solver.__encodeTerminal(symbolicExpression, type), type
            elif isinstance(symbolicExpression, sympy.Rational):
                type = Type('Real')
                return Solver.__encodeTerminal(symbolicExpression, type), type
            elif isinstance(symbolicExpression, sympy.Float):
                type = Type('Real')
                return Solver.__encodeTerminal(symbolicExpression, type), type
            else:
                type = Type('Real')
                return Solver.__encodeTerminal(symbolicExpression, type), type

    @staticmethod
    def __encodeTerminal(symbolicExpression, type):
        if isinstance(symbolicExpression, sympy.Symbol):
            if type.literal == 'Integer':
                return pysmt.Symbol(symbolicExpression.name, pysmt.INT)
            elif type.literal == 'Real':
                return pysmt.Symbol(symbolicExpression.name, pysmt.REAL)
            elif type.literal == 'Bool':
                return pysmt.Symbol(symbolicExpression.name, pysmt.BOOL)
            else:  # type.literal == 'BitVector'
                return pysmt.Symbol(symbolicExpression.name, pysmt.BVType(type.size))
        else:
            if type.literal == 'Integer':
                return pysmt.Int(symbolicExpression.p)
            elif type.literal == 'Real':
                if isinstance(symbolicExpression, sympy.Rational):
                    return pysmt.Real(symbolicExpression.p / symbolicExpression.q)
                else:  # isinstance(symbolicExpression, sympy.Float)
                    return pysmt.Real(symbolicExpression)
            elif type.literal == 'Bool':
                return pysmt.Bool(symbolicExpression)
            else:  # type.literal == 'BitVector'
                return pysmt.BV(symbolicExpression, type.size)
