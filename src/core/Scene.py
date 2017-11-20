import json

from Texture import Texture
from GeometricObject import *
from Tracer import *
from Vector import *
from Color import Color
from Renderer import *
from Camera import Camera

class Scene:
	def __init__(self):
		self.color = Color(1,0,0)
		self.gemoetries = []

	def initScene(self, scenePath):
		try:
			file = open(scenePath)
			scenejson = json.load(file)
			file.close()
			for g in scenejson["Gemoetries"]:
				self.gemoetries.append(createFromSceneFile(g["type"],g["params"]))
			camPamras = scenejson["Camera"]
			self.camera = Camera.create(camPamras["params"])
			cfg = scenejson["Result"]
			self.tex = Texture(cfg["width"], cfg["height"])
			self.pixelWidth = cfg["pixelWidth"]
			self.pixelHeight = cfg["pixelHeight"]
			
		except:
			print('加载场景失败，检查路径是否正确：%s'%scenePath)
			return
		self.hit = Renderer()


	def render(self):
		for j in range(0,self.tex.height()):
			for i in range(0,self.tex.width()):
 				x = self.pixelWidth*(i-0.5*(self.tex.width()-1))
 				y = self.pixelHeight*(j-0.5*(self.tex.height()-1))
 				ray = self.camera.screenPointToRay(Vector2(x,y))
 				#print(str(ray))
 				for g in self.gemoetries:
 					if g.hit(ray, self.hit, 0.000001):
 						self.tex.setPixel(i,j,self.color)
 				#if self.sphere.hit(ray, self.hit, 0.000001):
 				#	self.tex.setPixel(i,j, self.color)
		self.tex.save("aass")