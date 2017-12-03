import sys

from Vector import *
from GeometricObject import *
from Color import *

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
		self.ray = None
		self.material = None
		self.depth = 0
		self.t = sys.float_info.max

	def reset(self):
		self.t = sys.float_info.max

class ShadowHit:
	def __init__(self):
		self.t = sys.float_info.max

	def reset(self):
		self.t = sys.float_info.max

class Tracer:
	def __init__(self, tracingTimes):
		self.tracing_times = tracingTimes

	def push_obj(self, obj):
		pass

	def trace(self, ray, scene, epsilon, depth = 0):
		pass

	def shadow_hit(self, ray, shadowhit):
		pass


class SimpleTracer(Tracer):
	def __init__(self, tracingTimes):
		Tracer.__init__(self, tracingTimes)
		self.gemoetries = []

	def push_obj(self, obj):
		self.gemoetries.append(obj)

	def trace(self, ray, scene, epsilon, depth = 0):
		if depth > self.tracing_times:
			return Color.black
		hit = RayTracingHit()
		hit.ray = ray
		hit.depth = depth
		if SimpleTracer.__trace(self, ray, hit, epsilon):
			return hit.material.shade(hit, scene)
		if scene.sky != None:
			return scene.sky.shade(hit, scene)
		return Color.black

		#return SimpleTracer.__trace_recursion(self, ray, scene, epsilon, 0)
	
	def shadow_hit(self, ray, epsilon, shadowFilter = None):
		shadowhit = ShadowHit()
		return SimpleTracer.__shadow_trace(self, ray, shadowhit, epsilon, shadowFilter)

	# def __trace_recursion(self, ray, scene, epsilon, n):
	# 	hit = RayTracingHit()
	# 	hit.ray = ray
	# 	if SimpleTracer.__trace(self, ray, hit, epsilon):
	# 		if n == self.tracingTimes and hit.material != None:
	# 			return hit.material.shade(hit, scene, None)
	# 		elif hit.material != None:
	# 			reflDir = Vector3.reflect(ray.direction, hit.normal).get_normalized()
	# 			newRay = Ray(hit.point, reflDir)
	# 			reflCol = SimpleTracer.__trace_recursion(self, newRay, scene, epsilon, n+1)
	# 			return hit.material.shade(hit, scene, reflCol)
	# 	return None

	def __trace(self, ray, hit, epsilon):
		hit.reset()
		result = False
		for g in self.gemoetries:
			if g.hit(ray, hit, epsilon):
				hit.material = g.material
				result = True
		return result

	def __shadow_trace(self, ray, shadowhit, epsilon, shadowFilter):
		shadowhit.reset()
		for g in self.gemoetries:
			if g.shadowhit(ray, shadowhit, epsilon):
				if shadowFilter != None:
					if shadowFilter(shadowhit.t):
						return True
				else:
					return True
		return False


def create_tracer(params):
	return SimpleTracer(params["max_trace"])


