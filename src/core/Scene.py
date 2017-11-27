import json
import os.path

from Texture import Texture
from GeometricObject import *
from Tracer import *
from Color import Color
from Camera import *
from Light import *

current_progress = -1

def log_progress(progress):
	pgs = int(progress*100)
	if pgs == current_progress:
		return
	current_progress = pgs
	print('当前渲染进度：%d%%'%(current_progress)) 

class Scene:
	def __init__(self):
		self.color = Color(1,0,0)
		self.lights = []
		self.tracer = SimpleTracer(1)

	def init_scene(self, scenePath):
		if os.path.exists(scenePath) == False:
			return False
		try:
			file = open(scenePath)
			scenejson = json.load(file)
			file.close()
			for g in scenejson["Gemoetries"]:
				self.tracer.push_obj(create_from_scene_file(g["type"],g["params"]))
			for l in scenejson["Lights"]:
				if l["type"] == "Ambient":
					self.ambient = create_light(l["type"], l["params"])
				else:
					self.lights.append(create_light(l["type"], l["params"]))
			camPamras = scenejson["Camera"]
			self.camera = create_camera(camPamras["params"])
			cfg = scenejson["Result"]
			self.tex = Texture(cfg["width"], cfg["height"])
			self.camera.set_render_target(self.tex)
			
		except:
			print('加载场景失败，请检查文件：%s'%scenePath)
			return False
		return True


	def render(self, outputPath):
		print("开始渲染")
		self.camera.render(self, log_progress)
		print("渲染结束")
		self.tex.save(outputPath)

	