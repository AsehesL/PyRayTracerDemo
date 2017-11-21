from Vector import *
from Tracer import *
from Material import Material
import Res
import math
import os.path

class GeometricObject:
	def __init__(self, shader, point):
		self.point = point
		self.material = Material(shader)

	def hit(self, ray, hit, epsilon):
		pass

class Plane(GeometricObject):
	def __init__(self, shader, point, normal):
		GeometricObject.__init__(self, shader, point)
		self.normal = normal

	def hit(self, ray, hit, epsilon):
		t = Vector3.dot((self.point - ray.origin), self.normal) / (Vector3.dot(ray.direction, self.normal))
		if t > epsilon:
			if t > hit.t:
				return False
			hit.t = t
			hit.normal = self.normal
			hit.point = ray.origin + ray.direction * t
			return True
		else:
			return False

	@staticmethod
	def create(params):
		pos = Vector3(params["point"][0], params["point"][1], params["point"][2])
		n = Vector3(params["normal"][0], params["normal"][1], params["normal"][2])
		s = params["shader"]
		return Plane(s, pos, n)

class Sphere(GeometricObject):
	def __init__(self, shader, point, radius):
		GeometricObject.__init__(self, shader, point)
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

			if t>epsilon and t <= hit.t:
				hit.t = t
				hit.normal = (tocenter+ray.direction*t)/self.radius
				hit.point = ray.origin+ray.direction*t
				return True
			
			t = (-valb+e)/denom
			if t>epsilon and t <= hit.t:
				hit.normal = (tocenter+ray.direction*t)/self.radius
				hit.point = ray.origin+ray.direction*t
				return True
		return False

	@staticmethod
	def create(params):
		pos = Vector3(params["point"][0], params["point"][1], params["point"][2])
		r = params["radius"]
		s = params["shader"]
		return Sphere(s, pos, r)

def createFromSceneFile(gtype, params):
	if 'shader' in params:
		params['shader'] = Res.combineResPath(params['shader'])

	createCmd = '%s.create(%s)'%(gtype,params)
	go = eval(createCmd)
	if 'shader_params' in params:
		for p in params["shader_params"]:
			go.material.setParam(p, params["shader_params"][p])
	return go
