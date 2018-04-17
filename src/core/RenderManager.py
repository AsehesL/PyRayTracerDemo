from Scene import Scene
from Texture import Texture
from Camera import *
from Color import *
from multiprocessing import Process, Queue, Manager
#from concurrent.futures import ProcessPoolExecutor

def log_progress(progress):
	pgs = int(progress*100)
	print('当前队列初始化进度：%d%%'%(pgs)) 

class RenderManager:
	def __init__(self):
		pass
		#self.executor = ProcessPoolExecutor()
		#self.tasks = []

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

			#print("加载摄像机")		

			#camPamras = cfgjson["Camera"]
			#self.camera = create_camera(camPamras["params"])
			cfg = cfgjson["Result"]

			#print("初始化渲染配置")
			self.tex = Texture(cfg["width"], cfg["height"])
			#self.camera.set_render_target(self.tex)

			#print("等待队列初始化完成")
			#self.camera.render_for_task(queue, log_progress)

			#print("队列初始化完成")
			#taskResults = []

			#for i in range(0, self.executor._max_workers):
			#	taskResults.append(self.executor.submit(RenderManager.render_task, cfgpath, i))

			#for result in taskResults:
			#	result.result()

			tasks = []
			queue = Queue()
			#colorqueues = []

			bx = 0
			by = 0

			while by < self.tex.height():
				while bx < self.tex.width():
					bw = self.tex.width() - bx
					bh = self.tex.height() - by
					if bw > 32:
						bw = 32
					if bh > 32:
						bh = 32
					#print("Area Prepare: X:%d,Y:%d,W:%d,H:%d"%(bx,by,bw,bh))
					#pw = Process(target = RenderManager.render_task, args=(cfgpath, bx, by, bw, bh, colorqueue))
					queue.put((bx, by, bw, bh, self.tex.width(), self.tex.height()))
					#tasks.append(pw)
					bx += 32
				by += 32
				bx = 0

			manager = Manager()
			return_dict = manager.dict()
			for i in range(0, 8):
				#colorqueue = Queue()
				pw = Process(target = RenderManager.render_task, args=(cfgpath, i, queue, return_dict))
				#colorqueues.append(colorqueue)
				tasks.append(pw)

			for task in tasks:
				print("Task Start...")
				task.start()
				#task.join()

			# for cq in colorqueues:
			# 	while cq.empty() == False:
			# 		dt = cq.get(True)
			# 		self.tex.set_pixel(dt[0], dt[1], dt[2])

			# for cols in return_dict.values():
			# 	for c in cols:
			# 		self.tex.set_pixel(c[0], c[1], c[2])
			
			# self.tex.save(outputPath)

		except:
			print('渲染失败，请检查文件：%s'%cfgpath)
			return False
		
		return True

	@staticmethod
	def render_task(cfgpath, pid, taskqueue, colordict):
		#print('pid:%d'%(pid))
		# print("SceneInit:X:%d,Y:%d,W:%d,H:%d"%(beginx,beginy,width,height))
		# scene = Scene()
		# if scene.init_scene(cfgpath) == False:
		# 	print("Scene Init Faild")
		# 	return
		# print("Scene Render Begin")
		# scene.render_range(beginx, beginy, width, height, pixelqueue)
		# print("Range Finish")

		colors = []

		#colordict[pid] = []
		
		#if colordict.has_key(pid) == False:
		print("Key:%d"%(pid))
		colordict[7] = 5

		scene = Scene()
		if scene.init_scene(cfgpath) == False:
			print("Scene Init Faild")
			return

		while taskqueue.empty() == False:
			dt = taskqueue.get(True)
			print("Scene Render Begin:PID:%d,X:%d,Y:%d,W:%d,H:%d"%(pid,dt[0],dt[1],dt[2],dt[3]))
			scene.render_range(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5], colors)
			print("Range Finish")

			# for ray in dt[0]:
			# 	r = Color.black
			# 	r += scene.tracer.trace(ray, scene, 0.000001)
			# r = r/len(dt[0])
			# print('渲染进程ID:%d，x:%d,y:%d,color:%s'%(pid, dt[1], dt[2], str(r)))
			# pixelqueue.put((dt[1],dt[2],r))
