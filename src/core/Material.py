import os.path

from Color import *

def generateShader(scriptContent):
	head = 'from Vector import *\nfrom Color import Color\nimport math\n'
	entry = '\nmain(hit, scene, output)'
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

	def setParam(self, key, value):
		self.params[key] = value

	def setParams(self, params):
		self.params = params

	def getParams(self, key):
		if key in self.params:
			return self.params[key]
		return None

	def render(self, hit, scene):
		if self.shader == None:
			return Color.error
		self.params['hit'] = hit
		self.params['scene'] = scene
		self.params['output'] = {}
		exec(self.shader, self.params)
		if 'result' in self.params['output']:
			return self.params['output']['result']
		return Color.error
