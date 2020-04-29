import random

# from student import Student


class School(object):
	def __init__(self, name, capacity=1, students=None):
		"""
		self.students: unordered list of all students 
		self.applications: list of students
		self.preferences： dict student (student) -> order (int)
		self.preference_order: dict order (int) -> students (list of students). 
							small is preferred
		self.current_students: list of students that currently have a seat
		"""
		self.name = name
		self.capacity = capacity
		self.students = students

		self.applications = []
		self.current_students = []

		self.preferences = {}
		self.preference_order = {}
		
		self.raw_preference_order = {}

	def __repr__(self):
		return self.name

	def init_preference(self, students, preference_order):
		self.students = students
		self.preference_order = preference_order
		for ordr, schs in preference_order.items():
			for sch in schs:
				self.preferences[sch] = ordr

		self.raw_preference_order = preference_order

		from math import factorial
		self.num_std = len(self.students)
		self.num_permutations = factorial(self.num_std)

	def clear_result(self):
		self.applications = []
		self.current_students = []

	def break_ties(self, method='multiple', single_order=None, verbose=False, 
					rnd=None, index=None, permutations=None):
		if method == 'single':
			assert single_order is not None
			self.__break_ties_single(single_order)
		elif method == 'multiple':
			self.__break_ties_multi(rnd=rnd, index=index, permutations=permutations)
		else:
			raise NotImplementedError('invalid method %s' % method)

		if verbose:
			print('school %s strict preference order: %s' % (self, self.preference_order))

	def __break_ties_single(self, ordered_student_dict):
		"""
		ordered_student_dict: (dict) student -> int
		"""
		new_key = 0
		new_preference = {}
		for idx, students in self.raw_preference_order.items():
			if len(students) == 1:
				new_preference[new_key] = students[0]
				new_key += 1
			else:
				strict_student_list = sorted(students, key=lambda k: ordered_student_dict[k])
				for std in strict_student_list:
					new_preference[new_key] = std
					new_key += 1

		self.preference_order = new_preference
		self.preferences = {std: ordr for ordr, std in new_preference.items()}

	def __break_ties_multi(self, rnd=None, index=None, permutations=None):
		if rnd is None:
			students = self.students
			random.shuffle(students)
			shuffle_result = {std: idx for idx, std in enumerate(students)}
		else:
			assert index is not None
			assert permutations is not None
			shuffle_result = self.order_by_seed(rnd, index, permutations)

		self.__break_ties_single(shuffle_result)

	def order_by_seed(self, rnd, idx, permutations):
		cutoff = pow(self.num_permutations, idx)
		above_cutoff = cutoff * self.num_permutations # previous digit cutoff
		_rnd = rnd % above_cutoff # remove all considerations of bigger digits
		permutation_choice = _rnd // cutoff # clock for current digit
		permutation = permutations[permutation_choice]

		shuffle_result = {self.students[i]: permutation[i] for i in range(self.num_std)}
		return shuffle_result

	def receive(self, student):
		if student in self.preferences:
			self.applications.append(student)
			return True
		else:
			return False

	def prefer(self, A, B):
		if A is None:
			return False
		elif B is None:
			return True
		elif self.preferences[A] < self.preferences[B]:
			return True
		else:
			return False

	def select(self):
		# TODO: change this to accomodate for capacity>1
		favoraite = self.current_students

		for student in self.applications:
			if self.prefer(student, favoraite):
				favoraite.hear_back(self, False)
				favoraite = student
			else:
				student.hear_back(self, False)
		favoraite.hear_back(self, True)
		self.current_students = favoraite

	def received_app_in_round(self):
		return len(self.applications)>0

	def DA_select(self):
		pool = self.current_students + self.applications
		self.current_students = []
		pool = list(set(pool))

		sorted_pool = sorted(pool, key=lambda std: self.preferences[std])
		# import pdb; pdb.set_trace()
		for selected_std in sorted_pool[:self.capacity]:
			selected_std.hear_back(self, True)
			self.current_students.append(selected_std)

		for rejected_std in sorted_pool[self.capacity:]:
			rejected_std.hear_back(self, False)

		self.applications = []

