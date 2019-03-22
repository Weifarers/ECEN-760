# Creates a class for nodes, which are defined by their parents, children, and other values of interest.
class Node(object):
    def __init__(self, name=""):
        # Gives each node a name, parents, and children.
        self.name = name
        self.parents = list()
        self.children = list()
        # Gives each node a list of values it can take.name
        self.val = list()
        # Gives each node a set of lambda and pi values.
        self.l_val = dict()
        self.p_val = dict()
        # Gives each node a set of lambda and pi messages.
        self.l_msg = dict()
        self.p_msg = dict()
        # Gives each node a set of marginal distributions and conditional probabilities.
        self.marg = dict()
        self.cond = dict()
        # Gives each node a set of non-normalized marginal distributions.
        self.nnmarg = dict()

    # Defines a function to add parents to a node.
    def add_parent(self, parent):
        self.parents.append(parent)

    # Defines a function to add children to a node.
    def add_children(self, child):
        self.children.append(child)
