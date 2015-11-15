# ! /usr/bin/env python3
from sys import stdin
import collections
import copy


def get_root(graph):
    the_root = None
    for g in graph:
        if graph.get(g)[1] == '_':
            the_root = g
            break
    else:
         the_root = None
    return the_root

def levelorder(graph, root):
    q = collections.deque()
    q.appendleft(root)
    lst = []
    while len(q) != 0:
        removed = q.pop()
        lst.append(removed)
        visit = removed
        if graph.get(visit)[2] != '_':
            q.appendleft(graph.get(visit)[2])
        if graph.get(visit)[3] != '_':
            q.appendleft(graph.get(visit)[3])

    return lst

def path(graph, root, k):
    k1 = None
    for g in graph:
        if graph.get(g)[0] == str(k):
            k1 = g
            break
    else:
         k1 = None
    lst = []
    temp = k1
    while temp != root:
        lst.append(temp)
        temp = graph.get(temp)[1]
    lst.append(root)
    return lst[::-1]

def rotate_right(graph, k):
    rotate = copy.deepcopy(graph)
    k1 = None
    for g in rotate:
        if rotate.get(g)[0] == str(k):
            k1 = g
            break
    else:
        k1 = None

    if rotate.get(k1)[2] == '_':
        return rotate
    else:
        left = rotate.get(k1)[2]
        if rotate.get(k1)[1] == '_':
            rotate[left][1] = '_'
        elif rotate[rotate.get(k1)[1]][2] == k1:
            rotate[rotate.get(k1)[1]][2] = left
        else:
            rotate[rotate.get(k1)[1]][3] = left
        rotate[left][1] = rotate[k1][1]
        rotate[k1][2] = rotate[left][3]
        if rotate[k1][2] != '_':
            rotate[rotate.get(k1)[2]][1] = k1
        rotate[left][3] = k1
        rotate[k1][1] = left
    return rotate

def find_min(graph, k):
    if graph[k][2] == '_':
        return k
    else:
        return find_min(graph, graph[k][2])

def transplant(trans, u, v):
    # trans = copy.deepcopy(graph)
    if trans[u][1] == '_':
        trans[v][1] = '_'
    elif trans[trans.get(u)[1]][2] == u:
        trans[trans.get(u)[1]][2] = v
    else:
        trans[trans.get(u)[1]][3] = v
    if v != '_':
        trans[v][1] = trans[u][1]
    return trans

def tree_delete(graph, k1):
    del_tree = copy.deepcopy(graph)
    z = None
    for g in del_tree:
        if del_tree.get(g)[0] == str(k1):
            z = g
            break
    else:
        z = None
    if del_tree[z][2] == '_':
        transplant(del_tree, z, del_tree[z][3])
    elif del_tree[z][3] == '_':
        transplant(del_tree, z, del_tree[z][2])
    else:
        y = find_min(del_tree, del_tree[z][3])
        if del_tree[y][1] != z:
            transplant(del_tree, y, del_tree[y][3])
            del_tree[y][3] = del_tree[z][3]
            del_tree[del_tree.get(y)[3]][1] = y
        transplant(del_tree, z, y)
        del_tree[y][2] = del_tree[z][2]
        del_tree[del_tree.get(y)[2]][1] = y
    return del_tree

def tree_insert(graph, z):
    ins_tree = copy.deepcopy(graph)
    ins_tree['in'] = [str(z), 'foo', '_', '_']
    x = get_root(ins_tree)
    y = '_'
    while x != '_':
        y = x
        if int(ins_tree['in'][0]) < int(ins_tree[x][0]):
            x = ins_tree[x][2]
        else:
            x = ins_tree[x][3]
    ins_tree['in'][1] = y
    if y == '_':
        ins_tree['in'][1] = '_'
    elif int(ins_tree['in'][0]) < int(ins_tree[y][0]):
        ins_tree[y][2] = 'in'
    else:
        ins_tree[y][3] = 'in'
    return ins_tree

for line in stdin:
# line = "11 9 2 13 _, 4 18 2 14 _, 2 10 _ 11 4, 14 16 4 _ _, 13 0 11 _ _ | 10 | 7"
# line = "16 17 _ 1 19, 10 1 1 13 _, 19 19 16 _ _, 13 0 10 _ _, 1 11 16 10 _ | 0 | 3"
# line = "43 42 34 29 15, 41 7 11 28 _, 34 8 _ 11 43, 11 4 34 _ 41, 28 5 41 _ _, 29 41 43 14 _, 14 39 29 _ _, 15 47 43 _ _ | 41 | 37"
    A = [elem.strip() for elem in line.split("|")]

    temp = [elem.split() for elem in A[0].split(",")]
    k1 = int(A[1])
    k2 = int(A[2])

    graph = {d[0]: d[1:] for d in temp}
    g1 = levelorder(graph, get_root(graph))
    p = path(graph, get_root(graph), k1)
    # print int(graph.get(get_root(graph))[0])
    # print "The Searchpath is: ", searchpath(graph, get_root(graph), k1)

    rotated_tree = rotate_right(graph, k1)
    g2 = levelorder(rotated_tree, get_root(rotated_tree))
    deleted_tree = tree_delete(rotated_tree, k1)
    g3 = levelorder(deleted_tree, get_root(deleted_tree))
    inserted_tree = tree_insert(deleted_tree, k2)
    g4 = levelorder(inserted_tree, get_root(inserted_tree))

    print(', '.join([' '.join(g1), '-'.join(p), ' '.join(g2), ' '.join(g3), ' '.join(g4)]))







