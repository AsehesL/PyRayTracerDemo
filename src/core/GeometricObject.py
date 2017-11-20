from Vector import *
from Tracer import *
from Renderer import *
import math

class GeometricObject:
	def __init__(self, point):
		self.point = point

	def hit(self, ray, renderer, epsilon):
		pass

class Plane(GeometricObject):
	def __init__(self, point, normal):
		GeometricObject.__init__(self, point)
		self.normal = normal

	def hit(self, ray, renderer, epsilon):
		t = Vector3.dot((self.point - ray.origin), self.normal) / (Vector3.dot(ray.direction, self.normal))
		if t > epsilon:
			if t > renderer.t:
				return False
			renderer.t = t
			renderer.normal = self.normal
			renderer.point = ray.origin + ray.direction * t
			return True
		else:
			return False

	@staticmethod
	def create(params):
		pos = Vector3(params["point"][0], params["point"][1], params["point"][2])
		n = Vector3(params["normal"][0], params["normal"][1], params["normal"][2])
		return Plane(pos, n)

class Sphere(GeometricObject):
	def __init__(self, point, radius):
		GeometricObject.__init__(self, point)
		self.radius = radius

	def hit(self, ray, renderer, epsilon):
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

			if t>epsilon and t <= renderer.t:
				renderer.t = t
				renderer.normal = (tocenter+ray.direction*t)/self.radius
				renderer.point = ray.origin+ray.direction*t
				return True
			
			t = (-valb+e)/denom
			if t>epsilon and t <= renderer.t:
				renderer.normal = (tocenter+ray.direction*t)/self.radius
				renderer.point = ray.origin+ray.direction*t
				return True
		return False

	@staticmethod
	def create(params):
		pos = Vector3(params["point"][0], params["point"][1], params["point"][2])
		r = params["radius"]
		return Sphere(pos, r)

def createFromSceneFile(gtype, params):
	createCmd = '%s.create(%s)'%(gtype,params)
	return eval(createCmd)