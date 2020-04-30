# from school import School


class Student(object):
	def __init__(self, name, schools=None):
		"""
		self.schools: list of all schools
		self.assigned_school: (school) currently assigned school
		self.rejected_schools: dict school (school) -> bool (T for reject)
		self.preference_order: list of schools (school) ordered by preference
		self.preference_keys: list of ints, correspond to keys in preference_order but ordered by value

		"""
		self.name = name
		self.schools = schools
		self.assigned_school = None
		# self.current_app = 0
		# self.preference_keys = []
		self.rejected_schools = {}
		self.preference_order = []

	def __repr__(self):
		return self.name

	def __hash__(self):
		return hash(self.name)

	def is_unassigned(self):
		return self.assigned_school is None

	def init_preference(self, schools, preference_order):
		assert schools is not None
		self.schools = schools
		self.preference_order = preference_order
		# self.preference_keys = sorted(preference_order.keys())

	def clear_result(self):
		self.assigned_school = None
		self.rejected_schools = {}

	def submit_app(self, school):
		success = school.receive(self)
		if not success:
			raise RuntimeError('%s does not receive your application' % school)

	def choose_school_and_apply(self, diagnose=False):
		for sch in self.preference_order:
			if sch in self.rejected_schools:
				continue
			else:
				if diagnose:
					print('%s applies to %s' % (self, sch))
				self.submit_app(sch)
				return

	def hear_back(self, school, accept):
		if accept:
			self.assigned_school = school
		else:
			self.rejected_schools[school] = True
			if self.assigned_school == school:
				self.assigned_school = None

	def strategize_preference(self):
		pass
