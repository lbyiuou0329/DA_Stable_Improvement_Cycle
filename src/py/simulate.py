import random

from tqdm.auto import tqdm

from world import World
from school import School
from student import Student

NUM_STUDENTS = 3
NUM_SCHOOLS = 3

class Simulation(World):

	def init_example(self, schools_list):
		# example from http://www.eecs.harvard.edu/cs286r/courses/fall09/papers/stable-improvement-cycles.pdf
		x = School('X')
		y = School('Y')
		z = School('Z')

		s1 = Student('1')
		s2 = Student('2')
		s3 = Student('3')

		self.schools = [x, y, z]
		self.students = [s1, s2, s3]

		x.init_preference(self.students, {
				0: [s1],
				1: [s2, s3]
			})
		y.init_preference(self.students, {
				0: [s2],
				1: [s1, s3]
			})
		z.init_preference(self.students, {
				0: [s3],
				1: [s1, s2]
			})

		for i in range(len(self.students)):
			std = self.students[i]
			schools = [self.schools[pos] for pos in schools_list[i]]
			# print(std, schools)
			std.init_preference(self.schools, schools)

		# s1.init_preference(self.schools, [y, x, z])
		# s2.init_preference(self.schools, [z, y, x])
		# s3.init_preference(self.schools, [y, z, x])

		self.calculate_permutations()

	def run_example(self, method, schools_list, show=False, diagnose=False):
		# import pdb; pdb.set_trace()
		self.init_example(schools_list)
		self.use_DA()
		stats = []

		if method == 'single':
			for permutation in self.permutations:
				single_order = {self.students[i]: permutation[i] for i in range(3)}
				result = self.simulate('single', 1, show=show, diagnose=diagnose, single_order=single_order)
				# import pdb; pdb.set_trace()
				stats.append(result)
			result = sum(stats)/len(stats)
		elif method == 'multiple':
			result = self.simulate('multiple', self.calculate_num_rounds(), show=show, diagnose=diagnose, sosm=None)
		else:
			raise NotImplementedError('invalid method %s' % method)

		return result

	def compare_methods(self, schools_list):
		single_result = self.run_example('single', schools_list=schools_list)
		multiple_result = self.run_example('multiple', schools_list=schools_list)
		# print(single_result, multiple_result)
		return single_result, multiple_result

	def simulate_example(self, rnds=10, input_schools_list=None):
		for rnd in tqdm(range(rnds)):
			# print('round', rnd)

			if input_schools_list is None:
				schools_list = []
				school_fake_list = list(range(NUM_SCHOOLS))
				for _ in range(NUM_STUDENTS):
					random.shuffle(school_fake_list)
					schools_list.append(school_fake_list)
			else:
				schools_list = input_schools_list

			single_result, multiple_result = self.compare_methods(schools_list=schools_list)
			if single_result < multiple_result:
				import pdb; pdb.set_trace()

if __name__=='__main__':
	w = Simulation()
	w.simulate_example(rnds=500)

	# single higher
	# w.simulate_example(input_schools_list=[[2,0,1],
	# 								[2,0,1],
	# 								[0,2,1]])

	# single higher
	# w.simulate_example(input_schools_list=[[2,1,0],
	# 								[2,1,0],
	# 								[1,2,0]])

