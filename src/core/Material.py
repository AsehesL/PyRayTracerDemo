import os.path

from Color import *

class Material:
	def __init__(self, shader):
		# if os.path.exists(shader) == False:
		# 	raise Exception("shader不存在，检查路径%s"%shader)
		# file = open('shader')
		# shaderScript = file.read()+'\n'+'main(hit, scene)'
		# file.close()

		# self.shader = shaderScript
		self.params = {}

	def setParam(self, key, value):
		self.params[key] = value

	def setParams(self, params):
		self.params = params

	def render(self, hit, scene):
		return green
		#self.params['hit'] = hit
		#self.params['scene'] = scene
		#exec(self.shader, self.params)