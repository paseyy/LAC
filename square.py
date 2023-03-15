# coding: utf-8
import os, sys
from z3 import *

# get the playground information
if len(sys.argv) != 2:
    print("Usage: python3 square.py <test-file>")
    sys.exit(0)

with open(sys.argv[1]) as f:
    playground = f.read()
rows = playground.strip().split("\n")
playground = [[None if x == "_" else int(x) for x in r.split()] for r in rows]

# get the playground size
size_y = len(playground)
assert(size_y != 0)
size_x = len(playground[0])
assert(size_x != 0)
assert(size_x == size_y)

#################################### Square ####################################

# create the solver
solver = Solver()

# create an integer variable for each playground cell
# hint: use something like the coordinates as part of the variable name
numbers = [[None for _j in range(size_x)] for _j in range(size_y)]
for i in range(size_y):
    for j in range(size_x):
        numbers[i][j] = Int(f"C_{i}_{j}")
        # solver.add(numbers[i][j] >= 0) ?

# assign each known number the corresponding value from playground
for i in range(size_y):
    for j in range(size_x):
        if playground[i][j]:
            solver.add(numbers[i][j] == playground[i][j])

# declare a variable for the sum of all columns, rows and diagonals
my_sum = Int("sum")

# enforce that each column sums up to the declared variable
for j in range(size_x):
    solver.add(my_sum == Sum([numbers[i][j] for i in range(size_y)]))

# enforce that each row sums up to the declared variable
for i in range(size_y):
    solver.add(my_sum == Sum([numbers[i][j] for j in range(size_x)]))

# enforce that both diagonals sum up to the declared variable
diag1 = [numbers[i][i] for i in range(size_y)]
diag2 = [numbers[i][size_y - i - 1] for i in range(size_y)]

solver.add(my_sum == Sum(diag1))
solver.add(my_sum == Sum(diag2))

# call the solver and check satisfiability
res = solver.check()
if res != sat:
    print("unsat")
    sys.exit(1)

# print the model
m = solver.model()
for i in range(size_y):
    results = []
    for j in range(size_x):
        num = numbers[i][j]
        results.append("_" if num is None else m[num].as_long())
    print(("%4s" * len(results)) % tuple(results))

################################################################################
