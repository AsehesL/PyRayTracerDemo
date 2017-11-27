from Color import *

class BRDF:
	def __init__(self):
		pass

	def f(self, hit, wi, wo):
		pass

	def sample_f(self, hit, wi, wo):
		pass

	def rho(self, hit, wo):
		pass

class Lambertian(BRDF):
	def __init__(self):
		BRDF.__init__(self)

	def f(self, hit, wi, wo):
		BRDF.f(self, hit, wi, wo)
		return self.kd*self.cd/3.1415926535

	def rho(self, hit, wo):
		BRDF.rho(self, hit, wo)
		return self.kd*self.cd

