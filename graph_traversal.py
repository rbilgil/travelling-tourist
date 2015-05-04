graph = {
	"Victoria": ["Oxford Circus", "Picadilly Circus", "Kings Cross", "Leicester Square"],
	"Oxford Circus": ["Victoria", "Leicester Square"],
	"Picadilly Circus": ["Victoria", "Oxford Circus"],
	"Leicester Square": ["Victoria", "Kings Cross"],
	"Kings Cross": ["Victoria", "Picadilly Circus"]
}

def is_connected(graph):
	node_length = len(graph)
	connected_nodes = []
	for node, conns in graph.iteritems():
		print node
		result = traverse(node, graph, visited_nodes = [], depth = 0)
		connected_nodes.append(result)

	return connected_nodes

def traverse(current_node, graph, visited_nodes = [], depth = 0):
	paths = []
	if current_node not in visited_nodes:
		visited_nodes.append(current_node)

	connections = graph[current_node]
	
	for next_node in connections:
		path = [next_node]
		if len(visited_nodes) < len(graph):
			if next_node in visited_nodes:
				paths.append(path)
			else:
				current_node = next_node
				breadth = 0
				depth += 1

			return traverse(current_node, graph, visited_nodes, depth, breadth)
		else:
			print visited_nodes
			return len(visited_nodes) == len(graph)
	

print is_connected(graph)
