import sys

sys.path.append('core')

from Scene import Scene

if __name__ == "__main__":
	scene = Scene()
	if scene.initScene('../res/testscene1.json') == True:
		scene.render('../outputs/testscene1')


