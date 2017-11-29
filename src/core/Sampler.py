import random
import math

from Vector import *

class Sampler:
	def __init__(self, numSamples):
		self.numSamples = numSamples
		self.samples = []
		self.hemisphere_samples = []
		self.index = 0
		self.hindex = 0

	def sample_unit_square(self):
		pass

	def sample_hemisphere(self):
		pass

	def map_samples_to_hemisphere(self, e):
		for i in range(0, len(self.samples)):
			cos_phi = math.cos(2.0*math.pi*self.samples[i].x)
			sin_phi = math.sin(2.0*math.pi*self.samples[i].x)
			cos_theta = math.pow(1.0-self.samples[i].y,1.0/(e+1.0))
			sin_theta = math.sqrt(1.0-cos_theta*cos_theta)
			pu = sin_theta*cos_phi
			pv = sin_theta*sin_phi
			pw = cos_theta
			self.hemisphere_samples.append(Vector3(pu,pv,pw))

class RandomSampler(Sampler):
	def __init__(self, numSamples):
		Sampler.__init__(self, numSamples)
		for i in range(0, 83):
			sp = Vector2(random.random(), random.random())
			self.samples.append(sp)

	def sample_unit_square(self):
		s = self.samples[int(self.index%len(self.samples))]
		self.index += 1
		return s

	def sample_hemisphere(self):
		s = self.hemisphere_samples[int(self.hindex%len(self.hemisphere_samples))]
		self.hindex += 1
		return s

class JitteredSampler(Sampler):
	def __init__(self, numSamples):
		pass

