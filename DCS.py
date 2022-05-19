from CountMedian import CountMedianSketch as CountSketch
import math
import  numpy as  np

class DCS():
	def __init__(self, universe, gamma, rho = None):
		# assume the universe is a power of 2
		#w = 1/gamma sqrt(logU log(logU/gamma)) columns
		#d = log(logU /gamma) rows
		self.totalsize = 0
		self.U = universe
		self.gamma = gamma

		self.columns = math.ceil( (1.0/self.gamma) * math.sqrt(math.log(self.U)*math.log(math.log(self.U)/self.gamma)) )
		self.rows = math.ceil(math.log(math.log(self.U)/self.gamma))


		self.total_levels = math.ceil ( math.log2(universe) )
		self.subdomains = []
		for i in range(self.total_levels):
			if rho:
				self.subdomains.append( CountSketch(1.0/self.columns, 1.0/self.rows, 1.0*rho/self.total_levels) )
			else:
				self.subdomains.append( CountSketch(1.0/self.columns, 1.0/self.rows) )
			self.totalsize += self.rows*self.columns

	def update(self, item, weight = 1):
		for j in range(0, self.total_levels):
			self.subdomains[j].update(item, weight)
			
			item = math.floor(item/2)
	
	def rank(self, x):
		result = 0
		for i in range(self.total_levels):
			if x % 2 == 1:
				result += self.subdomains[i].query(x-1)
			x = math.floor(x/2)
		return result
		
	def query(self, x):
		return self.rank(x)

	def memory_budget(self):
		return self.totalsize
