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
		self.point = Vector3.zero
		self.normal = Vector3.zero
		self.material = None
		self.t = sys.float_info.max

	def reset(self):
		self.t = sys.float_info.max

class Tracer:
	def __init__(self, tracingTimes):
		self.tracingTimes = tracingTimes

	def push_obj(self, obj):
		pass

	def trace(self, ray, scene, epsilon):
		pass


class SimpleTracer(Tracer):
	def __init__(self, tracingTimes):
		Tracer.__init__(self, tracingTimes)
		self.gemoetries = []

	def push_obj(self, obj):
		self.gemoetries.append(obj)

	def trace(self, ray, scene, epsilon):
		return SimpleTracer.__trace_recursion(self, ray, scene, epsilon, 0)
		# hit.reset()
		# result = None
		# for g in self.gemoetries:
		# 	if g.hit(ray, hit, epsilon):
		# 		result = g.material.shade(hit, scene)
		# return result

	def __trace_recursion(self, ray, scene, epsilon, n):
		hit = RayTracingHit()
		if SimpleTracer.__trace(self, ray, hit, epsilon):
			if n == self.tracingTimes and hit.material != None:
				return hit.material.shade(hit, scene, None)
			elif hit.material != None:
				reflDir = Vector3.reflect(ray.direction, hit.normal).get_normalized()
				newRay = Ray(hit.point, reflDir)
				reflCol = SimpleTracer.__trace_recursion(self, newRay, scene, epsilon, n+1)
				return hit.material.shade(hit, scene, reflCol)
		return None

	def __trace(self, ray, hit, epsilon):
		hit.reset()
		result = False
		for g in self.gemoetries:
			if g.hit(ray, hit, epsilon):
				hit.material = g.material
				result = True
		return result


def create_tracer(params):
	return SimpleTracer(params["max_trace"])


