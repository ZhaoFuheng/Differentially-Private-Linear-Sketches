import math
import hashlib
import array
import numpy as np


class CountMinSketch():
    def __init__(self, gamma, beta, rho = None):
        # d rows and t columns
        self.t = math.ceil(1.0/gamma)
        self.d = math.ceil(math.log(1.0/beta))
        self.C = []
        self.sigma = None
        self.E = None
        if not rho:
            for _ in range(self.d):
                table = array.array("f", (0.0 for _ in range(self.t)))
                self.C.append(table)
        else:
            self.sigma = math.sqrt(math.log(2.0/beta)/rho)
            self.E = math.sqrt(2.0 * math.log(2.0/beta)/rho) *  math.sqrt(math.log(math.log(2.0/beta)*4.0/gamma)/beta)
            for _ in range(self.d):
                noises = np.random.normal(self.E,self.sigma, self.t)
                table = array.array("f", (noises[index] for index in range(self.t)))
                self.C.append(table)

    def h(self, x):
        md5 = hashlib.md5(str(hash(x)).encode('utf-8'))
        for i in range(self.d):
            md5.update(str(i).encode('utf-8'))
            yield int(md5.hexdigest(), 16) % self.t

    def update(self, x, value=1):
        for table, i in zip(self.C, self.h(x)):
            table[i] += value

    def query(self, x):
        return min(table[i] for table, i in zip(self.C, self.h(x)))
