import os.path

from Color import *

def generate_shader(scriptContent, shadepass):
	head = 'from Vector import *\nfrom Color import Color\nimport math\nfrom Light import *\nfrom Scene import *\nfrom Tracer import *\n'
	entry = '\n%s(hit, scene, reflcol, output)'%shadepass
	return head + scriptContent + entry 

class Material:
	def __init__(self, shader):
		if os.path.exists(shader) == True:
			file = open(shader)
			shaderScript = file.read()
			file.close()
			self.shader = shaderScript
		else:
			self.shader = None
		self.params = {}

	def set_param(self, key, value):
		self.params[key] = value

	def set_params(self, params):
		self.params = params

	def get_param(self, key):
		if key in self.params:
			return self.params[key]
		return None

	def shade(self, hit, scene, reflcol, shadepass='main'):
		if self.shader == None:
			return Color.error
		self.params['hit'] = hit
		self.params['scene'] = scene
		self.params['reflcol'] = reflcol
		self.params['output'] = {}
		shadercode = generate_shader(self.shader, shadepass)
		exec(shadercode, self.params)
		if 'result' in self.params['output']:
			return self.params['output']['result']
		return Color.error
