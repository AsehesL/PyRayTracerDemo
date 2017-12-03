import sys

sys.path.append('core')

from Scene import Scene

if __name__ == "__main__":
	scene = Scene()
	if scene.init_scene('../res/refltest.json') == True:
		scene.render('../outputs/refltest')
		#scene.render_debug(237,86)


