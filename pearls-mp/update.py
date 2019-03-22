from send import *


def update(v, node_list, evidence):
    # Gets the name and the evidence associated with the current value.
    v_name, v_val = name_val(v)
    # Adds the node to the evidence.
    evidence[v_name] = v_val
    # Iterates through all potential values of v.
    for val in node_list[v_name].val:
        # If we are looking at the instantiated value:
        if val == v_val:
            # Sets the lambda value and pi value to 1.
            node_list[v_name].l_val[val] = 1
            node_list[v_name].p_val[val] = 1
            # Sets the conditional probability given the evidence to 1.
            evi_list = list()
            for v in evidence:
                evi_list.append(v + str(evidence[v]))
            node_list[v_name].cond[val].update({tuple(evi_list): 1})
        # If we are not at the instantiated value:
        else:
            # Sets the lambda value and pi values to 0.
            node_list[v_name].l_val[val] = 0
            node_list[v_name].p_val[val] = 0
            # Sets the conditional probability given the evidence to 0.
            evi_list = list()
            for v in evidence:
                evi_list.append(v + str(evidence[v]))
            node_list[v_name].cond[val].update({tuple(evi_list): 0})
    # Sends a lambda message to all parents of V not in the evidence.
    for z in node_list[v].parents:
        if z not in evidence.keys():
            node_list = send_lambda(v, z, node_list, evidence)
    # Sends a pi message to all children of V.
    for y in node_list[v].children:
        node_list = send_pi(v, y, node_list, evidence)
    return evidence, node_list


def name_val(x):
    # Gets the label associated with the marginal distribution.
    label = list(map(str, x))
    # Gets the name associated with the marginal distribution.
    name = label[0]
    # Gets the binary value associated with the marginal distribution.
    val = int(label[1])
    return name, val
