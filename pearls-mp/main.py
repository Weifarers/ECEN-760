from read import *
from initialize import *
from update import *


def main():
    # Prompts users for a file name containing the graph structure.
    graph_name = input('Graph Structure File: ')
    node_list = read_graph(graph_name)
    # Prompts users for a file name containing the possibles values of the nodes.
    val_name = input('Node Value File: ')
    node_list = read_val(val_name, node_list)
    # Prompts users for a file name containing the probabilities.
    prob_name = input('Probability File: ')
    node_list = read_prob(prob_name, node_list)
    # Initializes the graph structure.
    evidence, node_list = initialize(node_list)
    exit_flag = False
    while not exit_flag:
        # Resets the nodes and evidence to their initial values.
        node_list = read_graph(graph_name)
        node_list = read_val(val_name, node_list)
        node_list = read_prob(prob_name, node_list)
        evidence, node_list = initialize(node_list)
        # Prompts the user for a node and value of interest.
        int_node = input('Input the node of interest and its value (ex: A1): ')
        # Prompts the user for all the evidence.
        evi_nodes = input('Input all evidence nodes (ex: B1 C0 D1). If there is no evidence, type None: ')
        if evi_nodes == 'None':
            # Gets the name and value associated with the node of interest.
            interest_name, interest_val = name_val(int_node)
            # Since there is no evidence, we need only the marginal distribution given no evidence, which we
            # initialized as 'Empty.'
            cond_prob = node_list[interest_name].cond[interest_val]['Empty']
            print('The conditional probability of', int_node, 'given no evidence is', '{0:0.4f}.'.format(cond_prob))
        else:
            # Gets the name and value associated with the node of interest.
            interest_name, interest_val = name_val(int_node)
            # Updates the network for every evidence given.
            evidence_list = evi_nodes.split(' ')
            for e in evidence_list:
                evidence, node_list = update(e, node_list, evidence)
            # Creates a list of the evidence.
            evi_list = list()
            for v in evidence:
                evi_list.append(v + str(evidence[v]))
            # Gets the conditional probability given the evidence.
            try:
                cond_prob = node_list[interest_name].cond[interest_val][tuple(sorted(evi_list))]
            # If the exact conditional probability doesn't exist, then a message wasn't sent, so we have to
            # use a different metric.
            except KeyError:
                # Gets a list of all the conditional probabilities.
                cond_list = list(node_list[interest_name].cond[interest_val].keys())
                # Scores each conditional probability by the number of shared indices with the evidence.
                score_dict = score(evi_list, cond_list)
                # The one with the most amount of similar indices is the one that we want.
                condition = max(score_dict, key=score_dict.get)
                cond_prob = node_list[interest_name].cond[interest_val][condition]
            print('The conditional probability of', int_node, 'given', evi_nodes, 'is', '{0:0.4f}.'.format(cond_prob))
        # Cycling exit prompt, for convenience.
        exit_prompt = input('Would you like to make another query? (Y or N): ')
        if exit_prompt == 'Y':
            exit_flag = False
        else:
            exit_flag = True


def score(int_list, total_list):
    score_dict = {}
    # Iterates through all the conditional probabilities.
    for curr_list in total_list:
        # Function that scores each index in total list based on the number of shared indices with int_list.
        list_score = 0
        # Looks at the indices for each conditional probability.
        for t_idx in curr_list:
            # If that probability is inside the one of interest, update the list score.
            if t_idx in int_list:
                list_score += 1
        score_dict[curr_list] = list_score
    return score_dict


main()
