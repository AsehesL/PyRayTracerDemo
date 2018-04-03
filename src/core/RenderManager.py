from Scene import Scene
from concurrent.futures import ProcessPoolExecutor

class RenderManager:
	def __init__(self, cfg, cellsize):
		self.executor = ProcessPoolExecutor()

		self.scene = Scene()

		if scene.init_scene('../res/refltest.json') == True:
			scene.render('../outputs/refltest')

	def render(self, cfgpath, cellsize):
		if os.path.exists(cfgpath) == False:
			print("配置文件不存在：%s"%cfgpath)
			return False
		try:
			file = open(cfgpath)
			cfgjson = json.load(file)
			file.close()
			
			dpcfg = cfgjson["Result"]

			width = int(dpcfg["width"])
			height = int(dpcfg["height"])
			
		except:
			print('渲染失败，请检查文件：%s'%cfgpath)
			return False
		
		return True