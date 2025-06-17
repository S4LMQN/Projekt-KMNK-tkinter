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



