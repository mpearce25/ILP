import pulp
import itertools

# Represents the 15 equations that need to be solved
A_b10 = [
    [0, 1, 2],
    [3, 4, 5, 6],
    [7, 8, 9, 10, 11],
    [12, 13, 14, 15],
    [16, 17, 18],

    [0, 3, 7], 
    [1, 4, 8, 12], 
    [2, 5, 9, 13, 16],
    [6, 10, 14, 17],
    [11, 15, 18],

    [7, 12, 16],
    [3, 8, 13, 17],
    [0, 4, 9, 14, 18],
    [1, 5, 10, 15], 
    [2, 6, 11]
]

# Converting to binary matrix
# With bin mat only the piecies in a relavant position can have a value that 
# contributes to the 38 total
A_b2 = []
for l in A_b10:
    A_b2.append([1 if x in l else 0 for x in range(19)])

b = [38] * 15
mod = pulp.LpProblem('38 puzzle')
vars = pulp.LpVariable.dicts('x', range(len(A_b2[0])), lowBound=1, upBound=19, cat='Integer')

for row, rhs in zip(A_b2, b):
    mod += sum([row[i]*vars[i] for i in range(len(row))]) == rhs

vl = list(vars.values())
for i in list(itertools.combinations(vl, 2)):
    c = pulp.LpVariable('c' + str(i), lowBound=0, upBound=1, cat='Integer')
    mod += i[0] >= i[1] + (1 - c) - (1000*c)
    mod += i[1] >= i[0]  + c - (1000 * (1 - c))

print('solving')
mod.solve()
print(pulp.LpStatus[mod.status])

# Displaying solution
sol = [str(vars[i].value()) for i in range(len(A_b2[0]))]
ss = '    '
print(' ' * 14 + ss.join(sol[0:3]))
print(' ' * 11 + ss.join(sol[3:7]))
print(' ' * 8 + ss.join(sol[7:12]))
print(' ' * 11 + ss.join(sol[12:16]))
print(' ' * 14 + ss.join(sol[16:19]))
