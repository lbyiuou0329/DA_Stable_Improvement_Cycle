from scc import Graph, scc
from student import Student


class DA_solution(object):
	def __init__(self, students, schools):
		self.students = students
		self.schools = schools
		self.init()

	def init(self):
		self.nodes = []
		self.graph = {}
		self._find_student_preferred_schools()
		self._school_point_to_students()

	def _school_point_to_students(self):
		for sch in self.schools:
			self.graph[sch] = []
			self.nodes.append(sch)
			for std in sch.current_students:
				self.graph[sch].append(std)
				
	def _find_student_preferred_schools(self):
		for std in self.students:
			if std.assigned_school is None:
				continue
			self.graph[std] = []
			self.nodes.append(std)
			for sch in std.preference_order:
				if sch is std.assigned_school:
					break
				else:
					self.graph[std].append(sch)

	def find_cycles(self):
		self.init()
		self.g = Graph(self.graph, self.nodes)
		self.list_scc = scc(self.g)
		self.list_scc = [scc for scc in self.list_scc if len(scc)>1] # remove single node scc
		if len(self.list_scc) == 0:
			return False
		else:
			# print(self.list_scc)
			return True

	def update_cycle(self):
		if len(self.list_scc) == 1:
			biggest_scc = self.list_scc[0]
		else:
			biggest_scc = sorted(self.list_scc, key=lambda scc: len(scc), reverse=True)[0]

		if not isinstance(biggest_scc[0], Student):
			sch = biggest_scc.pop(0)
			biggest_scc.append(sch)

		i = 0
		while i < len(biggest_scc):
			std = biggest_scc[i]
			preferred_sch = biggest_scc[i+1]
			# assign student to next element, which is the school this student points to
			# import pdb; pdb.set_trace()
			# self.graph[std] = [preferred_sch]
			# self.graph[preferred_sch] = [std]
			std.assigned_school = biggest_scc[i+1] 
			i += 2

	def stable_improvement_cycle(self, limit=10):
		cycle_exists = True
		cnt = 0
		while cycle_exists and cnt < limit:
			cycle_exists = self.find_cycles()
			cnt += 1
			if cycle_exists:
				self.update_cycle()
		success = cnt != limit
		return success, {std: std.assigned_school for std in self.students}

