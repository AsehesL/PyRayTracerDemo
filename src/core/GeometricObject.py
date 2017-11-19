from core.Vector import *
from core.RayCaster import *
import math

class GeometricObject:
	def __init__(self, point):
		self.point = point

	def hit(self, ray, hit, epsilon):
		pass

class Plane(GeometricObject):
	def __init__(self, point, normal):
		GeometricObject.__init__(self, point)
		self.normal = normal

	def hit(self, ray, hit, epsilon):
		t = Vector3.dot((self.point - ray.origin), self.normal) / (Vector3.dot(ray.direction, self.normal))
		if t > epsilon:
			hit.normal = self.normal
			hit.point = ray.origin + ray.direction * t
			return True
		else:
			return False

class Sphere(GeometricObject):
	def __init__(self, point, radius):
		GeometricObject.__init__(self, point)
		self.radius = radius

	def hit(self, ray, hit, epsilon):
		tocenter = ray.origin - self.point
		vala = Vector3.dot(ray.direction, ray.direction)
		valb = Vector3.dot(tocenter, ray.direction) * 2.0
		valc = Vector3.dot(tocenter, tocenter)-self.radius*self.radius
		dis = valb*valb-4.0*vala*valc

		if dis < 0.0:
			return False
		else:
			e = math.sqrt(dis)
			denom = 2.0 * vala
			t = (-valb-e)/denom

			if t>epsilon:
				hit.normal = (tocenter+ray.direction*t)/self.radius
				hit.point = ray.origin+ray.direction*t
				return True
			
			t = (-valb+e)/denom
			if t>epsilon:
				hit.normal = (tocenter+ray.direction*t)/self.radius
				hit.point = ray.origin+ray.direction*t
				return True
		return False