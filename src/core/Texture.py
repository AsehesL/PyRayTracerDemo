import PIL.Image
import Color

class Texture:
	def __init__(self, width, height):
		self.pic = PIL.Image.new("RGB", (width, height),(0,0,0))

	def width(self):
		return self.pic.width

	def height(self):
		return self.pic.height

	def set_pixel(self, x,y,color):
		self.pic.putpixel((x,y), color.to_rgb32())

	def save(self, path):
		self.pic.save("%s.png"%(path), "PNG")


