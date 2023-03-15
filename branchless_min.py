# coding: utf-8
from z3 import *

# Create an instance of a z3 solver
solver = Solver()

min_ite = BitVec("min", 32)
x = BitVec("x", 32)
y = BitVec("y", 32)

# Declare additional z3 variables
tmp = BitVec("tmp", 32)
min_hack = BitVec("min_hack", 32)


solver.add(min_ite == If(x < y, x, y))

# compute the result of slt and store it in a variable
solver.add(tmp == If(x < y, BitVecVal(1, 32), BitVecVal(0, 32)))

# compute min using the formula
solver.add(min_hack == y ^ ((x ^ y) & -tmp))

solver.add(min_ite != min_hack)

# Check and print the result.
result = solver.check()
print(result)
if result == sat:
    print("The bithack method can yield a different result: not equivalent")
    print(solver.model())
else:
    print("The bithack method is equivalent to the standard method")
