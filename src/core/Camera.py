import math
from Vector import Vector3
from RayCaster import Ray

class Camera:
	def __init__(self, position, forward, up, d):
		self.near = d
		self.f = forward.getNormalized()
		r = Vector3.cross(up, forward)
		self.r = r.getNormalized()
		self.u = up.getNormalized()

	def screenPointToRayDir(self, point):
		d = self.r*point.x + self.u*point.y - self.f * self.d
		return d.getNormalized()
