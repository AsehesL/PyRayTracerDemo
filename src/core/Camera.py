import math
from Vector import *
from Tracer import *
from Texture import Texture
from Sampler import *
from Scene import *

class Camera:
	def __init__(self, position, forward, up, d, pixelWidth, pixelHeight):
		self.near = d
		self.f = forward.getNormalized()
		r = Vector3.cross(up, forward)
		self.r = r.getNormalized()
		u = Vector3.cross(forward, r)
		self.u = u.getNormalized()
		self.position = position
		self.pixelWidth = pixelWidth
		self.pixelHeight = pixelHeight

	def screenPointToRay(self, point):
		d = self.r*point.x + self.u*point.y + self.f * self.near
		return Ray(self.position, d.getNormalized())

	def setSampler(self, sampler):
		self.sampler = sampler

	def setRenderTarget(self, target):
		self.target = target

	def render(self, scene):
		for j in range(0,self.target.height()):
			for i in range(0,self.target.width()):
				r = Color.black
				for n in range(0,self.sampler.numSamples):
					sp = self.sampler.sampleUnitSquare()
					x = self.pixelWidth*(i-0.5*(self.target.width())+sp.x)
					y = self.pixelHeight*((self.target.height()-1- j)-0.5*(self.target.height())+sp.y)
				
					ray = self.screenPointToRay(Vector2(x,y))
					r += scene.tracer.trace(ray, scene, 0.000001)
				if r != None:
					self.target.setPixel(i,j,r/self.sampler.numSamples)


def createCamera(params):
	pos = Vector3(params['position'][0],params['position'][1],params['position'][2])
	f = Vector3(params['forward'][0],params['forward'][1],params['forward'][2])
	u = Vector3(params['up'][0],params['up'][1],params['up'][2])
	d = params['near']
	samplerType = params['sampler']
	nums = params['num_samples']
	sampler = eval('%s(%d)'%(samplerType, nums))
	pw = params["pixel_width"]
	ph = params["pixel_height"]
	cam = Camera(pos, f, u, d, pw, ph)
	cam.setSampler(sampler)
	return cam