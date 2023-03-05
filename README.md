## Kernighan-Lin Algorithm

The Kernighan-Lin Algorithm is a graph partitioning algorithm that tries to split a graph into two sets, each with approximately the same number of nodes, and with a minimum number of edges between them. The algorithm was first published in 1970 by Brian Kernighan and S. Lin.

### The Kernighan-Lin Algorithm works as follows:

1. Divide the nodes of the graph into two roughly equal parts, partition A and partition B.

2. Calculate the total weight of the edges between partition A and partition B, and call it the gain of the partition.

3. For each node in partition A, calculate the gain in the total weight of the edges that would result if it were moved to partition B. Similarly, for each node in partition B, calculate the gain in the total weight of the edges that would result if it were moved to partition A.

4. Choose the node from partition A or partition B with the highest gain, and move it to the other partition.

5. Recalculate the gains for all nodes affected by the move, and choose the node with the highest gain to move next. Repeat until no further gains are possible.

6. The algorithm returns the two partitions, along with the total weight of the edges between them, which is known as the cutset.

### Implementation Details

The Kernighan-Lin Algorithm has been implemented in Python 3. The algorithm takes as input a netlist file containing the graph to be partitioned. The file is read in using the `read_netlist` function and a `Graph` object is created based on the information contained in the file.

The `Graph` class is used to represent a graph in memory as a collection of vertices and edges with connectivity information. The `Vertex` class is used to represent a vertex in the graph, with an id, a list of edges connected to the vertex, and a partition label indicating whether the vertex belongs to partition A or partition B. The `Edge` class is used to represent an edge in the graph, with left and right vertices and their respective ids.

The `KernighanLin` class is used to perform the graph partitioning. It takes as input a `Graph` object and performs the Kernighan-Lin algorithm to split the graph into two partitions. The `partition` method of this class returns the two partitions, along with the total weight of the edges between them.

The `write_output` function is used to write the output of the algorithm to a file, including the cutset size, and the ids of the vertices in each partition.

### credits:

- Improved from this <a href="https://github.com/mcavus/Kernighan-Lin.git">**Repository**</a>. The main changes include sorting the gains array in descending order, and using only the maximum gain for each iteration, which significantly improves performance.
- Based on the paper: <a href="https://ieeexplore.ieee.org/document/6771089">An Efficient Heuristic Procedure for Partitioning Graphs</a>
