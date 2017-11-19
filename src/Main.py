import PIL.Image
import sys

sys.path.append('core')

from Scene import Scene

if __name__ == "__main__":
	scene = Scene(640,320)
	scene.initScene()
	scene.render()

# print(dir(PIL.Image))

# newImg = PIL.Image.new("RGB", (640,320),(0,0,0))

# sphere = Sphere(Vector3(0,0,7),2)

# hit = RayHitPoint()

# for j in range(0,320):
# 	for i in range(0,640):
#  		#newImg.putpixel((i,j),(255,0,0))
#  		x = 0.3*(i-0.5*(640-1))
#  		y = 0.3*(j-0.5*(320-1))
#  		ray = Ray(Vector3(x,y,0), Vector3.forward)
#  		if sphere.hit(ray, hit, 0.000001):
#  			newImg.putpixel((i,j), (255,0,0))

# newImg.save("test.png", "PNG")