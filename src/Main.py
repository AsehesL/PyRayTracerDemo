import sys

sys.path.append('core')

from Scene import Scene

if __name__ == "__main__":
	scene = Scene(640,320)
	scene.initScene('../res/testscene1.json')
	scene.render()


