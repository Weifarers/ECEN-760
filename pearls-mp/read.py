from node import Node


def read_graph(graph_file):
    # Opens the graph file.
    graph = open(graph_file, 'r')
    # Gets the number of nodes and the number of edges.
    num_data = graph.readline().rstrip().split(' ')
    (num_node, num_edge) = map(int, num_data)
    # Gets the list of nodes.
    nodes = graph.readline().rstrip().split(' ')
    # Gives each node a value of a node object, and gives it a name.
    node_list = dict()
    for i in range(len(nodes)):
        node_name = nodes[i]
        node_list[node_name] = Node()
        node_list[node_name].name = node_name
    # Organizes all the parents and children defined by the edges.
    for x in range(num_edge):
        # Gets each edge.
        temp_edge = graph.readline().rstrip().split(' ')
        # Defines the parent and the child in each edge.
        parent = temp_edge[0]
        child = temp_edge[1]
        # Assigns the parents and the children to each object.
        node_list[parent].add_children(child)
        node_list[child].add_parent(parent)
    return node_list


def read_prob(prob_file, node_list):
    # Opens the probability file.
    prob = open(prob_file, 'r')
    for temp_prob in prob:
        temp_prob = temp_prob.rstrip().split(' ')
        # Splits a label into its' string and binary value.
        name, val = name_val(temp_prob[0])
        # If the probability only contains two strings, then it is a marginal distribution.
        if len(temp_prob) == 2:
            # Gets the marginal distribution.
            marg_prob = float(temp_prob[1])
            # Assigns the binary value the marginal distribution.
            node_list[name].marg[val] = marg_prob
        else:
            # Gets the index for where the condition separator is.
            sep_index = temp_prob.index('|')
            # The conditions of a conditional probability are always after the separator.
            condition = temp_prob[sep_index + 1:]
            for x in condition:
                # This gets the probability by searching for the string with a decimal point.
                if '.' in x:
                    cond_prob = float(x)
                    condition.remove(x)
            # Adds a new dictionary, where the key is the condition, and the value is the probability.
            # Initializes the dictionary if it doesn't already exist.
            if val not in node_list[name].cond:
                node_list[name].cond[val] = {tuple(condition): cond_prob}
            # If the dictionary does exist, just updates it with a new value.
            else:
                node_list[name].cond[val].update({tuple(condition): cond_prob})
    return node_list


def read_val(val_file, node_list):
    # Opens the value file.
    val = open(val_file, 'r')
    # Each line contains a node and its potential values.
    for nodes in val:
        node = nodes.rstrip().split(' ')
        # Gets the name.
        node_name = node[0]
        # Gets the values.
        node_val = node[1:]
        # Converts the values into integers, and assigns them to the potential values of the node.
        node_list[node_name].val = list(map(int, node_val))
    return node_list


def name_val(x):
    # Gets the label associated with the marginal distribution.
    label = list(map(str, x))
    # Gets the name associated with the marginal distribution.
    name = label[0]
    # Gets the binary value associated with the marginal distribution.
    val = int(label[1])
    return name, val
