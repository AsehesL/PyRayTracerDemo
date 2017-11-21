import math
from Vector import Vector3
from Tracer import Ray

class Camera:
	def __init__(self, position, forward, up, d):
		self.near = d
		self.f = forward.getNormalized()
		r = Vector3.cross(up, forward)
		self.r = r.getNormalized()
		u = Vector3.cross(forward, r)
		self.u = u.getNormalized()
		self.position = position

	def screenPointToRay(self, point):
		d = self.r*point.x + self.u*point.y + self.f * self.near
		return Ray(self.position, d.getNormalized())

	@staticmethod
	def create(params):
		pos = Vector3(params['position'][0],params['position'][1],params['position'][2])
		f = Vector3(params['forward'][0],params['forward'][1],params['forward'][2])
		u = Vector3(params['up'][0],params['up'][1],params['up'][2])
		d = params['near']
		return Camera(pos, f, u, d)
