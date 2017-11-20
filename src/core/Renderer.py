import sys

from Vector import Vector3

class Renderer:

	def __init__(self):
		self.t = sys.float_info.max
		self.point = Vector3.zero
		self.normal = Vector3.zero

	def reset(self):
		self.t = sys.float_info.max