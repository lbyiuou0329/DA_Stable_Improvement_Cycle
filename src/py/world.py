import random

from school import School
from student import Student


class World(object):
	def __init__(self):
		self.students = []
		self.schools = []
		self.algorithm = None

	def __init_students(self):
		self.students = []

	def __init_schools(self):
		self.schools = []

	def use_DA(self):
		from DA import DA
		self.algorithm = DA(self.students, self.schools)

	def print_current_allocation(self):
		print({std: std.assigned_school for std in self.students})

	def calculate_permutations(self):
		from itertools import permutations as tools_permu
		num_students = len(self.students)
		positions = list(range(num_students))
		self.permutations = list(tools_permu(positions))

	def run(self, show=False, diagnose=False):
		if self.algorithm is None:
			raise RuntimeError('must choose an algorithm first')

		self.algorithm.clear_result()
		self.algorithm.run(verbose=diagnose)
		if show:
			result = self.algorithm.show_result()
			return result
		return None

	def break_ties(self, method, verbose=False, single_order=None, rnd=None):
		if method == 'single':
			if single_order is None:
				random.shuffle(self.students)
				single_order = {std: idx for idx, std in enumerate(self.students)}

			for sch in self.schools:
				sch.break_ties(method='single', single_order=single_order, verbose=verbose)
		elif method == 'multiple':
			i = 0
			for sch in self.schools:
				sch.break_ties(method='multiple', verbose=verbose, rnd=rnd, 
								index=i, permus=self.permutations)
				i += 1
		else:
			raise NotImplementedError('invalid method %s' % method)

	def evaluate(self, sosm):
		match_all_locs = [std.assigned_school==sosm[std] for std in self.students]
		# import pdb; pdb.set_trace()
		return all(match_all_locs)

	def find_sosm(self, method, single_order, rnd):
		from stable_improvement_cycle import DA_solution
		# import pdb; pdb.set_trace()
		self.break_ties(method, single_order=single_order, rnd=rnd)
		self.run()

		solution = DA_solution(self.students, self.schools)
		success, sosm = solution.stable_improvement_cycle()
		if not success:
			self.print_current_allocation()
			raise RuntimeError('failed to find sosm')
		return sosm

	def simulate(self, method, rounds=100, show=False, diagnose=False, single_order=None, sosm=None):
		if diagnose:
			for sch in self.schools:
				print('%s preference: %s' % (sch, sch.preference_order))
		
		if method == 'single':
			if sosm is None:
				sosm = self.find_sosm(method, single_order, None)
				print('found sosm: \n\t %s' % sosm)

		stats = []

		for rnd in range(rounds):
			if rounds>1 and diagnose:
				print('\nround %s' % rnd)

			if method == 'multiple':
				sosm = self.find_sosm(method, single_order, rnd)
				if diagnose:
					print('found sosm: \n\t %s' % sosm)

			self.break_ties(method, verbose=diagnose, single_order=single_order, rnd=rnd)
			self.run(show=show, diagnose=diagnose)

			stats.append(self.evaluate(sosm))

		return sum(stats) / rounds

	def init_example(self):
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
		s1.init_preference(self.schools, [y, x, z])
		s2.init_preference(self.schools, [z, y, x])
		s3.init_preference(self.schools, [y, z, x])

		self.calculate_permutations()

		return {s1:x, s2:z, s3:y}

	def run_one_example(self):
		sosm = w.init_example()
		w.use_DA()
		result = w.simulate('single', 3, show=True, diagnose=False, single_order={self.students[i]: i for i in range(3)})
		print(result)

	def run_example_single(self):
		sosm = w.init_example()
		w.use_DA()
		# self.permutations = [[0,1,2], [0,2,1], [1,0,2], [1,2,0],[2,1,0],[2,0,1]]

		stats = []
		for permutation in self.permutations:
			single_order = {self.students[i]: permutation[i] for i in range(3)}
			print(single_order)
			w.simulate('single', 1, show=True, diagnose=False, single_order=single_order)
			# import pdb; pdb.set_trace()
			stats.append(self.evaluate(sosm))
		
		result = sum(stats)/len(stats)
		print(result)
		return result

	def calculate_num_rounds(self):
		from math import factorial
		n_student = len(self.students)
		n_schools = len(self.schools)
		return pow(factorial(n_student), n_schools)

	def run_example_multi(self):
		sosm = w.init_example()
		# self.permutations = [[0,1,2], [0,2,1], [1,0,2], [1,2,0],[2,1,0],[2,0,1]]
		w.use_DA()

		stats = []
		result = w.simulate('multiple', self.calculate_num_rounds(), show=False, diagnose=False, sosm=None)
		print(result)
		return result

	def compare_methods(self):
		single_result = self.run_example_single()
		multiple_result = self.run_example_multi()
		print(single_result, multiple_result)

if __name__=='__main__':
	w = World()
	w.run_example_multi()
