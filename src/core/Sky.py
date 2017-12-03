from Material import *
import Res

class Sky:
	def __init__(self, shader):
		self.material = Material(shader)

	def shade(self, hit, scene):
		return self.material.shade(hit, scene)


def create_sky(shader, shaderParams):
	if shader == None:
		return None
	if shaderParams == None:
		return None

	shader = Res.combine_res_path(shader)

	sky = Sky(shader)

	for p in shaderParams:
		sky.material.set_param(p, shaderParams[p])
	return sky