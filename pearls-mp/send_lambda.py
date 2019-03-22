from send_pi import *


def send_lambda(y, x, node_list, evidence):
    print('sending a lambda message from ', y, 'to', x)
    # Iterates through all the values of X.
    for x_val in node_list[x].val:
        # Sets the curr_x string, which we use to search for all conditional probabilities involving this string.
        curr_x = x + str(x_val)
        # Initializes the lambda message being sent from Y to X.
        yx_l_msg = 0
        # Iterates over all the other values of y.
        for y_val in node_list[y].val:
            # Gets all the conditional probabilities associated with the current y_val and x_val.
            # Also removes the curr_x from the conditional probabilities, because we only care about the values
            # of the other parents.
            condition_list = [[j for j in i if j != curr_x] for i in node_list[y].cond[y_val] if curr_x in i]
            # Initializes the product of the conditional probability and the pi messages.
            cond_pi_y = 1
            # Iterates through all the conditions.
            for condition in condition_list:
                # Gets the conditional probability associated with the current condition.
                cond_prob = node_list[y].cond[y_val][tuple(sorted([curr_x] + condition))]
                # Initializes the product of pi messages being sent from all the parents to Y.
                wp_p_msg = 1
                # Iterates through all the elements of the remaining conditions.
                for cond_elem in condition:
                    # Gets the name and value associated with the current condition.
                    cond_name, cond_val = name_val(cond_elem)
                    # Gets the pi message sent from the parent to Y at the current value of the parent.
                    wp_p_msg = wp_p_msg * node_list[cond_name].p_msg[y][cond_val]
                cond_pi_y = cond_prob * wp_p_msg
            # Sums together all the condition probabilities times the pi messages times the lambda values.
            yx_l_msg = yx_l_msg + cond_pi_y * node_list[y].l_val[y_val]
        # Updates the lambda message being sent from Y to the current value of X.
        node_list[y].l_msg[x][x_val] = yx_l_msg
        # Initializes the lambda value for the current value of X.
        x_l_val = 1
        # Cycles through all the children of X.
        for u in node_list[x].children:
            # Multiples together all the lambda messages being sent from children to the current value of X.
            x_l_val = x_l_val * node_list[u].l_msg[x][x_val]
        # Updates the lambda value at the current value of x.
        node_list[x].l_val[x_val] = x_l_val
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
            node_list[x].cond[xc_val] = {'Empty': node_list[x].nnmarg[xc_val] / alpha}
        else:
            # Converts the evidence dictionary into a list.
            evi_list = list()
            for v in evidence:
                evi_list.append(v + str(evidence[v]))
            node_list[x].cond[xc_val][tuple(evi_list)] = node_list[x].nnmarg[xc_val] / alpha
    # Iterates through all the children of X.
    for z in node_list[x].parents:
        # Checks if Z is not in the evidence already.
        if z not in evidence:
            node_list = send_lambda(x, z, node_list, evidence)
    # Gets the other children of X that are not Y.
    other_children = [other for other in node_list[x].children if other != y]
    # Iterates through all the other children.
    for child in other_children:
        # Sends pi messages to all the other children of X.
        node_list = send_pi(x, child, node_list, evidence)
    return node_list


def name_val(x):
    # Gets the label associated with the marginal distribution.
    label = list(map(str, x))
    # Gets the name associated with the marginal distribution.
    name = label[0]
    # Gets the binary value associated with the marginal distribution.
    val = int(label[1])
    return name, val
