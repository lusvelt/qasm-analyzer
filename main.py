from sympy import symbols
from Variable import ClassicalType
from Solver import Solver
from pysmt.shortcuts import get_model

x, y, z = symbols('x, y, z')
int5 = ClassicalType('int', 5)
symbolTypes = {'x': int5, 'y': int5, 'z': int5}
solver = Solver(symbolTypes)
symbolicExpression = 2*x >= y*z + 42
expression = solver.getSolvableExpression(symbolicExpression)
model = get_model(expression)
pass