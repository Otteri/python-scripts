import time

TREE_SIZE = 99999999
tree = [None] * 200000000
 
def root(key):
    if tree[1] != None:
        return -1
    else:
        tree[1] = key
    return 0

def set_left(key, parent):
    if tree[parent] == None:
        return -1
    else:
        tree[(parent * 2)] = key
    return 0

def set_right(key, parent):
    if tree[parent] == None:
        return -1
    else:
        tree[(parent * 2) + 1] = key
    return 0

def create():
    root(1)
    for i in range(1, TREE_SIZE+1):
        set_left((2*i), i)
        set_right((2*i + 1), i)    

def search():
    for item in tree:
        if item == 199999999:
            return 1

if __name__ == "__main__":
    start = time.time()
    create()
    search()
    end = time.time()
    print("BST1, time spent: %.6f s" % (end - start))
