import os.path

from Color import *

def generateShader(scriptContent):
	head = 'from Vector import *\nfrom Color import Color\nimport math\n'
	entry = '\nmain(hit, scene, reflcol, output)'
	return head + scriptContent + entry 

class Material:
	def __init__(self, shader):
		if os.path.exists(shader) == True:
			file = open(shader)
			shaderScript = file.read()
			file.close()
			self.shader = generateShader(shaderScript)
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

	def render(self, hit, scene, reflcol):
		if self.shader == None:
			return Color.error
		self.params['hit'] = hit
		self.params['scene'] = scene
		self.params['reflcol'] = reflcol
		self.params['output'] = {}
		exec(self.shader, self.params)
		if 'result' in self.params['output']:
			return self.params['output']['result']
		return Color.error
