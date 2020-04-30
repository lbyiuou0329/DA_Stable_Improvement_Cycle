
class Node(object):
	def __init__(self, node_type, data, point_to=[]):
		"""
		node_type: (str) 'student' or 'school'
		data: (student or school object)
		point_to: list of (other) Node object
		"""
		self.node_type = node_type
		self.data = data
		self.point_to = point_to

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.data == other.data
		elif isinstance(other, type(self.data)):
			return self.data == other
		else:
			return False

	def __hash__(self):
		return hash(self.data)

	def add_point_to(self, point_to)
		self.point_to.extend(point_to)

	def replace_point_to(self, point_to)
		self.point_to = point_to


class DA_solution(object):
	def __init__(self, students, schools):
		self.students = students
		self.schools = schools
		self.student_nodes = {}
		self.school_nodes = {}
		self.graph = []

	def init(self):
		self._find_student_preferred_schools()
		self._school_point_to_students()

	def _school_point_to_students(self):
		for sch in self.schools:
			has_one_match = False
			school_node = Node('school', sch)
			for std in sch.current_students:
				if std in self.student_nodes:
					school_node.add_point_to([self.student_nodes[std]])
					has_one_match = True
			if has_one_match:
				self.school_nodes[sch] = school_node
				self.graph.append(school_node)

		self._update_student_pointers()

	def _update_student_pointers(self):
		for std_node in self.student_nodes.values():
			sch_nodes = []
			for sch in std_node.point_to:
				sch_nodes.append(self.school_nodes[sch])
			std_node.replace_point_to(sch_nodes)
		
	def _find_student_preferred_schools(self):
		for std in self.students:
			if std.assigned_school is None:
				continue
			choice_rank = std.preference_order.index(std.assigned_school)
			if choice_rank >0:
				new_node = Node('student', std)
				#TOOO: add check for student being top D_mu choices of school
				new_node.add_point_to(std.preference_order[:choice_rank])
				self.student_nodes[std] = new_node
				self.graph.append(new_node)

	def DFS(self):
		nodes = list(self.graph.keys())
		visited = {n:False for n in nodes}
		recStack = {n:False for n in nodes}

		for node in nodes:
			if not visited[node]:
				if self.DFS_util(node,visited,recStack) == True: 
                    return True
        return False

	def DFS_util(self, v, visited, recStack):
		# Mark current node as visited and  
        # adds to recursion stack 
        visited[v] = True
        recStack[v] = True
  
        # Recur for all neighbours 
        # if any neighbour is visited and in  
        # recStack then graph is cyclic 
        for neighbour in self.graph[v]: 
            if visited[neighbour] == False: 
                if self.DFS_util(neighbour, visited, recStack) == True: 
                    return True
            elif recStack[neighbour] == True: 
                return True
  
        # The node needs to be poped from  
        # recursion stack before function ends 
        recStack[v] = False
        return False

	def find_cycles(self):
		pass

	def update_cycle(Self):
		pass

	def stable_improvement_cycle(self):
		cycle_exists = True
		while cycle_exists:
			cycle_exists = self.find_cycles()
			if cycle_exists:
				self.update_cycle()

