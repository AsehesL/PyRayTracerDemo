from Texture import Texture
from GeometricObject import *
from RayCaster import *
from Vector import *
from Color import Color

class Scene:
	def __init__(self, renderWidth, renderHeight):
		self.tex = Texture(renderWidth, renderHeight)
		self.color = Color(1,0,0)

	def initScene(self):
		self.sphere = Sphere(Vector3(0,0,40),6)
		self.hit = RayHitPoint()


	def render(self):
		for j in range(0,self.tex.height()):
			for i in range(0,self.tex.width()):
 				x = 0.3*(i-0.5*(self.tex.width()-1))
 				y = 0.3*(j-0.5*(self.tex.height()-1))
 				ray = Ray(Vector3(x,y,0), Vector3.forward)
 				if self.sphere.hit(ray, self.hit, 0.000001):
 					self.tex.setPixel(i,j, self.color)
		self.tex.save("aass")