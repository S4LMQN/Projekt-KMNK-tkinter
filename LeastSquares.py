from Matrices import *
from statistics import *
from copy import deepcopy

def multiple_regression(*, y: list, x_args: list):
    
    #Sprawdza czy wszystkie argumenty mają tą samą długość
    max_len = max(len(argument) for argument in x_args)
    if any(len(argument) != max_len for argument in x_args):
        raise IndexError("Wszystkie zmienne niezalezne musza miec ta sama dlugosc")
    if len(y) != max_len:
        raise IndexError("Zmienna zalezna musi miec taka sama dlugosc jak zmienne niezalezne")

    x = Matrix(n_cols=1, n_rows=max_len,values=[1] * max_len)
    y = Matrix(n_cols=1,n_rows=max_len,values=y)

    for arg in x_args:
        x.append(values=arg, by_row=False)
    
    xtx = x.transpose() * x
    xtx_inv_xt = xtx.inverse() * x.transpose() 
    beta_hat = xtx_inv_xt * y
    return beta_hat.values

"""Tworzy macierz kowariancji"""
def calculate_covariance_matrix(m: Matrix):
    return (m.transpose() * m).inverse()

"""Przyjmuje słownik prób, nazwę y będącą napisem, listę nazw zmiennych x."""
class Regression:
    def __init__(self,*,samples: dict, y_label: str, x_labels: list):
        self.y_label = y_label
        samples_cp = deepcopy(samples)
        #Wybiera zmienną objaśnianą do modelu
        try:
            self.y = samples_cp.pop(y_label)
        except KeyError as e:
            raise KeyError('Nie znaleziono zmiennej objaśnianej dla modelu')
        #Jeśli zmienne są zawarte w liście x_labels, uwzględnia je w modelu
        self.x_labels = [key for key in samples_cp.keys() if key in x_labels]
        self.x = list(samples_cp[key] for key in self.x_labels)
        try:
            self.beta_hat = multiple_regression(y=self.y,x_args=self.x)
        except Exception as e:
            raise Exception("dla podanych wartości niemoliwe jest stworzenie modelu regresji", str(e))
        
        self.n = len(self.y)
        self.k = len(self.x)

        #Tworzenie i zapisanie macierzy kowariancji potrzebnej do obliczenia błędów estymatorów
        c = Matrix(n_cols=1, n_rows=self.n,values=[1] * self.n)
        for arg in self.x:
            c.append(values=arg, by_row=False)

        self.covariance_matrix = calculate_covariance_matrix(c)
        self.residuals = self.calcuate_residuals()

    """Oblicza reszty modelu"""
    def calcuate_residuals(self):
        reisduals = []
        y_hat = []
        for i in range(0, len(self.y)):
            u_hat = self.beta_hat[0]
            for j in range(1, len(self.beta_hat)):
                u_hat += self.beta_hat[j] * self.x[j-1][i]
            reisduals.append(self.y[i] - (u_hat))
            y_hat.append(u_hat)

        self.y_hat = y_hat
        return reisduals
    
    def estimate(sef, *x_args):
        pass
    
    """Oblicza zmienność niewyjaśnioną"""
    def sse(self):
        return sum(e**2 for e in self.residuals)
    
    """Oblicza zmiennosć wyjaśnioną"""
    def ssr(self):
        y_bar = mean(self.y)
        return sum((y_hat_i - y_bar)**2 for y_hat_i in self.y_hat)
    
    """Oblicza całkowitą zmienność"""
    def sst(self):
        y_bar = mean(self.y)
        return sum((y_i - y_bar)**2 for y_i in self.y)
    
    """Oblicza współczynnik determinacji"""
    def r_sq(self):
        y_var = variance(self.y)
        if y_var == 0:
            raise ValueError
        
        return 1 - self.sse()/self.sst() 
    
    """Oblicza błąd kwadratowy reszt"""
    def calculate_squared_residual_error(self):
        return self.sse()/(self.n - self.k - 1)
    
    """Oblicza błąd standardowy parametru strukturalnego"""
    def beta_error(self, beta_index: int):
        return (self.covariance_matrix.access_element(beta_index,beta_index) * self.calculate_squared_residual_error())**0.5
    
    """Test t istotności parametrów strukturalnych dla poziomu ufności 95%"""
    def t_test(self, beta_index: int):
        if beta_index > self.k:
            raise IndexError("Indeks przekroczył długość listy parametrów strukturalnych")

        beta_hat = self.beta_hat[beta_index]

        t = beta_hat / self.beta_error(beta_index)
        return {'t': t, 'significant': abs(t) > student_critical_values(self.n - self.k - 1)}
    
    """Oblicza przedział ufności parametrów strukturalnych dla poziomu ufności 95%"""
    def calculate_confidence_interval(self, beta_index: int):
        if beta_index > self.k:
            raise IndexError("Indeks przekroczył długość listy parametrów strukturalnych")
        
        beta_error = self.beta_error(beta_index)
        beta_hat = self.beta_hat[beta_index]
        t_critical = student_critical_values(self.n - self.k - 1)

        return (beta_hat - beta_error * t_critical, beta_hat + beta_error * t_critical)
    
    '''Test F sprawdzający istotność regresji'''
    def f_test(self):
        r_sq = self.r_sq()    

        m_1 = self.k
        m_2 = self.n - self.k - 1

        return (r_sq * m_2)/((1-r_sq) * m_1)
    
    def __str__(self):
        string = f'Regresja metodą klasycznych kwadratów dla zmiennej {self.y_label}. n={self.n}, k={self.k}\n\n'
        string += '                parametr'+'      błąd st.'+'  dolny przed.'+'  górny przed.'+'        test-t\n'
        string += '------------------------'+'--------------'+'--------------'+'--------------'+'--------------\n'
        #disp len 24,14,14,14,14 = 28
        i = 0
        for index in range(self.k + 1):
            if i == 0:
                string += f'{"stala": <12}'
            else:
                string += f'{f"{self.x_labels[index-1]}": <12}'
            i += 1
            string += f'{f"{round(self.beta_hat[index],4)}": >12}'
            string += f'{f"{round(self.beta_error(index),4)}": >14}'
            interval = self.calculate_confidence_interval(index)
            string += f'{f"{round(interval[0],4)}": >14}'
            string += f'{f"{round(interval[1],4)}": >14}'
            t_test = self.t_test(index)
            string += f'{f"{round(t_test['t'],4)}": >14}'
            asterisks = '***' if t_test["significant"] == True else ''
            string += f'{f"{asterisks}": >9}\n'
        string += (' ' * 46) + '\n'
        string += f'{f"y_bar": <15}' + f'{f"{round(mean(self.y),4)}": >24}' + '  ' + f'{f"SSR": <15}' f'{f"{round(self.ssr(),4)}": >24}\n'
        string += f'{f"SSE": <15}' + f'{f"{round(self.sse(),4)}": >24}' + '  ' + f'{f"SST": <15}' f'{f"{round(self.sst(),4)}": >24}\n'
        string += f'{f"R-kwadrat": <15}' + f'{f"{round(self.r_sq(),4)}": >24}' + '  '+ f'{f"MSE": <15}' f'{f"{round(self.calculate_squared_residual_error()**0.5,4)}": >24}\n'
        string += f'{f"t(0.05,{self.n-self.k-1})": <15}' + f'{f"{round(student_critical_values(self.n-self.k-1),4)}": >24}' + '  '+ f'{f"Test-F": <15}' f'{f"{round(self.f_test(),4)}": >24}\n'
        return string

"""Zwraca wartość krytczną dystrybuanty rozkładu t-studenta dla poziomu ufności 95%"""
def student_critical_values(df: int):
    if type(df) not in (int, float):
        raise TypeError("Wartość stopni swobody musi być typem liczbowym, całkowitym")
    if df % 1 != 0:
        raise ValueError("Wartość stopni swobody musi być liczbą całkowitą")
    
    critical_values = [
    12.7062, 4.3027, 3.1824, 2.7764, 2.5706, 2.4469, 2.3646, 2.3060, 2.2622, 2.2281,
    2.2010, 2.1788, 2.1604, 2.1448, 2.1314, 2.1199, 2.1098, 2.1009, 2.0930, 2.0860,
    2.0796, 2.0739, 2.0687, 2.0639, 2.0595, 2.0555, 2.0518, 2.0484, 2.0452, 2.0423,
    2.0395, 2.0369, 2.0345, 2.0322, 2.0301, 2.0281, 2.0262, 2.0244, 2.0227, 2.0211,
    2.0195, 2.0181, 2.0167, 2.0154, 2.0141, 2.0129, 2.0117, 2.0106, 2.0096, 2.0086,
    2.0076, 2.0066, 2.0057, 2.0049, 2.0040, 2.0032, 2.0025, 2.0017, 2.0010, 2.0003,
    1.9996, 1.9990, 1.9983, 1.9977, 1.9971, 1.9966, 1.9960, 1.9955, 1.9950, 1.9944,
    1.9939, 1.9934, 1.9930, 1.9925, 1.9921, 1.9917, 1.9913, 1.9909, 1.9905, 1.9901,
    1.9897, 1.9893, 1.9890, 1.9886, 1.9883, 1.9879, 1.9876, 1.9873, 1.9870, 1.9867,
    1.9864, 1.9861, 1.9858, 1.9855, 1.9852, 1.9850, 1.9847, 1.9845, 1.9842, 1.9840,
    1.9837, 1.9835, 1.9833, 1.9830, 1.9828, 1.9826, 1.9824, 1.9822, 1.9819, 1.9817,
    1.9815, 1.9813, 1.9811, 1.9809, 1.9808, 1.9806, 1.9804, 1.9802, 1.9800, 1.9799,
    1.9797, 1.9795, 1.9793, 1.9719, 1.9647, 1.9600
    ]

    if df <= 0:
        raise Exception('Wartość stopni swobody musi być dodatnia')
    elif df <= 120:
        df = df
    elif 200 > df > 120:
        df = 121
    elif 500 > df >= 200:
        df = 122
    elif 1000 > df >= 500:
        df = 123
    elif 2000 > df >= 1000:
        df = 124
    else:
        df = 125
    
    return critical_values[int(df - 1)]
