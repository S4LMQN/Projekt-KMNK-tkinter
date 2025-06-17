
y = [1, 2, 3 ,4, 1, 1, 4]
x = [3, 4, 5, 6, 2, 3, 4]

from Matrices import *
from statistics import *

def multiple_regression(*args: list, y_arg: list):
    
    max_len = max(len(argument) for argument in args)
    if any(len(argument) != max_len for argument in args):
        raise IndexError()
    if len(y_arg) != max_len:
        raise IndexError()

    x = Matrix(n_cols=1, n_rows=max_len,values=[1 for _ in range(0,max_len)])
    y = Matrix(n_cols=1,n_rows=max_len,values=y_arg)
    
    for arg in args:
        x.append(values=arg, by_row=False)

    return ((x.transpose() * x).inverse() * x.transpose() * y).values

class Regression:
    def __init__(self,*samples,y):
        self.x = samples
        self.y = y
        self.parameters = multiple_regression(*self.x, y_arg=y)
        self.res = self.residues()

    def residues(self):
        residues = []
        y_hat = []
        for i in range(0, len(self.y)):
            u_hat = self.parameters[0]
            for j in range(1, len(self.parameters)):
                u_hat += self.parameters[j] * self.x[j-1][i]
            residues.append(self.y[i] - (u_hat))
            y_hat.append(u_hat)

        self.y_hat = y_hat
        return residues
    
    def ssr(self):
        return sum(e**2 for e in self.res)
    
    def r_sq(self):
        return variance(self.y_hat)/variance(self.y)
    
    def phi_sq(self):
        return self.ssr()/(variance(self.y)*len(self.y))



from random import uniform
from statistics import variance
c1 = [uniform(-1,1) for _ in range(0,100)]
c2 = [uniform(-1,1) for _ in range(0,100)]
c3 = [uniform(-1,1) for _ in range(0,100)]
pack = [c1,c2,c3]



emp_vals = []
sum = 0
res_sum = 0
'''
for i in range(len(c1)):
    emp_val = p[0] + c1[i]*p[1]
    print(f'{i}: {c1[i]} = {emp_val}')
    res_sum += (c1[i] - emp_val)**2
    emp_vals.append(emp_val)
print(f'Variance of y: {variance(c1)}')
print(f'Variance of y_hat: {variance(emp_vals)}')
print(f'SS of model: {res_sum}')
'''

r = Regression(x, y=y)
print(r.parameters())



