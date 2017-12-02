import math

class Vector2:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __getitem__(self, index):
		if index<0 or index >=2:
			raise Exception("无效的索引")
		if index == 0:
			return self.x
		return self.y

	def __setitem__(self, index, value):
		if index<0 or index >=2:
			raise Exception("无效的索引")
		if index == 0:
			self.x = value
		elif index == 1:
			self.y = value

	def magnitude(self):
		'''计算二维向量的模长'''
		return math.sqrt(self.x*self.x+self.y*self.y)

	def sqr_magnitude(self):
		'''计算二维向量模长的平方'''
		return self.x*self.x+self.y*self.y

	def normalize(self):
		'''计算单位向量'''
		m = self.magnitude()
		if m > 0:
			self.x /= m
			self.y /= m
		else:
			self.x = 0
			self.y = 0

	def get_normalized(self):
		vccopy = Vector2(self.x,self.y)
		vccopy.normalize()
		return vccopy

	def __str__(self):
		return '(%f, %f)'%(self.x,self.y)

	def __repr__(self):
		return 'Vector2(%s, %s)'%(repr(self.x),repr(self.y))

	def __eq__(self, other):
		return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

	def __add__(self, other):
		return Vector2(self.x+other.x, self.y+other.y)

	def __sub__(self, other):
		return Vector2(self.x-other.x, self.y-other.y)

	def __mul__(self, n):
		return Vector2(self.x*n, self.y*n)

	def __rmul__(self, n):
		return Vector2(self.x*n, self.y*n)

	def __truediv__(self, n):
		return Vector2(self.x/n, self.y/n)

	def __floordiv__(self, n):
		return Vector2(self.x//n, self.y//n)

	@staticmethod
	def lerp(a,b,t):
		if t < 0:
			t = 0
		elif t > 1:
			t = 1
		return Vector2(a.x+(b.x-a.x)*t, a.y+(b.y-a.y)*t)

	@staticmethod
	def reflect(direction, normal):
		return 2.0 * Vector2.dot(normal, direction)*normal-direction

	@staticmethod
	def angle(fromvec, tovec):
		v = Vector2.dot(fromvec.get_normalized(), tovec.get_normalized())
		if v < -1:
			v = -1
		elif v > 1:
			v = 1
		return math.acos(v) * 57.29578

	@staticmethod
	def dot(lhs, rhs):
		return lhs.x*rhs.x+lhs.y*rhs.y

	@staticmethod
	def distance(a, b):
		return (a-b).magnitude()

	@staticmethod
	def max(lhs, rhs):
		return Vector2(max(lhs.x,rhs.x), max(lhs.y,rhs.y))

	@staticmethod
	def min(lhs, rhs):
		return Vector2(min(lhs.x,rhs.x), min(lhs.y,rhs.y))

class Vector3:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def __getitem__(self, index):
		if index<0 or index >=3:
			raise Exception("无效的索引")
		if index == 0:
			return self.x
		elif index == 1:
			return self.y
		return self.z

	def __setitem__(self, index, value):
		if index<0 or index >=3:
			raise Exception("无效的索引")
		if index == 0:
			self.x = value
		elif index == 1:
			self.y = value
		elif index == 2:
			self.z = value

	def magnitude(self):
		'''计算三维向量的模长'''
		return math.sqrt(self.x*self.x+self.y*self.y+self.z*self.z)

	def sqr_magnitude(self):
		'''计算三维向量模长的平方'''
		return self.x*self.x+self.y*self.y+self.z*self.z

	def normalize(self):
		'''计算单位向量'''
		m = self.magnitude()
		if m > 0:
			self.x /= m
			self.y /= m
			self.z /= m
		else:
			self.x = 0
			self.y = 0
			self.z = 0

	def get_normalized(self):
		vccopy = Vector3(self.x,self.y, self.z)
		vccopy.normalize()
		return vccopy

	def __str__(self):
		return '(%f, %f, %f)'%(self.x,self.y,self.z)

	def __repr__(self):
		return 'Vector3(%s, %s, %s)'%(repr(self.x),repr(self.y),repr(self.z))

	def __eq__(self, other):
		return math.isclose(self.x, other.x) and math.isclose(self.y, other.y) and math.isclose(self.z,other.z)

	def __add__(self, other):
		return Vector3(self.x+other.x, self.y+other.y, self.z+other.z)

	def __sub__(self, other):
		return Vector3(self.x-other.x, self.y-other.y, self.z-other.z)

	def __mul__(self, n):
		return Vector3(self.x*n, self.y*n, self.z*n)

	def __rmul__(self, n):
		return Vector3(self.x*n, self.y*n, self.z*n)

	def __truediv__(self, n):
		return Vector3(self.x/n, self.y/n, self.z/n)

	def __floordiv__(self, n):
		return Vector3(self.x//n, self.y//n, self.z//n)

	@staticmethod
	def lerp(a,b,t):
		if t < 0:
			t = 0
		elif t > 1:
			t = 1
		return Vector3(a.x+(b.x-a.x)*t, a.y+(b.y-a.y)*t, a.z+(b.z-a.z)*t)

	@staticmethod
	def reflect(direction, normal):
		return 2.0 * Vector3.dot(normal, direction)*normal-direction

	# @staticmethod
	# def refract(direction, normal, eta):
	# 	cosi = Vector3.dot(normal, direction)
	# 	cost2 = 1.0 - eta * eta * (1.0 - cosi * cosi)
	# 	t = -direction*eta+((eta*cosi - normal*math.sqrt(abs(cost2))))
	# 	return t

	@staticmethod
	def angle(fromvec, tovec):
		v = Vector3.dot(fromvec.get_normalized(), tovec.get_normalized())
		if v < -1:
			v = -1
		elif v > 1:
			v = 1
		return math.acos(v) * 57.29578

	@staticmethod
	def dot(lhs, rhs):
		return lhs.x*rhs.x+lhs.y*rhs.y+lhs.z*rhs.z

	@staticmethod
	def cross(lhs, rhs):
		return Vector3(lhs.y * rhs.z - lhs.z * rhs.y, lhs.z * rhs.x - lhs.x * rhs.z, lhs.x * rhs.y - lhs.y * rhs.x)

	@staticmethod
	def distance(a, b):
		vec = Vector3(a.x - b.x, a.y - b.y, a.z - b.z)
		return math.sqrt(vec.x * vec.x + vec.y * vec.y + vec.z * vec.z);

	@staticmethod
	def max(lhs, rhs):
		return Vector3(max(lhs.x,rhs.x), max(lhs.y,rhs.y), max(lhs.z,rhs.z))

	@staticmethod
	def min(lhs, rhs):
		return Vector3(min(lhs.x,rhs.x), min(lhs.y,rhs.y), min(lhs.z,rhs.z))

Vector2.zero = Vector2(0,0)
Vector2.one = Vector2(1,1)
Vector2.up = Vector2(0,1)
Vector2.down = Vector2(0,-1)
Vector2.right = Vector2(1,0)
Vector2.left = Vector2(-1,0)

Vector3.zero = Vector3(0,0,0)
Vector3.one = Vector3(1,1,1)
Vector3.forward = Vector3(0,0,1)
Vector3.back = Vector3(0,0,-1)
Vector3.right = Vector3(1,0,0)
Vector3.left = Vector3(-1,0,0)
Vector3.up = Vector3(0,1,0)
Vector3.down = Vector3(0,-1,0)

