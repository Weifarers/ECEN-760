def send_pi(z, x, node_list, evidence):
    # Commented out error checker: Let's me know what pi messages are being sent.
    # if len(evidence) != 0:
    #     print('sending a pi message from ', z, 'to', x)
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
        # Updates the pi message value.
        node_list[z].p_msg[x][z_val] = zx_p_msg
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
                cond_flag = False
                # Skips the 'Empty' conditional probability that came from initialization.
                if condition == 'Empty':
                    cond_flag = True
                # Also skips instances in which conditional probabilities do not have all the parents in them.
                else:
                    cond_name_list = list()
                    for condition_check in condition:
                        check_name, check_val = name_val(condition_check)
                        cond_name_list.append(check_name)
                    if cond_name_list != node_list[x].parents:
                        cond_flag = True
                if cond_flag:
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


def send_lambda(y, x, node_list, evidence):
    # Commented out error checker: Let's me know what lambda messages are being sent.
    # if len(evidence) != 0:
    #     print('sending a lambda message from ', y, 'to', x)
    # Sends a lambda message from a child Y to a parent X (for each of its' values) .
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
            # Iterates through all the conditions.
            for condition in condition_list:
                # Skips the 'Empty' conditional probability that came from initialization.
                if condition == 'Empty':
                    continue
                # Gets the conditional probability associated with the current condition.
                cond_prob = node_list[y].cond[y_val][tuple(sorted([curr_x] + condition))]
                # Initializes the product of pi messages being sent from all the parents to Y.
                wp_p_msg = 1
                # Iterates through all the elements of the remaining conditions.
                for cond_elem in sorted(condition):
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
            node_list[x].cond[xc_val].update({tuple(evi_list): node_list[x].nnmarg[xc_val] / alpha})
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
