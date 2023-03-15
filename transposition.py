# coding: utf-8
from z3 import *

# Create an instance of a z3 solver
solver = Solver()

# Declare needed z3 variables
p, q = Bools("p q")
l, r = Bools("l r")

# Add the needed constraints to check equivalence of the two formulae.
solver.add(l == Implies(p, q))
solver.add(r == Implies(Not(q), Not(p)))

solver.add(l != r)

# Check and print the result.
result = solver.check()
print(result)
if result == sat:
    print("There is a case where the left and right side don't "
          "have the same truth value --> not equivalent")
    print(solver.model())
else:
    print("The statements are equivalent")

