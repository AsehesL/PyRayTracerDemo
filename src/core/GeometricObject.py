from Vector import *
from Tracer import *
from Material import Material
from Sampler import *
import Res
import math
import os.path

class GeometricObject:
	def __init__(self, shader, point):
		self.point = point
		self.material = Material(shader)

	def hit(self, ray, hit, epsilon):
		pass

	def sample(self):
		return Vector3.zero

	def set_sampler(self, sampler):
		self.sampler = sampler

	def get_normal(self, point):
		pass

	def pdf(self, hit):
		pass

	def shadowhit(self, ray, shadowhit, epsilon):
		pass

class Plane(GeometricObject):
	def __init__(self, shader, point, normal):
		GeometricObject.__init__(self, shader, point)
		self.normal = normal.get_normalized()

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

	def get_normal(self, point):
		return self.normal

	def shadowhit(self, ray, shadowhit, epsilon):
		t = Vector3.dot((self.point - ray.origin), self.normal) / (Vector3.dot(ray.direction, self.normal))
		if t > epsilon:
			if t > shadowhit.t:
				return False
			shadowhit.t = t
			return True
		else:
			return False

	@staticmethod
	def create(params):
		pos = Vector3(params["point"][0], params["point"][1], params["point"][2])
		n = Vector3(params["normal"][0], params["normal"][1], params["normal"][2])
		s = params["shader"]
		return Plane(s, pos, n)

class Rectangle(Plane):
	def __init__(self, shader, point, normal, right, up):
		Plane.__init__(self, shader, point, normal)
		self.width_squared = right.sqr_magnitude()
		self.height_squared = up.sqr_magnitude()
		self.invArea = 1/(right.magnitude()*up.magnitude())
		self.right = right
		self.up = up

	def hit(self, ray, hit, epsilon):
		t = Vector3.dot((self.point - ray.origin), self.normal) / (Vector3.dot(ray.direction, self.normal))
		if t <= epsilon:
			return False
		if t > hit.t:
			return False
		p = ray.origin + t * ray.direction
		d = p - self.point
		ddw = Vector3.dot(d, self.right)
		if ddw < 0.0 or ddw > self.width_squared:
			return False
		ddh = Vector3.dot(d, self.up)
		if ddh < 0.0 or ddh > self.height_squared:
			return False
		hit.t = t
		hit.normal = self.normal
		hit.point = p
		return True

	def get_normal(self, point):
		return self.normal

	def sample(self):
		sp = self.sampler.sample_unit_square()
		return self.point+(sp.x*2-1)*self.right+(sp.y*2-1)*self.up

	def pdf(self, hit):
		return self.invArea

	def shadowhit(self, ray, shadowhit, epsilon):
		t = Vector3.dot((self.point - ray.origin), self.normal) / (Vector3.dot(ray.direction, self.normal))
		if t <= epsilon:
			return False
		if t > shadowhit.t:
			return False
		p = ray.origin + t * ray.direction
		d = p - self.point
		ddw = Vector3.dot(d, self.right)
		if ddw < 0.0 or ddw > self.width_squared:
			return False
		ddh = Vector3.dot(d, self.up)
		if ddh < 0.0 or ddh > self.height_squared:
			return False
		shadowhit.t = t
		return True

	@staticmethod
	def create(params):
		pos = Vector3(params["point"][0], params["point"][1], params["point"][2])
		n = Vector3(params["normal"][0], params["normal"][1], params["normal"][2])
		r = Vector3(params["right"][0], params["right"][1], params["right"][2])
		u = Vector3(params["up"][0], params["up"][1], params["up"][2])
		s = params["shader"]
		return Rectangle(s, pos, n, r, u)


class Sphere(GeometricObject):
	def __init__(self, shader, point, radius):
		GeometricObject.__init__(self, shader, point)
		self.radius = radius
		self.invArea = 1/(4*math.pi*self.radius*self.radius)

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
				hit.t = t
				hit.normal = (tocenter+ray.direction*t)/self.radius
				hit.point = ray.origin+ray.direction*t
				hit.ray = ray
				return True
		return False

	def set_sampler(self, sampler):
		self.sampler = sampler
		self.sampler.map_samples_to_sphere()

	def get_normal(self, point):
		tocenter = point - self.point
		return tocenter.get_normalized()

	def sample(self):
		sp = self.sampler.sample_sphere()
		return self.point+Vector3(sp.x*self.radius,sp.y*self.radius, sp.z*self.radius)

	def pdf(self, hit):
		return self.invArea

	def shadowhit(self, ray, shadowhit, epsilon):
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

			if t>epsilon and t <= shadowhit.t:
				shadowhit.t = t
				return True
			
			t = (-valb+e)/denom
			if t>epsilon and t <= shadowhit.t:
				shadowhit.t = t
				return True
		return False

	@staticmethod
	def create(params):
		pos = Vector3(params["point"][0], params["point"][1], params["point"][2])
		r = params["radius"]
		s = params["shader"]
		return Sphere(s, pos, r)

def create_from_scene_file(gtype, params):
	if 'use' in params and params['use'] == False:
		return None
	if 'shader' in params:
		params['shader'] = Res.combine_res_path(params['shader'])

	createCmd = '%s.create(%s)'%(gtype,params)
	go = eval(createCmd)
	if 'shader_params' in params:
		for p in params["shader_params"]:
			go.material.set_param(p, params["shader_params"][p])
	return go
