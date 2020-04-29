from school import School
from student import Student


class DA(object):
	def __init__(self, students, schools):
		assert len(students)>0
		assert len(schools)>0
		self.students = students
		self.schools = schools

	def _round(self, verbose=False):
		action_in_round = False
		for std in self.students:
			if std.is_unassigned():
				std.choose_school_and_apply(diagnose=verbose)
				action_in_round = True
		if action_in_round:
			for sch in self.schools:
				if sch.received_app_in_round():
					sch.DA_select()
		
		if verbose:
			self.print_student_assignment()
			self.print_school_assignment()
		# import pdb; pdb.set_trace()
		return action_in_round

	def print_student_assignment(self):
		print({std: std.assigned_school for std in self.students})
	
	def print_school_assignment(self):
		print({sch: sch.current_students for sch in self.schools})
		
	def run(self, limit=10000, verbose=False):
		action_in_round = True
		i = 0
		while action_in_round:
			i += 1
			action_in_round = self._round(verbose=verbose)
			if i>limit:
				raise RuntimeError('reached iteration limit %s' % limit)
			# if i==1:
			# 	import pdb; pdb.set_trace()

	def clear_result(self):
		for std in self.students:
			std.clear_result()
		for sch in self.schools:
			sch.clear_result()

	def show_result(self):
		print('\nallocation result:')
		for std in self.students:
			print('\tstudent %s <-> school %s' % (std, std.assigned_school))

		return {std: std.assigned_school for std in self.students}
