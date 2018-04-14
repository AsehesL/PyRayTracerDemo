import os.path
#import threading

from Color import *
from Sampler import *

def generate_shader(scriptContent, shadepass):
	head = 'from Vector import *\nfrom Color import Color\nimport math\nfrom Light import *\nfrom Scene import *\nfrom Tracer import *\nfrom Sampler import *\n'
	entry = '\n%s(hit, scene, output)'%shadepass
	return head + scriptContent + entry 

class Material:
	def __init__(self, shader, params = None):
		if os.path.exists(shader) == True:
			file = open(shader)
			shaderScript = file.read()
			file.close()
			self.shader = shaderScript
		else:
			self.shader = None
		self.params = {}
		#self.mutes = threading.Lock()
		if params != None:
			for p in params:
				Material.set_param(self, p, params[p])

	def set_param(self, key, value):
		if key == 'sampler':
			tp = value['type']
			num = value['num_samples']
			exp = value['exp']
			s = eval('%s(%d)'%(tp, num))
			s.map_samples_to_hemisphere(exp)
			self.params['sampler'] = s
			return
		self.params[key] = value

	# def set_params(self, params):
	# 	self.params = params

	def get_param(self, key):
		if key in self.params:
			return self.params[key]
		return None

	def shade(self, hit, scene, shadepass='main'):
		if self.shader == None:
			return Color.error
		#self.mutes.acquire()
		params = self.params.copy()

		params['hit'] = hit
		params['scene'] = scene
		params['output'] = {}
		shadercode = generate_shader(self.shader, shadepass)
		exec(shadercode, params)
		col = Color.error
		if 'result' in params['output'] and params['output']['result'] != None:
			col = params['output']['result']
		#self.mutes.release()
		return col

Material.main_pass = 'main'
Material.em_pass = 'em_main'
