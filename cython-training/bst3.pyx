import time

cdef int TREE_SIZE = 99999999
cdef int tree[200000000] # globals are zero initialized

cdef root(int key):
    if tree[1] != 0:
        return -1
    else:
        tree[1] = key
    return 0

cdef set_left(int key, int parent):
    if tree[parent] == 0:
        return -1
    else:
        tree[(parent * 2)] = key
    return 0

cdef set_right(int key, int parent):
    if tree[parent] == 0:
        return -1
    else:
        tree[(parent * 2) + 1] = key
    return 0

cdef create():
    root(1)
    cdef int i = 0
    for i in range(1, TREE_SIZE+1):
        set_left((2*i), i)
        set_right((2*i + 1), i)
    return 0

cdef search():
    for item in tree:
        if item == 199999999:
            return 1
    return 0

def run():
    start = time.time()
    create()
    search()
    end = time.time()
    print("BST3, time spent: %.6f s" % (end - start))
