from Vector import Vector3
from Color import *
from Tracer import *
from Sampler import *

class Light:
	def __init__(self, shadow):
		self.casts_shadows = shadow

	def get_direction(self, hit):
		pass

	def L(self, hit, scene):
		pass

class PointLight(Light):
	def __init__(self, shadow, position, ls, color):
		Light.__init__(self, shadow)
		self.position = position
		self.ls = ls
		self.color = color

	def get_direction(self, hit):
		return (self.position - hit.point).get_normalized()

	def L(self, hit, scene):
		return self.ls*self.color

	@staticmethod
	def create(params):
		ls = params['ls']
		pos = Vector3(params['position'][0],params['position'][1],params['position'][2])
		col = Color(params['color'][0], params['color'][1], params['color'][2], params['color'][3])
		shadow = False
		if 'shadow' in params:
			shadow = params['shadow'] == 1
		return PointLight(shadow, pos, ls, col)

class DirectionalLight(Light):
	def __init__(self, shadow, direction, ls, color):
		Light.__init__(self, shadow)
		self.direction = direction.get_normalized()
		self.ls = ls
		self.color = color

	def get_direction(self, hit):
		return self.direction

	def in_shadow(self, scene, ray):
		return scene.tracer.shadow_hit(ray, -1, 0.00001)

	def L(self, hit, scene):
		return self.ls*self.color

	@staticmethod
	def create(params):
		ls = params['ls']
		d = Vector3(params['direction'][0],params['direction'][1],params['direction'][2])
		col = Color(params['color'][0], params['color'][1], params['color'][2], params['color'][3])
		shadow = False
		if 'shadow' in params:
			shadow = params['shadow'] == 1
		return DirectionalLight(shadow, d, ls, col)

class Ambient(Light):
	def __init__(self, ls, color):
		Light.__init__(self, False)
		self.ls = ls
		self.color = color

	def get_direction(self, hit):
		return Vector3.zero

	def L(self, hit, scene):
		return self.ls*self.color

	@staticmethod
	def create(params):
		ls = params['ls']
		col = Color(params['color'][0], params['color'][1], params['color'][2], params['color'][3])
		return Ambient(ls, col)

class AmbientOccluder(Light):
	def __init__(self, sampler, ls, color, minAmount):
		Light.__init__(self, False)
		self.sampler = sampler
		self.min_amount = minAmount
		self.ls = ls
		self.color = color
		self.sampler.map_samples_to_hemisphere(1)
		
	def get_direction(self, hit):
		pos = self.sampler.sample_hemisphere()
		return pos.x*self.u + pos.y*self.v+pos.z*self.w

	def in_shadow(self, scene, ray):
		return scene.tracer.shadow_hit(ray, -1, 0.00001)

	def L(self, hit, scene):
		self.w = hit.normal
		self.v = Vector3.cross(self.w, Vector3(0.0072, 1.0, 0.0034))
		self.v.normalize()
		self.u = Vector3.cross(self.v, self.w)

		shadowray = Ray(hit.point, AmbientOccluder.get_direction(self, hit))
		if AmbientOccluder.in_shadow(self, scene, shadowray):
			return self.min_amount*self.ls*self.color
		else:
			return self.ls*self.color

	@staticmethod
	def create(params):
		ls = params['ls']
		col = Color(params['color'][0], params['color'][1], params['color'][2], params['color'][3])
		minam = params['min_amount']
		samplertype = params['sampler']
		samplenum = params['num_samples']
		sampler = eval('%s(%d)'%(samplertype, samplenum))
		print(minam)
		return AmbientOccluder(sampler, ls, col, minam)


def create_light(ltype, params):
	createCmd = '%s.create(%s)'%(ltype,params)
	l = eval(createCmd)
	return l