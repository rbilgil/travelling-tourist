from tube.graph import Graph


def tube_file_to_graph(filename):
    tube = Graph()
    tube.from_json_file(filename)

    return tube

