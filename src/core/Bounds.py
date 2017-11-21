from Vector import *

class Bounds:
	def __init__(self, center, size):
		self.center = center
		self.size = size
		maxX = max(center.x+size.x/2, center.x-size.x/2)
		maxY = max(center.y+size.y/2, center.y-size.y/2)
		maxZ = max(center.z+size.z/2, center.z-size.z/2)
		minX = min(center.x+size.x/2, center.x-size.x/2)
		minY = min(center.y+size.y/2, center.y-size.y/2)
		minZ = min(center.z+size.z/2, center.z-size.z/2)
		self.max = Vector3(maxX,maxY,maxZ)
		self.min = Vector3(minX,minY,minZ)