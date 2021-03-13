
#include <bits/stdc++.h>
#include <time.h>

int TREE_SIZE = 99999999;
int tree[200000000] = { 0 };

int root(int key)
{
    if(tree[1] != 0)
    {
        return -1;
    }
    else
    {
        tree[1] = key;
    }
    return 0;
}
 
int set_left(int key, int parent)
{ 
    if(tree[parent] == 0)
    {
        return -1;
    }
    else
    {
        tree[(parent * 2)] = key;
    }
    return 0;
}
 
int set_right(int key, int parent)
{
    if(tree[parent] == 0)
    {
        return -1;
    }
    else
    {
        tree[(parent * 2) + 1] = key;
    }
    return 0;
}
 
int create()
{
    root(1);
    for(int i = 1; i < TREE_SIZE+1; i++)
    {
        set_left(2*i, i);
        set_right(2*i + 1, i);
    }
    return 0;
}

int search()
{
    for(int i = 0; i < TREE_SIZE+1; i++)
    {
        if(tree[i] == 199999999)
        {
            return 1;
        }
    }
    return 0;
}

int main()
{
    clock_t begin = clock();

    create();
    search();

    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    std::cout << "BST4, time spent: " << time_spent << " s" << std::endl;

    return 0;
}
 