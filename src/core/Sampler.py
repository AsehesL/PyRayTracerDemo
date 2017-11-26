import random

from Vector import Vector2

class Sampler:
	def __init__(self, numSamples):
		self.numSamples = numSamples
		self.index = 0

	def sample_unit_square(self):
		pass

class RamdomSampler(Sampler):
	def __init__(self, numSamples):
		Sampler.__init__(self, numSamples)
		self.__samples = []
		for i in range(0, 83):
			sp = Vector2(random.random(), random.random())
			self.__samples.append(sp)

	def sample_unit_square(self):
		Sampler.sample_unit_square(self)
		s = self.__samples[int(self.index%len(self.__samples))]
		self.index += 1
		return s

class JitteredSampler(Sampler):
	def __init__(self, numSamples):
		pass

