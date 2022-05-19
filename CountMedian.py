import math
import hashlib
import array
import numpy as np
import statistics

class CountMedianSketch():
    def __init__(self, gamma, beta, rho = None):
        # d rows and t columns
        self.t = math.ceil(1.0/gamma)
        self.d = math.ceil(math.log(1.0/beta))
        self.C = []
        self.sigma = None
        if not rho:
            for _ in range(self.d):
                table = array.array("f", (0.0 for _ in range(self.t)))
                self.C.append(table)
        else:
            self.sigma = math.sqrt(math.log(2.0/beta)/rho)
            for _ in range(self.d):
                noises = np.random.normal(0,self.sigma, self.t)
                table = array.array("f", (noises[index] for index in range(self.t)))
                self.C.append(table)

    def h(self, x):
        md5 = hashlib.md5(str(hash(x)).encode('utf-8'))
        for i in range(self.d):
            md5.update(str(i).encode('utf-8'))
            yield int(md5.hexdigest(), 16) % self.t

    def g(self, x):
        sha = hashlib.sha256(str(hash(x)).encode('utf-8'))
        for i in range(self.d):
            sha.update(str(i).encode('utf-8'))
            val = int(sha.hexdigest(), 16) % 2
            if val == 0:
                val = -1
            yield val

    def update(self, x, value=1):
        for table, i, j in zip(self.C, self.h(x), self.g(x)):
            table[i] += j * value

    def query(self, x):
        return statistics.median( j * table[i] for table, i, j in zip(self.C, self.h(x), self.g(x)))