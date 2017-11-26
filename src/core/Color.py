import colorsys
import math

class Color:
	def __init__(self, r, g, b, a=1.0):
		self.r = r
		self.g = g
		self.b = b
		self.a = a

	def __getitem__(self, index):
		if index<0 or index >=4:
			raise Exception("无效的索引")
		if index == 0:
			return self.r
		elif index == 1:
			return self.g
		elif index == 2:
			return self.b
		return self.a

	def __setitem__(self, index, value):
		if index<0 or index >=4:
			raise Exception("无效的索引")
		if index == 0:
			self.r = value
		elif index == 1:
			self.g = value
		elif index == 2:
			self.b = value
		else:
			self.a = value

	def grayscale(self):
		return 0.299*self.r+0.587*self.g+0.114*self.b

	def to_hsv(self):
		return colorsys.rgb_to_hsv(self.r, self.g, self.b)

	def to_rgb32(self):
		return (int(self.r*255),int(self.g*255),int(self.b*255),int(self.a*100))

	def __str__(self):
		return 'Color:(%f, %f, %f, %f)'%(self.r,self.g,self.b,self.a)

	def __repr__(self):
		return 'Color(%s, %s, %s, %s)'%(repr(self.r),repr(self.g),repr(self.b),repr(self.a))

	def __eq__(self, other):
		if other == None:
			return False
		return math.isclose(self.r, other.r) and math.isclose(self.g, other.g) and math.isclose(self.b, other.b) and math.isclose(self.a, other.a)

	def __add__(self, other):
		return Color(self.r+other.r, self.g+other.g, self.b+other.b, self.a+other.a)

	def __sub__(self, other):
		return Color(self.r-other.r, self.g-other.g, self.b-other.b, self.a-other.a)

	def __mul__(self, other):
		return Color(self.r*other.r, self.g*other.g, self.b*other.b, self.a*other.a)

	def __rmul__(self, n):
		return Color(self.r*n, self.g*n, self.b*n, self.a*n)

	def __truediv__(self, n):
		return Color(self.r/n, self.g/n, self.b/n, self.a/n)

	def __floordiv__(self, n):
		return Color(self.r//n, self.g//n, self.b//n, self.a//n)

	@staticmethod
	def lerp(a,b,t):
		if t < 0:
			t = 0
		elif t > 1:
			t = 1
		return Color(a.r+(b.r-a.r)*t, a.g+(b.g-a.g)*t, a.b+(b.b-a.b)*t, a.a+(b.a-a.a)*t)

	@staticmethod
	def hsv_to_rgb(h, s, v, a=1.0):
		hv = h/360.0
		rgb = colorsys.hsv_to_rgb(hv,s,v)
		return Color(rgb[0],rgb[1],rgb[2],a)


Color.red = Color(1,0,0,1)
Color.green = Color(0,1,0,1)
Color.blue = Color(0,0,1,0)
Color.white = Color(1,1,1,1)
Color.black = Color(0,0,0,1)
Color.yellow = Color(1,1,0,1)
Color.magenta = Color(1,0,1,1)
Color.cyan = Color(1,0,1,1)
Color.gray = Color(0.5,0.5,0.5,1)
Color.error = Color(1,0,0.75,1)
