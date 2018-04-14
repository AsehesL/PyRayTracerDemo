import sys

sys.path.append('core')

from RenderManager import RenderManager

if __name__ == "__main__":
	mgr = RenderManager()
	mgr.init('../res/refltest.json', '../outputs/refltest')

	#scene = Scene()
	#if scene.init_scene('../res/refltest.json') == True:
	#	scene.render('../outputs/refltest')
		#scene.render_debug(237,86)


