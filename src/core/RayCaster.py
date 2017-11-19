from Vector import *

class Ray:
	def __init__(self, origin, direction):
		self.origin = origin
		self.direction = direction

class RayHitPoint:

	def __init__(self):
		self.point = Vector3.zero
		self.normal = Vector3.zero
		
		