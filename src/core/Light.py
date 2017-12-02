from Vector import Vector3
from Color import *
from Tracer import *
from Sampler import *
from GeometricObject import *
from Material import *
import Res

class Light:
	def __init__(self, shadow):
		self.casts_shadows = shadow

	def get_direction(self, hit):
		pass

	def L(self, hit, scene):
		pass

	def G(self, hit):
		return 1

	def pdf(self, hit):
		return 1

class PointLight(Light):
	def __init__(self, shadow, position, ls, color):
		Light.__init__(self, shadow)
		self.position = position
		self.ls = ls
		self.color = color

	def get_direction(self, hit):
		return (self.position - hit.point).get_normalized()

	def in_shadow(self, scene, ray):
		ts = Vector3.distance(self.position, ray.origin)
		return scene.tracer.shadow_hit(ray, 0.00001, lambda t:0<t<ts)

	def L(self, hit, scene):
		rp = (hit.point - self.position).sqr_magnitude()
		return self.ls*self.color/rp

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
		return scene.tracer.shadow_hit(ray, 0.00001)

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
		return scene.tracer.shadow_hit(ray, 0.00001)

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
		return AmbientOccluder(sampler, ls, col, minam)

class AreaLight(Light):
	def __init__(self, shadow, obj):
		Light.__init__(self, shadow)
		self.obj = obj
		self.material = obj.material

	def get_direction(self, hit):
		self.sample_point = self.obj.sample()
		self.light_normal = self.obj.get_normal(self.sample_point)
		self.light_dir = (self.sample_point - hit.point).get_normalized()
		return self.light_dir

	def in_shadow(self, scene, ray):
		ts = Vector3.dot(self.sample_point - ray.origin, ray.direction)
		return scene.tracer.shadow_hit(ray, 0.00001,lambda t:t<ts)

	def L(self, hit, scene):
		ndl = Vector3.dot(-1*self.light_normal, self.light_dir)
		if ndl > 0.0:
			return self.material.shade(hit, scene, 0, Material.em_pass)
		return Color.black


	def G(self, hit):
		ndl = Vector3.dot(-1*self.light_normal, self.light_dir)
		return ndl/((hit.point-self.sample_point).sqr_magnitude())

	def pdf(self, hit):
		return self.obj.pdf(hit)

	@staticmethod
	def create(params):
		gtype = params['geometric_object']
		gparams = params['geometric_params']
		go = create_from_scene_file(gtype, gparams)
		samplerType = gparams['sampler']
		nums = gparams['num_samples']
		sampler = eval('%s(%d)'%(samplerType, nums))
		go.set_sampler(sampler)
		shadow = False
		if 'shadow' in params:
			shadow = params['shadow'] == 1
		return AreaLight(shadow, go)

class EnvironmentLight(Light):
	def __init__(self, sampler, shadow, material):
		Light.__init__(self, shadow)
		self.sampler = sampler
		self.sampler.map_samples_to_hemisphere(1)
		self.material = material
		
	def get_direction(self, hit):
		self.w = hit.normal
		self.v = Vector3.cross(Vector3(0.0034, 1.0, 0.0071), self.w)
		self.v.normalize()
		self.u = Vector3.cross(self.v, self.w)
		pos = self.sampler.sample_hemisphere()
		self.light_dir = pos.x*self.u + pos.y*self.v+pos.z*self.w
		return self.light_dir

	def in_shadow(self, scene, ray):
		return scene.tracer.shadow_hit(ray, 0.00001)

	def L(self, hit, scene):
		return self.material.shade(hit, scene, 0, Material.em_pass)

	def pdf(self, hit):
		return Vector3.dot(hit.normal, self.light_dir)/math.pi 

	@staticmethod
	def create(params):
		samplertype = params['sampler']
		samplenum = params['num_samples']
		sampler = eval('%s(%d)'%(samplertype, samplenum))
		shadow = False
		if 'shadow' in params:
			shadow = params['shadow'] == 1
		if 'shader' in params:
			params['shader'] = Res.combine_res_path(params['shader'])
		mat = Material(params["shader"])
		if 'shader_params' in params:
			for p in params["shader_params"]:
				mat.set_param(p, params["shader_params"][p])
		return EnvironmentLight(sampler, shadow, mat)

def create_light(ltype, params):
	if 'use' in params and params['use'] == False:
		return None
	createCmd = '%s.create(%s)'%(ltype,params)
	l = eval(createCmd)
	return l