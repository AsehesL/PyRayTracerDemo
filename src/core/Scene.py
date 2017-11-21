import json
import os.path

from Texture import Texture
from GeometricObject import *
from Tracer import *
from Vector import *
from Color import Color
from Camera import Camera

class Scene:
	def __init__(self):
		self.color = Color(1,0,0)
		self.tracer = SimpleTracer(1)

	def initScene(self, scenePath):
		if os.path.exists(scenePath) == False:
			return False
		try:
			file = open(scenePath)
			scenejson = json.load(file)
			file.close()
			for g in scenejson["Gemoetries"]:
				self.tracer.pushObj(createFromSceneFile(g["type"],g["params"]))
			camPamras = scenejson["Camera"]
			self.camera = Camera.create(camPamras["params"])
			cfg = scenejson["Result"]
			self.tex = Texture(cfg["width"], cfg["height"])
			self.pixelWidth = cfg["pixelWidth"]
			self.pixelHeight = cfg["pixelHeight"]
			
		except:
			print('加载场景失败，请检查文件：%s'%scenePath)
			return False
		return True


	def render(self):
		for j in range(0,self.tex.height()):
			for i in range(0,self.tex.width()):
 				x = self.pixelWidth*(i-0.5*(self.tex.width()))
 				y = self.pixelHeight*((self.tex.height()-1- j)-0.5*(self.tex.height()))
 				ray = self.camera.screenPointToRay(Vector2(x,y))
 				r = self.tracer.trace(ray, self, 0.000001)
 				if r != None:
 					self.tex.setPixel(i,j,r)
		self.tex.save("aass")
		self.tex.show()