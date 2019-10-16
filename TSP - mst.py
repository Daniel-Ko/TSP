from Graph import *


def odd_degree_vertices(graph):
    """ Use graph's adjacency list to determine which nodes have an odd degree of edges"""
    return {id for id in graph.adjlist if (len(graph.adjlist[id]) % 2 == 1)}

def perfect_matching(graph):
    """ Minimum-weight perfect matching. Apparently a quite difficult problem, see attached photo """
    min_cost = 99e9
    final_matches = set()

    # Walk and create the MST
    for currn in graph.nodes.values():
        matches = set()

        # Have a diminishing pool to match from
        pool = set(graph.nodes.values())
        pool.remove(currn) 

        # Store ids of visited nodes
        visited: Set[str] = set() 
        
        # Choose shortest for this node
        min_edge = min([Edge(currn, neigh) for neigh in graph.nodes.values() if currn != neigh])

        # Now both nodes of this edge are removed from the dating....the matching pool
        pool.remove(min_edge.n2)
        matches.add(min_edge)
        cost = min_edge.weight

        # While there are eligible nodes remaining (odd number of nodes means near-perfect match and 1 left over)
        while len(pool) > 1:
            other = pool.pop()

            min_edge = min(
                [
                    Edge(other, neigh) for neigh in pool    
                    if other not in visited 
                    and neigh not in visited
                ]
            )

            pool.discard(min_edge.n1)
            pool.discard(min_edge.n2)
            matches.add(min_edge)

            cost += min_edge.weight

        # Choose this as the solution if smaller
        if cost < min_cost:
            min_cost = cost
            final_matches = matches

    assert len(final_matches) == len(graph.nodes) // 2
    
    return (final_matches, min_cost)

def eulerian_tour(graph, edges, odd_verts):
    """ Computes eulerian tour by avoiding bridges """
    tour = set()

    # If 2 odd verts, add the ones between them
    if len(odd_verts) == 2:
        tour.add(Edge(*map(graph.get_node, odd_verts)))
    elif len(odd_verts) > 2:
        for v in odd_verts:
            pair_to_v = [n for n in graph.adjlist[v] if n in odd_verts][0]
            tour.add(
                Edge(*map(graph.get_node, (v, pair_to_v)))
                )
            
    for edge in edges:
        if edge not in tour and not is_bridge(graph.adjlist, edge):   
            tour.add(edge)
    return tour

def is_bridge(adjlist, edge):
    if len(adjlist[edge.n1.id]) == 1: 
        return True

    # Check if this edge is a bridge 
    countn1 = DFS_reachable(adjlist, edge.n1.id, set())
    
    # Remove this edge and check the other node for reachable count
    adjlist[edge.n1.id].discard(edge.n2.id)
    adjlist[edge.n2.id].discard(edge.n1.id)

    countn2 = DFS_reachable(adjlist, edge.n2.id, set())
     
    # Add edge back
    adjlist[edge.n1.id].add(edge.n2.id)
    adjlist[edge.n2.id].add(edge.n1.id)

    return countn1 > countn2


def DFS_reachable(adjlist, id, reachable):
    """ How many points are reachable from this node """
    count = 1
    reachable.add(id)
    for neighid in adjlist[id]:
        if neighid not in reachable:
            count += DFS_reachable(adjlist, neighid, reachable)
    
    return count

def unvisited_from_backtrack(adjlist, id, unvisited):
    """ lol"""
    return [x for x in adjlist[list(adjlist[id])[0]] if x in unvisited][0]

def hamiltonian_path(tour):
    """ Apparently NP-hard on undirected graphs. Who scoped this assignment? """
    path = []
    unvisited = [n.id for n in tour.nodes.values()]
    
    startid = "1"
    unvisited.remove(startid)  

    # Edge case if we start at a dead end, create link to another
    if len(tour.adjlist[startid]) == 1:
        neighid = unvisited_from_backtrack(tour.adjlist, startid, unvisited)
        path.append(Edge(tour.get_node(startid), tour.get_node(neighid)))
        currid = neighid
        print(f"Started on DEAD LINK. Creating link to {currid}")
    else:
        # First neighbour of start
        for neighid in tour.adjlist[startid]:
            currid = neighid
            break
            
        path.append(Edge(tour.get_node(startid), tour.get_node(currid)))
    
    
    while len(unvisited) > 0:
        # Get all neighbours from the adjacency list
        print(f"curr: {currid}", end=" ")
        print(tour.adjlist[currid])
        print(f"\tUnvisited so far: {[n for n in unvisited]}")

        # This check is because we might backtrack from a dead end
        if currid in unvisited:
            unvisited.remove(currid)

        # If we encounter a dead end, create a new link
        if len(tour.adjlist[currid]) == 1:
            neighid = unvisited_from_backtrack(tour.adjlist, currid, unvisited)
            path.append(Edge(tour.get_node(currid), tour.get_node(neighid)))
            currid = neighid
            print(f"\tDEAD LINK. Creating link to {currid}")
            continue
        # Make sure unvisited actually has elements!
        elif tour.adjlist[currid].isdisjoint(unvisited) and unvisited:
            neighid = unvisited[0]
            path.append(Edge(tour.get_node(currid), tour.get_node(neighid)))
            currid = neighid
            print(f"\tDEAD LINK. Creating link to {currid}")
            continue
            
        # Look ahead in neighbours of currid to try to redirect to the dead-end, if it exists (for completeness)
        neighids = list(tour.adjlist[currid])
        for neighid in tour.adjlist[currid]:
            if len(tour.adjlist[neighid]) == 1 and neighid in unvisited: 
                neighids = [neighid]
                break

        # FINALLY process the neighids (or dead-end, neighids length = 1 to see where to go next)
        for neighid in neighids: 
            print(f"\tneigh: {neighid}")
            print(f"\tUnvisited so far: {[n for n in unvisited]}")

            # No more links left, complete the cycle
            if neighid == startid and len(unvisited) == 0:
                path.append(Edge(tour.get_node(currid), tour.get_node(startid)))
                print("END!")
                break
            
            # Ignore visited neighbour
            if neighid not in unvisited:
                print("\tVISITED\n")
                continue
            
            # Otherwise, process this neighbour
            path.append(Edge(tour.get_node(currid), tour.get_node(neighid)))
            currid = neighid
            print(f"\tPROCESSED\n")
            break
    
    print(path)
    # Return the edgelist we follow, and the final cost
    return (path, sum([e.weight for e in path]))
        
def test():
    """ Make sure methods are working as intended good lord """
    # Test Edge and Node class implementation comparisons with priority queue
    fringe = PriorityQueue()
    fringe.put(Edge(
        Node("1", "10", "0"),
        Node("2", "13", "0")
    ))
    fringe.put(Edge(
        Node("1", "10", "0"),
        Node("3", "15", "5")
    ))
    fringe.put(Edge(
        Node("2", "13", "0"),
        Node("3", "15", "5")
    ))

    first = fringe.get()
    assert first.n1.id == "1"
    assert first.n2.id == "2"
    assert first.weight == 3

    second = fringe.get()
    assert second.n1.id == "2"
    assert second.n2.id == "3"
    assert second.weight == 5.385164807134504

    third = fringe.get()
    assert third.n1.id == "1"
    assert third.n2.id == "3"
    assert third.weight == 7.0710678118654755

    # Test Node hash
    visited = set()
    visited.add(first)
    assert first in visited

    # Test MST build
    nodelist = readTSP("test.tsp")
    nodes = dict(zip([node.id for node in nodelist], nodelist))

    test_graph = Graph(nodelist)
    mst, cost = test_graph.build_MST()
    assert cost == 120.18410376299617, "Cost has not been calculated correctly"
    assert len(mst) == 9, "Not the right number of edges in MST"

    # Test adjacency list build
    test_graph.populate()
    assert len(test_graph.adjlist) == 10, "Not all nodes included in MST"
    assert all(test_graph.adjlist), "Disconnected graph"

    # Test odd vertices finding
    odd_vertices = odd_degree_vertices(test_graph)
    assert ({"1", "8", "9", "10"} & set(odd_vertices)) == {"1", "8", "9", "10"} 
    # Load nodes for perfect matching. Don't need edges for the next algo
    odd_verts_graph = Graph([nodes[vertid] for vertid in odd_vertices]) 

    # Find min-weight perfect matches between odd vertices 
    matches, mincost = perfect_matching(odd_verts_graph)

    # Combine the mst and matches graphs so we always have 0 or 2 odd vertices
    combined_edgelist = [edge for edge in test_graph.mst] + [edge for edge in matches]
    combined_graph = Graph(nodelist)
    combined_graph.populate(combined_edgelist)

    # Get the odd vertices here to check where we need to start and end (or if the entire thing is already a cycle)
    combined_graph_odd_verts = odd_degree_vertices(combined_graph)
    assert len(combined_graph_odd_verts) in (0, 2) 

    # Get tour as an edgelist
    tour = eulerian_tour(combined_graph, combined_edgelist, combined_graph_odd_verts)
    eul_tour = Graph(nodelist)
    eul_tour.populate(tour)
    assert len(tour) == len(nodelist)

    # Hamiltonian path between the nodes
    solution, final_cost = hamiltonian_path(eul_tour)
    assert len(solution) == len(nodelist)


if __name__ == "__main__":
    # Make sure methods are working
    test()

    nodelist = readTSP("a280.tsp")
    nodes = dict(zip([node.id for node in nodelist], nodelist))

    # Wrap full MST set of edges in a Graph and build its adjacency list
    full_MST = Graph(nodelist)
    full_MST.build_MST()
    full_MST.populate() # build adj list
    
    # Create MST from odd degree vertices to find perfect matches
    odd_verts = Graph([nodes[vertid] for vertid in odd_degree_vertices(full_MST)])
    
    # Find min-weight perfect matches between odd vertices 
    matches, mincost = perfect_matching(odd_verts)
   
    # Combine the mst and matches graphs so we always have 0 or 2 odd vertices
    combined_edgelist = [edge for edge in full_MST.mst] + [edge for edge in matches]
    combined_graph = Graph(nodelist)
    combined_graph.populate(combined_edgelist)

    # Get the odd vertices here to check where we need to start and end (or if the entire thing is already a cycle)
    combined_graph_odd_verts = odd_degree_vertices(combined_graph)
    print(combined_graph_odd_verts)

    # Get tour as an edgelist
    tour = eulerian_tour(combined_graph, combined_edgelist, combined_graph_odd_verts)
    eul_tour = Graph(nodelist)
    eul_tour.populate(tour)

    # Hamiltonian path between the nodes
    solution, final_cost = hamiltonian_path(eul_tour)
    print(final_cost)
    print(solution)




    