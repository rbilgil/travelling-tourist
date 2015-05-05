from graph import Graph
filename = "tube_data/tube_graph.json"

def tube_data_as_graph():	
	tube = Graph()
	tube.from_json_file(filename)

	return tube

if __name__ == '__main__':
	tube = tube_data_as_graph()
	bfs = tube.bfs(tube.vertices()[0])
	print len(bfs), len(tube.vertices())