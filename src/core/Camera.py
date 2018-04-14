import math
from Vector import *
from Tracer import *
from Texture import Texture
from Sampler import *
from Scene import *

class Camera:
	def __init__(self, position, forward, up, d, pixelWidth, pixelHeight):
		self.near = d
		self.f = forward.get_normalized()
		r = Vector3.cross(up, forward)
		self.r = r.get_normalized()
		u = Vector3.cross(forward, r)
		self.u = u.get_normalized()
		self.position = position
		self.pixelWidth = pixelWidth
		self.pixelHeight = pixelHeight

	def screen_point_to_ray(self, point):
		d = self.r*point.x + self.u*point.y + self.f * self.near
		return Ray(self.position, d.get_normalized())

	def set_sampler(self, sampler):
		self.sampler = sampler

	def set_render_target(self, target):
		self.target = target

	def render_for_task(self, queue, callback):
		for j in range(0,self.target.height()):
			progress = j/(self.target.height()-1)
			if callback != None:
				callback(progress)
			for i in range(0,self.target.width()):
				rays = []
				for n in range(0,self.sampler.num_samples):
					sp = self.sampler.sample_unit_square()
					x = self.pixelWidth*(i-0.5*(self.target.width())+sp.x)
					y = self.pixelHeight*((self.target.height()-1- j)-0.5*(self.target.height())+sp.y)

					ray = self.screen_point_to_ray(Vector2(x,y))

					rays.append(ray)
				queue.put((rays, i, j))

	def render(self, scene, callback):
		for j in range(0,self.target.height()):
			progress = j/(self.target.height()-1)
			if callback != None:
				callback(progress)
			for i in range(0,self.target.width()):
				r = Color.black
				for n in range(0,self.sampler.num_samples):
					sp = self.sampler.sample_unit_square()
					x = self.pixelWidth*(i-0.5*(self.target.width())+sp.x)
					y = self.pixelHeight*((self.target.height()-1- j)-0.5*(self.target.height())+sp.y)
				
					ray = self.screen_point_to_ray(Vector2(x,y))
					try:
						r += scene.tracer.trace(ray, scene, 0.000001)
					except:
						raise Exception('渲染错误，当前像素%d,%d'%(i,j))
				if r != None:
					self.target.set_pixel(i,j,r/self.sampler.num_samples)

	def render_debug(self, scene, i, j):
		r = Color.black
		for n in range(0,self.sampler.num_samples):
			sp = self.sampler.sample_unit_square()
			x = self.pixelWidth*(i-0.5*(self.target.width())+sp.x)
			y = self.pixelHeight*((self.target.height()-1- j)-0.5*(self.target.height())+sp.y)
				
			ray = self.screen_point_to_ray(Vector2(x,y))
			
			r += scene.tracer.trace(ray, scene, 0.000001)


def create_camera(params):
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
	cam.set_sampler(sampler)
	return cam