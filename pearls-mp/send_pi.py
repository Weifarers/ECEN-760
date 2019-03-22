from send_lambda import *


def send_pi(z, x, node_list, evidence):
    if len(evidence) != 0:
        print('sending a pi message from ', z, 'to', x)
    # Sends a pi message from a parent Z (for each of its' values) to a child X.
    # Iterates through all values of the parent Z.
    for z_val in node_list[z].val:
        # Initializes the pi message being sent from Z to X with the pi value.
        zx_p_msg = node_list[z].p_val[z_val]
        # Gets all other children of the node that are not X.
        other_children = [c for c in node_list[z].children if c != x]
        # Iterates through all the other children.
        for child in other_children:
            # Gets the lambda message sent from each child to the current value of node Z.
            child_l_msg = node_list[child].l_msg[z][z_val]
            # Multiples all the lambda messages sent from the children of Z to the current value of Z.
            zx_p_msg = zx_p_msg * child_l_msg
    # Checks if X is not in the evidence.
    if x not in evidence:
        # Iterates through all the values of X.
        for x_val in node_list[x].val:
            # Gets all the conditional probabilities associated with the current value of X.
            # These tell us the various combinations of parent values that we need to sum over.
            condition_list = node_list[x].cond[x_val]

            # Iterates over every condition in the list.
            temp_pi_val = 0
            for condition in condition_list:
                if condition == 'Empty':
                    continue
                # Gets the conditional probability for the current condition.
                cond_prob = node_list[x].cond[x_val][condition]
                # Initializes the product of pi messages for the elements of the conditional probability.
                cond_p_msg = 1
                # print(x + str(x_val), condition)
                # Goes through every element in the conditional probability.
                for condition_parent in condition:
                    # Skips the conditional probability given no evidence.
                    # Gets the name of the parent, and its' current value.
                    par_name, par_val = name_val(condition_parent)
                    # Gets the pi message sent from the parent to child node X at the current value of the parent.
                    # Multiplies them all together.
                    cond_p_msg = cond_p_msg * node_list[par_name].p_msg[x][par_val]
                # Sums together the conditional probabilities times their respective pi messages.
                temp_pi_val = temp_pi_val + cond_prob * cond_p_msg
            # Updates the pi value at the current value of X.
            node_list[x].p_val[x_val] = temp_pi_val
            # Calculates the non-normalized marginal distribution of the current value of X.
            node_list[x].nnmarg[x_val] = node_list[x].l_val[x_val] * node_list[x].p_val[x_val]
        # Initializes the normalization constant alpha.
        alpha = 0
        for xu_val in node_list[x].val:
            # Adds all the non-normalized marginal distributions to create alpha.
            alpha = alpha + node_list[x].nnmarg[xu_val]
        for xc_val in node_list[x].val:
            # Gets the conditional probability given no evidence.
            if len(evidence) == 0:
                node_list[x].cond[xc_val]['Empty'] = node_list[x].nnmarg[xc_val]/alpha
            # Adds the conditional probability if there is evidence.
            else:
                # Converts the evidence dictionary into a list.
                evi_list = list()
                for v in evidence:
                    evi_list.append(v + str(evidence[v]))
                node_list[x].cond[xc_val][tuple(evi_list)] = node_list[x].nnmarg[xc_val]/alpha
        # Propagates the pi messages through all other children of X.
        for y in node_list[x].children:
            node_list = send_pi(x, y, node_list, evidence)
    # Iterates through all the values of X.
    for xl_val in node_list[x].val:
        # Checks if the lambda value at the current value of X is 1.
        if node_list[x].l_val[xl_val] != 1:
            # Creates a list of all the parents of X that are not Z.
            par_list = [par for par in node_list[x].parents if par != z]
            # Cycles through all the parents.
            for w in par_list:
                # Checks to see if the parent is not in the evidence.
                if w not in evidence:
                    node_list = send_lambda(x, w, node_list, evidence)
    return node_list


def name_val(x):
    # Gets the label associated with the marginal distribution.
    label = list(map(str, x))
    # Gets the name associated with the marginal distribution.
    name = label[0]
    # Gets the binary value associated with the marginal distribution.
    val = int(label[1])
    return name, val
