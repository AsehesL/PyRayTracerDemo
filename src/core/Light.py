from Vector import Vector3
from Color import *
from Tracer import *

class Light:
	def __init__(self):
		pass

	def get_direction(self, hit):
		pass

	def L(self, hit):
		pass

class PointLight(Light):
	def __init__(self, position, ls, color):
		Light.__init__(self)
		self.position = position
		self.ls = ls
		self.color = color

	def get_direction(self, hit):
		return (self.position - hit.point).get_normalized()

	def L(self, hit):
		return self.ls*self.color

	@staticmethod
	def create(params):
		ls = params['ls']
		pos = Vector3(params['position'][0],params['position'][1],params['position'][2])
		col = Color(params['color'][0], params['color'][1], params['color'][2], params['color'][3])
		return PointLight(ls, col)

class DirectionalLight(Light):
	def __init__(self, direction, ls, color):
		Light.__init__(self)
		self.direction = direction.get_normalized()
		self.ls = ls
		self.color = color

	def get_direction(self, hit):
		return self.direction

	def L(self, hit):
		return self.ls*self.color

	@staticmethod
	def create(params):
		ls = params['ls']
		d = Vector3(params['direction'][0],params['direction'][1],params['direction'][2])
		col = Color(params['color'][0], params['color'][1], params['color'][2], params['color'][3])
		return DirectionalLight(ls, col)

class Ambient(Light):
	def __init__(self, ls, color):
		Light.__init__(self)
		self.ls = ls
		self.color = color

	def get_direction(self, hit):
		return Vector3.zero

	def L(self, hit):
		return self.ls*self.color

	@staticmethod
	def create(params):
		ls = params['ls']
		col = Color(params['color'][0], params['color'][1], params['color'][2], params['color'][3])
		return Ambient(ls, col)
		

def create_light(ltype, params):
	createCmd = '%s.create(%s)'%(ltype,params)
	l = eval(createCmd)
	return l