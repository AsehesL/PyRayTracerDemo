import json
import os.path

from Texture import Texture
from GeometricObject import *
from Tracer import *
from Color import Color
from Camera import *

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
			self.camera = createCamera(camPamras["params"])
			cfg = scenejson["Result"]
			self.tex = Texture(cfg["width"], cfg["height"])
			self.camera.setRenderTarget(self.tex)
			
		except:
			print('加载场景失败，请检查文件：%s'%scenePath)
			return False
		return True


	def render(self, outputPath):
		self.camera.render(self)
		self.tex.save(outputPath)