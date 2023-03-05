def read_netlist(filename):
	"""
	This is a Python function that reads in a netlist file and creates a Graph object based on the information contained in the file.
	It returns a new Graph object created with the vertices and edges lists. The Graph object represents the netlist in memory as a collection of vertices and edges with connectivity information.

	"""
	with open(filename, 'r') as file:
		edges = []
		vertices = []
		seen_vertex_ids = set()
		
		for line in list(file):
			v_list = line.split()
			left_id = int(v_list[0])
			right_id = int(v_list[1])
			
			edges.append(Edge(left_id, right_id))
			
			if left_id not in seen_vertex_ids:
				vertices.append(Vertex(left_id))
				seen_vertex_ids.add(left_id)
				
			if right_id not in seen_vertex_ids:
				vertices.append(Vertex(right_id))
				seen_vertex_ids.add(right_id)
		
		return Graph(vertices, edges)
    
def write_output(file_path, cutset, partition1, partition2):
    with open(file_path, 'w') as f:
        f.write(str(cutset) + '\n')
        f.write(' '.join(map(str, partition1)) + '\n')
        f.write(' '.join(map(str, partition2)) + '\n')
        
class Vertex:
	"""
	A class to represent a vertex in a graph.

	Attributes:
		id (int): The unique identifier of the vertex.
		edges (list): A list of edges connected to the vertex.
		partition_label (str): The partition (A or B) to which the vertex belongs.
	"""

	def __init__(self, id):
		"""
		Initializes a new instance of the Vertex class.

		Args:
		    id (int): The unique identifier of the vertex.
		"""
		self.id = id
		self.edges = []
		self.partition_label = None

	def get_D_value(self):
		"""
		Calculates the D-value of the vertex.

		Returns:
			The D-value of the vertex.
		"""
		D_value = 0

		for edge in self.edges:
			other_v = edge.left_v if edge.right_id == self.id else edge.right_v
			D_value += 1 if other_v.partition_label != self.partition_label else -1

		return D_value

	def add_edge(self, edge):
		"""
		Adds a new edge to the vertex.

		Args:
		    edge (Edge): The edge to add to the vertex.
		"""
		if not any(e.left_id == edge.right_id and e.right_id == edge.left_id for e in self.edges):
		    self.edges.append(edge)


class Edge:
	"""
	A class to represent an edge in a graph.

	Attributes:
		left_id (int): The unique identifier of the vertex at the left end of the edge.
		right_id (int): The unique identifier of the vertex at the right end of the edge.
		left_v (Vertex): The vertex object at the left end of the edge.
		right_v (Vertex): The vertex object at the right end of the edge.
	"""

	def __init__(self, left_id, right_id):
		"""
		Initializes a new instance of the Edge class.

		Args:
		    left_id (int): The unique identifier of the vertex at the left end of the edge.
		    right_id (int): The unique identifier of the vertex at the right end of the edge.
		"""
		self.left_id = left_id
		self.right_id = right_id
		self.left_v = None
		self.right_v = None


class Graph:
	"""
	A class to represent a graph.

	Attributes:
		vertices (list): A list of vertices in the graph.
		edges (list): A list of edges in the graph.
	"""

	def __init__(self, vertices, edges):
		"""
		Initializes a new instance of the Graph class.

		Args:
			vertices (list): A list of vertices in the graph.
			edges (list): A list of edges in the graph.
		"""
		self.vertices = vertices
		self.edges = edges
		vertex_dict = {v.id: v for v in self.vertices}

		# Assign the vertices and edges to each other and create the adjacency list for each vertex
		for edge in self.edges:
			edge.left_v = vertex_dict[edge.left_id]
			edge.right_v = vertex_dict[edge.right_id]
			vertex_dict[edge.left_id].add_edge(edge)
			vertex_dict[edge.right_id].add_edge(edge)

	def get_partition_cost(self):
		"""
		Calculates the cost of the partition.

		Returns:
		    The cost of the partition.
		"""
		return sum(1 for edge in self.edges if edge.left_v.partition_label != edge.right_v.partition_label)

       
class KernighanLin():
	"""
	Kernighan-Lin algorithm for graph partitioning.

	Attributes:
		graph (Graph): Graph to be partitioned.
	"""
	def __init__(self, graph):
		"""
		Initialize a new instance of the KernighanLin class.

		Args:
		    graph (Graph): Graph to be partitioned.
		"""
		self.graph = graph

	def partition(self):
		"""
		Perform graph partitioning using the Kernighan-Lin algorithm.

		Returns:
			Tuple[str, List[int], List[int]]: A tuple containing the cutset size,
			a list of vertex IDs in group A, and a list of vertex IDs in group B.
		"""
		# Partition the vertices into two equal-sized groups A and B.
		half = len(self.graph.vertices) // 2
		for i in range(half):
			self.graph.vertices[i].partition_label = "A"
			self.graph.vertices[i + half].partition_label = "B"
		
		total_gain = 0
		
		# Keep track of the total gain in each iteration.
		for _ in range(half):
			# Get the vertices in groups A and B and their D values.
			group_a = [v for v in self.graph.vertices if v.partition_label == "A"]
			group_b = [v for v in self.graph.vertices if v.partition_label == "B"]
			D_values = {v.id: v.get_D_value() for v in self.graph.vertices}
			
			# Compute the gains for all possible vertex swaps between groups A and B.
			gains = []
			
			for a in group_a:
				for b in group_b:
					c_ab = len(set(a.edges).intersection(b.edges))
					gain = D_values[a.id] + D_values[b.id] - (2 * c_ab)
					gains.append([[a, b], gain])
					
			# Sort the gains in descending order and get the maximum gain.       
			gains = sorted(gains, key=lambda x: x[1], reverse=True)
			max_gain = gains[0][1]
			if max_gain <= 0:
				break
				
			# Get the pair of vertices with the maximum gain and swap their partition labels.    
			pair = gains[0][0]
			group_a.remove(pair[0])
			group_b.remove(pair[1])
			pair[0].partition_label = "B"
			pair[1].partition_label = "A"
			
			# Update the D values of the vertices in groups A and B.
			for x in group_a:
				c_xa = len(set(x.edges).intersection(pair[0].edges))
				c_xb = len(set(x.edges).intersection(pair[1].edges))
				D_values[x.id] += 2 * c_xa - 2 * c_xb

			for y in group_b:
				c_yb = len(set(y.edges).intersection(pair[1].edges))
				c_ya = len(set(y.edges).intersection(pair[0].edges))
				D_values[y.id] += 2 * c_yb - 2 * c_ya
				
			# Update the total gain.
			total_gain += max_gain

		# Get the cutset size and the vertex IDs in groups A and B.
		cutset = str(self.graph.get_partition_cost())
		group_a = [v.id for v in self.graph.vertices if v.partition_label == "A"]
		group_b = [v.id for v in self.graph.vertices if v.partition_label == "B"]

		# Print the results
		print("Cutset size: {}".format(cutset))
		print("Group A vertices: {}".format(group_a))
		print("Group B vertices: {}".format(group_b))

		return cutset, group_a, group_b

"""
The key change is sorting the gains array in descending order, and using only the maximum gain for each iteration, which significantly improves performance.
"""
if __name__ == "__main__":
    filename = "test.net"
    graph = read_netlist(filename)
    kl = KernighanLin(graph)
    cutset, partition_1, partition_2 = kl.partition()
    
    output_name = "kernighan_lin_out_" + filename.split(".")[0] + ".txt"
    write_output(output_name, cutset, partition_1, partition_2)
