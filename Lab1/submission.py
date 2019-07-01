## import modules here 
import math
from collections import deque
################# Question 0 #################
import re


def myfind(s, char):
    pos = s.find(char)
    if pos == -1: # not found
        return len(s) + 1
    else:
        return pos


def next_tok(s): # returns tok, rest_s
    if s == '':
        return (None, None)
    # normal cases
    poss = [myfind(s, ' '), myfind(s, '['), myfind(s, ']')]
    min_pos = min(poss)
    if poss[0] == min_pos: # separator is a space
        tok, rest_s = s[ : min_pos], s[min_pos+1 : ] # skip the space
        if tok == '': # more than 1 space
            return next_tok(rest_s)
        else:
            return (tok, rest_s)
    else: # separator is a [ or ]
        tok, rest_s = s[ : min_pos], s[min_pos : ]
        if tok == '': # the next char is [ or ]
            return (rest_s[:1], rest_s[1:])
        else:
            return (tok, rest_s)


def str_to_tokens(str_tree):
    # remove \n first
    str_tree = str_tree.replace('\n', '')
    out = []

    tok, s = next_tok(str_tree)
    while tok is not None:
        out.append(tok)
        tok, s = next_tok(s)
    return out


def add(a, b): # do not change the heading of the function
    return a + b


################# Question 1 #################


def nsqrt(k):
    if k == 0:
        return 0
    a = round(find_root(lambda x: x**2-k, lambda x: 2*x, x_0=k))
    if a**2 > k:
        return a-1
    return a


################# Question 2 #################


# x_0: initial guess
# EPSILON: stop when abs(x - x_new) < EPSILON
# MAX_ITER: maximum number of iterations

# NOTE: you must use the default values of the above parameters, do not change them

def find_root(f, fprime, x_0=1.0, EPSILON = 1E-7, MAX_ITER = 1000): # do not change the heading of the function
    """
    >>> def f(x): return x * math.log(x) - 16.0
    >>> def fprime(x): return 1.0 + math.log(x)
    >>> x = find_root(f, fprime)
    >>> print(x)
    7.792741452820329
    >>> print(f(x))
    0.0
    """
    x = x_0
    for _ in range(MAX_ITER):
        x_new = x - f(x)/fprime(x)
        if abs(x - x_new) < EPSILON:
            return x_new
        x = x_new
    return x


################# Question 3 #################

class Tree(object):
    def __init__(self, name='ROOT', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def __repr__(self):
        return self.name

    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)


def add_chile_to_tree(tokens, index, tree):
    i = index
    last_tree = tree
    while i < len(tokens):
        if tokens[i] == '[':
            i = add_chile_to_tree(tokens, i+1, last_tree)
            continue
        if tokens[i] == ']':
            return i+1
        last_tree = Tree(tokens[i])
        tree.add_child(last_tree)
        i += 1


def make_tree(tokens):
    t = Tree(tokens[0])
    # tokens.append(']')
    add_chile_to_tree(tokens, 1, t)
    return t


def make_tree_2(tokens):
    stack = deque()
    last = r = Tree(tokens[0])
    # while i < len(tokens):
    for i in tokens[1:]:
        if i is '[':
            stack.append(last)
            continue
        if i is ']':
            stack.pop()
            continue
        last = Tree(i)
        stack[-1].add_child(last)
    return r

def max_depth(root):
    if len(root.children) == 0:
        return 1
    return 1+max(max_depth(i) for i in root.children)


str_tree = '''
1 [2 [3 4       5          ] 
   6 [7 8 [9]   10 [11 12] ] 
   13
  ]
'''


def convert(tokens):
    if len(tokens) == 0:
        return []

    if len(tokens) == 1 and tokens[0] not in '[]':
        return tokens[0]

    if tokens[0] == '[':
        tokens = tokens[1:-1]

    stack = deque()
    tree = list()
    sub_tree = list()
    print(tokens)
    for i in tokens:
        if i is '[':
            stack.append(i)
        elif i is ']':
            stack.pop()
        sub_tree.append(i)
        if len(stack) == 0:
            print(f'sub_tree: {sub_tree}')
            tree.append(convert(sub_tree))
            sub_tree.clear()
    return tree


def add_ele_to_list(tokens, index, l):
    i = index
    last_l = l
    while i < len(tokens):
        if tokens[i] == '[':
            i = add_ele_to_list(tokens, i + 1, last_l)
            continue
        if tokens[i] == ']':
            return i + 1
        last_l = list()
        l.append(tokens[i])
        l.append(last_l)
        i += 1


def make_tree_list(tokens):
    l = list(tokens[0])
    l.append(list())
    add_ele_to_list(tokens, 1, l[1])
    return l


def print_tree(root, indent=0):
    print(' ' * indent, root)
    if len(root.children) > 0:
        for child in root.children:
            print_tree(child, indent+4)
