import sys

from Vector import *
from GeometricObject import *

class Ray:
	def __init__(self, origin, direction):
		self.origin = origin
		self.direction = direction

	def __str__(self):
		return "Origin:"+str(self.origin)+",Direction:"+str(self.direction)

	def __repr__(self):
		return "Ray(%s,%s)"%(repr(self.origin),repr(self.direction))

class RayTracingHit:
	def __init__(self):
		self.t = sys.float_info.max
		self.point = Vector3.zero
		self.normal = Vector3.zero

	def reset(self):
		self.t = sys.float_info.max

class Tracer:
	def __init__(self):
		pass

	def pushObj(self, obj):
		pass

	def trace(self, ray, hit, scene, epsilon):
		pass


class SimpleTracer(Tracer):
	def __init__(self):
		Tracer.__init__(self)
		self.gemoetries = []

	def pushObj(self, obj):
		self.gemoetries.append(obj)

	def trace(self, ray, hit, scene, epsilon):
		hit.reset()
		result = None
		for g in self.gemoetries:
			if g.hit(ray, hit, epsilon):
				result = g.material.render(hit, scene)
		return result



