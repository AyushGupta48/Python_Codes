import math

class Circle:
	def __init__(self, r):
		self.radius = r 
	
	def circumference(self):
		return 2*self.radius*math.pi

	def area(self):
		return math.pi*(self.radius**2)
	
	
