# How to destroy an object?


class Matrix:
    __slots__ = ('__values', '__row_index', '__n_cols', '__n_rows')
    def __init__(self, *, n_cols: int, n_rows: int, values):
        if type(n_cols) != int or type(n_rows) != int:
            raise TypeError('Dimensions have to be represented by integer values!')
        elif type(values) not in (list, tuple):
            raise TypeError('Values have to be in the form of tuple or list!')
        elif n_cols * n_rows != len(values):
            raise IndexError(f'Given number of values is {len(values)}, but according to dimensions it should be {n_cols * n_rows}.')
        else:
            self.__values = list()
            self.__row_index = 0
            self.__n_cols = n_cols
            self.__n_rows = n_rows

            start_index = 0
            end_index = n_cols
            for _ in range(n_rows):
                row = values[start_index:end_index]
                self.__append(values = row)
                start_index += n_cols
                end_index += n_cols

    @property
    def values(self):
        return self.__values
        
    def access_element(self, i: int, j: int):
        if type(i) != int or type(j) != int:
            raise TypeError()
        if i >= self.__n_rows or j >= self.__n_cols:
            raise IndexError()
        
        return self.__values[i * self.__n_cols  + j]
    
    def access_row(self, i: int):
        if type(i) != int:
            raise TypeError()
        if i >= self.__n_rows:
            raise IndexError()
        
        return self.__values[i * self.__n_cols:(i + 1) * self.__n_cols]
    
    def access_column(self, j:int):
        if type(j) != int:
            raise TypeError()
        if j >= self.__n_cols:
            raise IndexError()
        
        column = []
        for index in range(j, self.__n_cols * (self.__n_rows - 1) + j + 1, self.__n_cols):
            column.append(self.__values[index])

        return column 

    def insert(self, values: list, index: int, by_row=True):
        if index < 0:
            raise IndexError()
        if by_row and len(values) != self.__n_cols:
            raise IndexError()
        if not by_row and len(values) != self.__n_rows:
            raise IndexError()
        if any(type(val) not in (int, float) for val in values): 
            raise TypeError()
        if by_row and index > self.__n_rows:
            index = self.__n_rows
        if not by_row and index > self.__n_cols:
            index = self.__n_cols
  
        if by_row:
            self.__n_rows += 1
            self.__values = self.__values[:(index) * self.__n_cols] + list(values) + self.__values[(index) * self.__n_cols:]
        else:
            for i in reversed(range(self.__n_rows)):
                self.__values.insert(i * self.__n_cols + index, values[i])
            self.__n_cols += 1

    def __append(self, *, values, by_row=True):
        lengths = (self.__n_rows, self.__n_cols)
        if not isinstance(values, (list, tuple)):
            raise TypeError()
        if any(not isinstance(val, (int, float)) for val in values):
            raise ValueError()
        if len(values) != lengths[by_row]:
            raise IndexError('Values cannot be appended to matrix because the length of a vec is not equal to length of n_cols or n_rows')
        
        if by_row:
            self.__values += list(values)
            self.__row_index += 1

        else:
            self.insert(values, self.__n_cols, by_row=False)

    def append(self, *, values, by_row=True):
        self.__append(values=values, by_row=by_row)
        if by_row:
            self.__n_rows += 1

    def modify(self, *, value, i: int, j: int):
        if type(value) not in (int, float):
            raise TypeError()
        elif (type(i) != int) or (type(j) != int):
            raise TypeError()
        elif (i >= self.__n_rows) or (j >= self.__n_cols):
            raise IndexError()
        
        self.__values[i * self.__n_cols  + j] = value

    def remove(self, *, number, by_row=True):
        if type(number) != int:
            raise TypeError()
        elif by_row and number >= self.__n_cols:
            raise IndexError()
        elif not by_row and number >= self.__n_rows:
            raise IndexError()
        
        if by_row:
            self.__n_rows -= 1
            self.__values = self.__values[:(number * self.__n_cols)] + self.__values[((number + 1) * self.__n_cols):]
        else:
            
            for i in range (len(self.__values) + number - self.__n_cols, number - 1, -self.__n_cols):
                self.__values.pop(i)
            self.__n_cols -= 1

    def replace(self, *, values, index, by_row=True):
        pass

    def transpose(self):
        v = []
        for i in range(0, self.__n_cols):
            temp = self.access_column(i)
            v += temp
        return Matrix(n_cols=self.__n_rows,n_rows=self.__n_cols,values=v)
    
    def determinant(self):
        if self.__n_cols != self.__n_rows:
            raise IndexError()
        
        if self.__n_cols == 2:
            return self.access_element(0,0) * self.access_element(1,1) - self.access_element(0,1) * self.access_element(1,0)

        a = self.__n_rows
        det = 0
        i = 0
        while i < a:
            temp = i
            diagonal_product = 1
            anti_diagonal_product = 1
            for j in range(0, a):
                diagonal_product *= self.access_element(i % a,j)
                anti_diagonal_product *= self.access_element(i % a,-1-j)
                i += 1
            det += (diagonal_product - anti_diagonal_product)
            i = temp + 1
        return det
    
    def minor(self):
        if self.__n_cols != self.__n_rows:
            raise IndexError()

        if self.__n_cols == 2:
            v = [self.access_element(1,1), -self.access_element(1,0), -self.access_element(0,1), self.access_element(0,0)]
            return Matrix(n_cols=self.__n_cols, n_rows=self.__n_rows, values=v)

        v = []
        for i in range(0, self.__n_rows):
            for j in range(0, self.__n_cols):
                min_m = []
                for a in range(0, self.__n_rows):
                    for b in range(0, self.__n_cols):
                        if a != i and b != j:
                            min_m.append(self.access_element(a,b))
                coefficient = -1 if (i + j) % 2 != 0 else 1
                v.append((Matrix(n_cols=self.__n_cols-1,n_rows=self.__n_rows-1,values=min_m).determinant())*coefficient)
        return Matrix(n_cols=self.__n_cols,n_rows=self.__n_rows,values=v)
    
    def inverse(self):
        return self.minor().transpose() * (1/self.determinant())
        
    def __str__(self):
        matrix_str = f'\n'
        if self.__n_rows == 1 or self.__n_cols == 1:
            return '[' + ' '.join(str(i) for i in self.__values) + ']'
        for i in range(self.__n_rows):
            row_str = ' '. join(str(val) for val in self.access_row(i))
            matrix_str += '[' + row_str + ']'
            matrix_str += '\n'
        return matrix_str
    
    def __repr__(self):
        args = self.__values
        cols, rows = self.__n_cols, self.__n_rows
        return f'{self.__class__.__name__}(n_cols={cols}, n_rows={rows}, values={args})'
    
    def __add__(self, other):
        if type(other) in (float, int):
            args = [val + other for val in self.__values]
        elif type(other) == Matrix:
            if (self.__n_cols != other.__n_cols) or (self.__n_rows != other.__n_rows):
                raise IndexError('Can\'t add matrices which are not of the same dimensions!')
            args = [self.__values[i] + other.__values[i] for i in range(len(self.__values))]
        else:
            raise ValueError('Cannot add objects!')

        return Matrix(n_cols=self.__n_cols, n_rows=self.__n_rows, values=args)
    
    def __sub__(self, other):
        if type(other) in (float, int):
            args = [val - other for val in self.__values]
        elif type(other) == Matrix:
            if (self.__n_cols != other.__n_cols) or (self.__n_rows != other.__n_rows):
                raise IndexError('Can\'t add matrices which are not of the same dimensions!')
            args = [self.__values[i] - other.__values[i] for i in range(len(self.__values))]
        else:
            raise ValueError('Cannot add objects!')

        return Matrix(n_cols=self.__n_cols, n_rows=self.__n_rows, values=args)
    
    def __mul__(self, other):
        other_type = type(other)
        if other_type not in (int, float, Matrix):
            raise TypeError()
        
        if other_type in (int, float):
            return Matrix(n_cols=self.__n_cols,n_rows=self.__n_rows,values=[val * other for val in self.__values])
        else:
            if self.__n_cols != other.__n_rows or self.__n_cols != other.__n_rows:
                raise IndexError()
            
            v = []
            for i in range(0, self.__n_rows):
                for j in range(0, other.__n_cols):
                    a = self.access_row(i)
                    b = other.access_column(j)
                    v.append(sum(a[x] * b[x] for x in range(0,len(a))))
            return Matrix(n_cols=other.__n_cols, n_rows=self.__n_rows,values=v)

