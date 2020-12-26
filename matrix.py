import random, json

class Matrix:
    
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.data = []
        self.hash = "%032x" % random.getrandbits(128)
        for x in range(rows):
            newArr = []

            for y in range(cols):
                newArr.append(0)

            self.data.append(newArr)

    #
    #   Static methods
    #

    @staticmethod
    def from_array(input_array):
        return Matrix(len(input_array),1).map(lambda e,i,j: input_array[i])

    @staticmethod
    def subtract(a,b):
        
        if a.rows != b.rows or a.cols != b.cols:
            raise Exception('The amount of rows and columns of the matrices must be the same.')
            return
        
        return Matrix(a.rows, a.cols).map(lambda _,i,j : a.data[i][j] - b.data[i][j])

    @staticmethod
    def transpose(matrix):
        return Matrix(matrix.cols, matrix.rows).map(lambda _,i,j : matrix.data[j][i])


    @staticmethod
    def multiply(a,b):
        def _mult(e,i,j):
            sum = 0
            for k in range(a.cols):
                sum += a.data[i][k] * b.data[k][j]
            return sum
        
        if a.cols != b.rows:
            raise Exception('Columns of matrix <A> must match Rows of matrix <B>')
        
        return Matrix(a.rows,b.cols).map(_mult)

    @staticmethod
    def map(matrix, func):
        return Matrix(matrix.rows,matrix.cols).map(lambda e,i,j : func(matrix.data[i][j], i, j))

    @staticmethod
    def deserialize(data):
        if type(data) is not Matrix and type(data) is not str:
            if type(data) != dict or not 'cols' in data or not 'rows' in data or not 'data' in data:
                raise Exception('Can only deserialize json-strings and objects with the required parameteres <rows:number, cols:number, data:number[]>')
        jData = data
        if type(data) is str:
            jData = json.loads(data)
            if not 'cols' in jData or not 'rows' in jData or not 'data' in jData:
                raise Exception('Can only deserialize json-strings and objects with the required parameteres <rows:number, cols:number, data:number[]>')
        matrix = Matrix(jData['rows'], jData['cols'])
        matrix.data = jData['data']
        return matrix

    #
    #   Public methods
    #

    def copy(self):
        m = Matrix(self.rows, self.cols)
        for x in range(len(self.data)):
            row = self.data[x]
            for y in range(len(row)):
                col = row[y]
                m.data[x][y] = col

        return m
    
    def map(self,func):
        for x in range(self.rows):
            for y in range(self.cols):
                val = self.data[x][y]
                self.data[x][y] = func(val,x,y)
        return self


    def to_array(self):
        arr = []
        for row in self.data:
            for col in row:
                arr.append(col)
        return arr

    def randomize(self):
        return self.map(lambda e,i,j : random.random() * 2 - 1)

    
    def add(self, number_or_matrix):
        if type(number_or_matrix) is Matrix:
            if self.rows != number_or_matrix.rows or self.cols != number_or_matrix.cols:
                raise Exception('The amount of rows and columns of the matrices must be the same.')
            return self.map(lambda e, i, j : e + number_or_matrix.data[i][j])
        elif type(number_or_matrix) is int or type(number_or_matrix) is float:
            return self.map(lambda e,i,j : e + number_or_matrix)

    def multiply(self, number_or_matrix):
        if type(number_or_matrix) is Matrix:
            if self.rows != number_or_matrix.rows or self.cols != number_or_matrix.cols:
                raise Exception('The amount of rows and columns of the matrices must be the same.')
            return self.map(lambda e,i,j : e * number_or_matrix.data[i][j])
        elif type(number_or_matrix) is int or type(number_or_matrix) is float:
            return self.map(lambda e, i, j: e * number_or_matrix)

    def print(self):
        print(f'UUID: {self.hash}')
        print(f'Columns: {self.cols}   Rows: {self.rows}')
        for col in self.data:
            oStr = '    '
            for row in col:
                oStr += f'{row},'
            print(oStr)
        return self
    
    def serialize(self):
        oObj = {
            'cols':self.cols,
            'rows':self.rows,
            'data':self.data
        }

        return json.dumps(oObj)