import random
import math

from Vector import *

class Sampler:
	def __init__(self, numSamples, numSets=83):
		self.num_samples = numSamples
		self.num_sets = numSets
		self.samples = []
		self.hemisphere_samples = []
		self.disk_samples = []
		self.sphere_samples = []
		self.index = 0
		self.jump = 0
		Sampler.setup_shuffled_indices(self)

	def setup_shuffled_indices(self):
		indexes = []
		self.shuffled_indices = []
		for i in range(0, self.num_samples):
			indexes.append(i)
		for p in range(0, self.num_sets):
			random.shuffle(indexes)
			for j in range(0, self.num_samples):
				self.shuffled_indices.append(indexes[j])

	def shuffle_x_coordinates(self):
		for i in range(0, self.num_sets):
			for j in range(0, self.num_samples-1):
				target = int(random.randint(0,self.num_samples-1)+i*self.num_samples)
				temp = self.samples[j+i*self.num_samples+1].x
				self.samples[j+i*self.num_samples+1].x = self.samples[target].x
				self.samples[target].x = temp

	def shuffle_y_coordinates(self):
		for i in range(0, self.num_sets):
			for j in range(0, self.num_samples-1):
				target = int(random.randint(0,self.num_samples-1)+i*self.num_samples)
				temp = self.samples[j+i*self.num_samples+1].y
				self.samples[j+i*self.num_samples+1].y = self.samples[target].y
				self.samples[target].y = temp

	def sample_unit_square(self):
		if int(self.index % self.num_samples) == 0:
			self.jump = random.randint(0, self.num_sets - 1)*self.num_samples
		ind = self.samples[self.jump + self.shuffled_indices[self.jump + self.index % self.num_samples]]
		self.index += 1
		return ind

	def sample_unit_disk(self):
		if int(self.index % self.num_samples) == 0:  		
			self.jump = random.randint(0, self.num_sets - 1)*self.num_samples
		ind = self.disk_samples[self.jump + self.shuffled_indices[self.jump + self.index % self.num_samples]]
		self.index += 1
		return ind

	def sample_hemisphere(self):
		if int(self.index % self.num_samples) == 0:  		
			self.jump = random.randint(0, self.num_sets - 1)*self.num_samples
		ind = self.hemisphere_samples[self.jump + self.shuffled_indices[self.jump + self.index % self.num_samples]]
		self.index += 1
		return ind

	def sample_sphere(self):
		if int(self.index % self.num_samples) == 0:  		
			self.jump = random.randint(0, self.num_sets - 1)*self.num_samples
		ind = self.sphere_samples[self.jump + self.shuffled_indices[self.jump + self.index % self.num_samples]]
		self.index += 1
		return ind

	def map_samples_to_unit_disk(self):
		for j in range(0, len(self.samples)):
			sp = Vector2(2.0*self.samples[j].x-1.0, 2.0*self.samples[j].y-1.0)
			if sp.x > - sp.y:
				if sp.x > sp.y:
					r = sp.x
					phi = sp.y / sp.x
				else:
					r = sp.y
					phi = 2 - sp.x / sp.y
			else:
				if sp.x < sp.y:
					r = -sp.x
					phi = 4 + sp.y / sp.x
				else:
					r = -sp.y
					if sp.y != 0.0:
						phi = 6 - sp.x/sp.y
					else:
						phi = 0.0
			phi *= math.pi / 4.0
			self.disk_samples.append(Vector2(r*math.cos(phi),r*math.sin(phi)))

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

	def map_samples_to_sphere(self):
		for i in range(0, len(self.samples)):
			r1 = self.samples[i].x 
			r2 = self.samples[i].y
			z = 1.0 - 2.0 * r1
			r = math.sqrt(1.0 - z * z)
			phi = math.pi*2*r2
			x = r*math.cos(phi)
			y = r*math.sin(phi)
			self.sphere_samples.append(Vector3(x,y,z))

class RandomSampler(Sampler):
	def __init__(self, numSamples, numSets=83):
		Sampler.__init__(self, numSamples, numSets)
		for i in range(0, self.num_sets):
			for j in range(0, self.num_samples):
				self.samples.append(Vector2(random.random(), random.random()))

class JitteredSampler(Sampler):
	def __init__(self, numSamples, numSets=83):
		Sampler.__init__(self, numSamples, numSets)
		n = int(math.sqrt(numSamples))
		for i in range(0, self.num_sets):
			for j in range(0, n):
				for k in range(0, n):
					sp = Vector2((k+random.random())/n, (j+random.random())/n)
					self.samples.append(sp)

class HammersleySampler(Sampler):
	def __init__(self, numSamples, numSets=83):
		Sampler.__init__(self, numSamples, numSets)
		for i in range(0, self.num_sets):
			for j in range(0, self.num_samples):
				sp = Vector2(j/self.num_samples, Hammersley.__phi(self, j))
				self.samples.append(sp)

	def __phi(self, j):
		x = 0.0
		f = 0.5
		while j:
			x += f * (j%2)
			j /= 2
			f *= 0.5
		return x

class NRooksSampler(Sampler):
	def __init__(self, numSamples, numSets=83):
		Sampler.__init__(self, numSamples, numSets)
		for i in range(0, self.num_sets):
			for j in range(0, self.num_samples):
				sp = Vector2((j+random.random())/self.num_samples, (j+random.random())/self.num_samples)
				self.samples.append(sp)
		self.shuffle_x_coordinates()
		self.shuffle_y_coordinates()


class RegularSampler(Sampler):
	def __init__(self, numSamples, numSets=83):
		Sampler.__init__(self, numSamples, numSets)
		n = int(math.sqrt(numSamples))
		for i in range(0, self.num_sets):
			for j in range(0, n):
				for k in range(0, n):
					sp = Vector2((k+0.5)/n, (j+0.5)/n)
					self.samples.append(sp)


# class MultiJitteredSampler(Sampler):
# 	def __init__(self, numSamples, numSets=83):
# 		Sampler.__init__(self, numSamples, numSets)
# 		n = int(math.sqrt(numSamples))
# 		subcellw = 1.0/self.num_samples

# 		for j in range(0, self.num_samples*self.num_sets):
			
		
