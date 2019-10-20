from Graph import *
from random import randrange, sample, choice


def rand_path(nodes):
    pool = list(nodes)
    random_path = []

    # Random start
    start = rand_pop(pool)
    currn = start

    while len(pool) > 1:
        nextn = rand_pop(pool)
        random_path.append(Edge(currn, nextn))
        currn = nextn

    # Complete cycle
    random_path.append(Edge(currn, start))
    return random_path

def rand_pop(l: list):
    """ Get a random element from list and remove it at the same time, efficiently """
    i = randrange(len(l)) 
    l[i], l[-1] = l[-1], l[i]    
    return l.pop()   

def rand_seg(path: Path):
    start, end = sample(path.nodes, 2)
    return (path.segment(start, end), start, end)

def reverse_transform(seg: Path, origPath: Path, start: Node, end: Node) -> Path:
    reversed_seg = seg.reverse()
    print("\nREVERSED")
    print(reversed_seg)
    transform = []
    currn = origPath.path[0].n1
    print(f"\ncurrn: {currn}, start: {end}")
    # If segment doesn't start at beginning
    if currn != end:
        # Add the left side
        while origPath.next_edge(currn).n2 != end:
            print("ADDING")
            print(origPath.next_edge(currn))
            transform.append(origPath.next_edge(currn))
            currn = origPath.adjlist[currn][0]
        # Join to new reversed seg
        transform.append(Edge(currn, reversed_seg.path[0].n1))

    # Add reversed seg
    transform.extend(reversed_seg.path)

    print(transform)

    

def rand_transform(seg, path, start, end):
    if choice([0, 1]):
        reverse = reverse_transform(seg, path, start, end)
    else:
        transport = path.transport()

if __name__ == "__main__":
    nodelist = readTSP("test.tsp")
    nodes = dict(zip([node.id for node in nodelist], nodelist))

    # Initial path is random
    init_path: List[Edge] = rand_path(nodelist)

    path = Path(init_path)

    print(path)

    seg, start, end = rand_seg(path)
    print("\nSEG")
    print(seg)

    reverse_transform(seg, path, start, end)