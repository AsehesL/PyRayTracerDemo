import sys

sys.path.append('core')

from Scene import *
from RenderManager import RenderManager

if __name__ == "__main__":
	mgr = RenderManager()
	mgr.init('../res/refltest.json', '../outputs/refltest')

	# scene = Scene()
	# if scene.init_scene('../res/skytest.json') == True:
	# 	scene.render('../outputs/skytest')
	# 	scene.render_debug(237,86)


