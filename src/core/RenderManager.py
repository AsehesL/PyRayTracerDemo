from Scene import Scene
from Texture import Texture
from Camera import *
from Color import *
from multiprocessing import Queue
from concurrent.futures import ProcessPoolExecutor

queue = Queue()
colorqueue = Queue()

def log_progress(progress):
	pgs = int(progress*100)
	print('当前队列初始化进度：%d%%'%(pgs)) 

class RenderManager:
	def __init__(self):
		self.executor = ProcessPoolExecutor()

		# self.scene = Scene()

		# if scene.init_scene('../res/refltest.json') == True:
		# 	scene.render('../outputs/refltest')

	def init(self, cfgpath, outputPath):
		if os.path.exists(cfgpath) == False:
			print("配置文件不存在：%s"%cfgpath)
			return False
		try:
			file = open(cfgpath)
			cfgjson = json.load(file)
			file.close()

			print("加载摄像机")		

			camPamras = cfgjson["Camera"]
			self.camera = create_camera(camPamras["params"])
			cfg = cfgjson["Result"]

			print("初始化渲染配置")
			self.tex = Texture(cfg["width"], cfg["height"])
			self.camera.set_render_target(self.tex)

			print("等待队列初始化完成")
			self.camera.render_for_task(queue, log_progress)

			print("队列初始化完成")
			taskResults = []

			for i in range(0, self.executor._max_workers):
				taskResults.append(self.executor.submit(RenderManager.render_task, cfgpath, i))

			for result in taskResults:
				result.result()

			while colorqueue.empty() == False:
				dt = colorqueue.get(True)
				self.tex.set_pixel(dt[0], dt[1], dt[2])
			
			self.tex.save(outputPath)

		except:
			print('渲染失败，请检查文件：%s'%cfgpath)
			return False
		
		return True

	@staticmethod
	def render_task(cfgpath, pid):
		print('pid:%d'%(pid))
		scene = Scene()
		scene.init_scene(cfgpath)
		while queue.empty() == False:
			dt = queue.get(True)
			for ray in dt[0]:
				r = Color.black
				r += scene.tracer.trace(ray, scene, 0.000001)
			r = r/len(dt[0])
			print('渲染进程ID:%d，x:%d,y:%d,color:%s'%(pid, dt[1], dt[2], str(r)))
			colorqueue.put((dt[1],dt[2],r))
