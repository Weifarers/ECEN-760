from send import *


def initialize(node_list):
    # Initializes an empty dictionary.
    evidence = dict()
    # Iterates through all the nodes in the structure.
    for node in node_list:
        # Iterates through every value of the node.
        for val in node_list[node].val:
            # Sets the lambda value for each node value to 1.
            node_list[node].l_val[val] = 1
        # Iterates through every parent of the node.
        for par in node_list[node].parents:
            # Initializes each set of lambda messages for each parent as a dictionary.
            node_list[node].l_msg[par] = {}
            # Iterates through all the values of the parents.
            for par_val in node_list[par].val:
                # Sets the lambda message from the node to the parent at the current par_val to 1.
                node_list[node].l_msg[par][par_val] = 1
        # Iterates through every child of the node.
        for child in node_list[node].children:
            # Initializes each set of pi messages for each child as a dictionary.
            node_list[node].p_msg[child] = {}
            # Iterates through every value that the parent node can take.
            for n_val in node_list[node].val:
                # Sets all pi messages sent from the current value of the parent to each child.
                node_list[node].p_msg[child][n_val] = 1
    # Gets all the roots by looking at whatever nodes have no parents.
    root_list = [x for x in node_list if len(node_list[x].parents) == 0]
    # Iterates through every root.
    for root in root_list:
        # Iterates through every value of the root.
        for r_val in node_list[root].val:
            node_list[root].cond[r_val] = {}
            # Makes the pi value associated with the root value equal to the marginal distribution of the root value.
            node_list[root].p_val[r_val] = node_list[root].marg[r_val]
            # Gives a conditional probability given no evidence, or 'Empty.'
            node_list[root].cond[r_val]['Empty'] = node_list[root].marg[r_val]
        # Passes pi messages to all children of the root node.
        for w in node_list[root].children:
            node_list = send_pi(root, w, node_list, evidence)
    return evidence, node_list
