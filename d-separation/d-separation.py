import sys
import copy

# Main Function, that runs the code.
def main():
    # Constants
    edgeList = []
    queryList = []
    nodeList = []
    
    # Reads in the second argument as the file name.
    # ie: d_separated.py ex.txt will read in "ex.txt" as the file name.
    filename = sys.argv[1]

    # Opens the file, and reads in the first line.
    file = open(filename,"r")
    # We strip each string, and define the separator as a space. 
    firstLine = file.readline().rstrip().split(" ")

    # Converts the first line into the number of values of interest. 
    (numNode, numEdge, numQuery) = map(int,firstLine)

    # Because we know the ordering of the file, we iterate through the number of edges,
    # and take every set of edges from the file.
    for x in range(numEdge):
        # Again, strip any strings and define the splits.
        tempEdge = file.readline().rstrip().split(" ")
        # Stores all the nodes into a list, so we can get a set of all the nodes. 
        for y in range(len(tempEdge)):
            nodeName = tempEdge[y]
            nodeList = nodeList + [nodeName]
        # Appends the temporary edge to the full list of edges.
        edgeList = edgeList + [tempEdge]

    # Converting to a set removes all the duplicate nodes.
    nodeSet = set(nodeList)
    # Converts back into a list for later usage. 
    nodeList = list(nodeSet)

    # Repeats the procedure to get all the queries as well. 
    for x in range(numQuery):
        tempQuery = file.readline().rstrip().split(" ")
        queryList = queryList + [tempQuery]

    for x,currQuery in enumerate(queryList):
        # Gets the node of interest and the evidence.
        startNode = currQuery[0]
        evidence = currQuery[2:]
        
        # Gets all the nodes who are in the evidence, or who have descendants
        # in the evidence.
        visitA = copy.deepcopy(evidence)
        aList = copy.deepcopy(evidence)
        while len(visitA) > 0:
            currNode = visitA.pop(0)
            for y,currEdge in enumerate(edgeList):
                if currNode == currEdge[1]:
                    visitA = visitA + [currEdge[0]]
                    aList = aList + [currEdge[0]]
        aList = list(set(aList))

        # Establishes a check for whether or not the node has been visited, and
        # if it has been reached.
        reachCheck = []
        visitCheck = []
        # Initializes the list of nodes we've visited.
        visitList = [(startNode,'up')]
        while len(visitList) > 0:
            # Takes out the first node from the list to be examined.
            tempNode = visitList.pop(0)
            # Gets the nodes value, and what direction it is.
            nodeVal = tempNode[0]
            dirVal = tempNode[1]
            # Only continues if we haven't seen the node before.
            if tempNode not in visitCheck:
                # The node is reachable, assuming it's not in the evidence.
                if nodeVal not in evidence:
                    reachCheck = reachCheck + [nodeVal]
                # Checks off the node for being visited.
                visitCheck = visitCheck + [tempNode]
                # Case #1, Visiting from the bottom: Your node must not be in the evidence.
                if dirVal == 'up' and nodeVal not in evidence:
                    for x,tempEdge in enumerate(edgeList):
                        # If the node value is the child, then the other index is the parent.
                        if nodeVal == tempEdge[1]:
                            # We associate 'up' with going towards a parent.
                            visitList = visitList + [(tempEdge[0],'up')]
                        # If the node value is a parent, then the other index is a child.
                        elif nodeVal == tempEdge[0]:
                            # We associate 'down' with going towards a child.
                            visitList = visitList + [(tempEdge[1],'down')]
                # Case #2, Visiting from the top.
                elif dirVal == 'down':
                    # If the node value is not in the evidence.
                    if nodeVal not in evidence:
                        for x, tempEdge in enumerate(edgeList):
                            # We add the children of the node to the list.
                            if nodeVal == tempEdge[0]:
                                visitList = visitList + [(tempEdge[1],'down')]
                    # If the node value is not in A.
                    elif nodeVal in aList:
                        for x, tempEdge in enumerate(edgeList):
                            # We add the parents of the node to the list.
                            if nodeVal == tempEdge[1]:
                                visitList = visitList + [(tempEdge[0],'up')]
                                
        # Presentation of Results:
        dSep = list(set(nodeList) - set(reachCheck))
        print('For the query', currQuery)
        print('The nodes that are d-Separated from',startNode,'are:',*dSep,'\n')
        #print('The nodes that are reachable from',startNode,'are:',list(set(reachCheck)),'\n')

main()
