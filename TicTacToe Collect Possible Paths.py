#!/usr/bin/env python
# coding: utf-8

# Create the class Surfer

# In[1]:


class Surfer:
    def __init__(self, array = None, prev = None, next = None):
        self.array = array
        self.stack = array.copy()
        self.pos = 0
        self.Eiop = 0
        self.prev = prev
        self.next = next


# Pop Stack and Remove it from the Array

# In[2]:


def popStackAndRemoveFromArray(B):
    array1 = B.array.copy()
    B.Eiop = B.stack.pop()
    array1.remove(B.Eiop)
    return B, array1


# Create node and use the popped element

# In[3]:


def createAndAddNode(B, array):
    NB = Surfer(array)
    NB.pos = B.pos + 1
    B.next = NB
    NB.prev = B
    return NB


# Traverse to the End and collect the Elements in Operation (Eiop)

# In[4]:


def gatherEiops(H, L, A):
    if H == L:
        A.insert(len(A), H.Eiop)
        return A
    else:
        A.insert(len(A), H.Eiop)
        return gatherEiops(H.next, L, A)


# Collect all the Eiop(s) and push to a matrix

# In[5]:


def InsEiopMatrix(H, pathMatrix):
    H1, array2Push = gatherEiops(H, np.array([0]))
    array2Push1 = np.delete(array2Push, 0)
    array2Push = np.delete(array2Push1, len(array2Push1)-1)
    retPathMatrix = np.append(pathMatrix, np.array([array2Push]), axis = 0)
    return retPathMatrix


# Search and Delete Nodes whose stacks are empty

# In[6]:


def searchAndDeleteEmptyStack(L):
    if len(L.stack) != 0:
        return L
    elif L.prev == None:
        return L
    else:
        lPrev = L.prev
        lPrev.next = None
        del L
        return searchAndDeleteEmptyStack(lPrev)


# Traverse to the End

# In[7]:


def go2End(H):
    if H.next == None:
        return H
    else:
        return go2End(H.next)


# Build a branch

# In[8]:


def buildABranch(H, a2c):
    if len(H.array) == 0:
        return H, 0
    else:
        B, array = popStackAndRemoveFromArray(H)
        if len(a2c) - 1 >= H.pos:
            a2c[H.pos] = H.Eiop
            A1 = a2c
        else:
            a2c.insert(len(a2c), H.Eiop)
        
    if scanAllWinPaths(WinPaths, a2c) == 1:
        return B, 1
    elif scanAllWinPaths(WinPaths, a2c) == 2:
        return B, 2
    else:
        NB = createAndAddNode(B, array)
        return buildABranch(NB, a2c)


# Scan all through all the Winning paths and check if the current path holds any of them

# In[9]:


def scanAllWinPaths(WinPaths, Path): # oe 0 for 1st mover, 1 for 2nd mover
    for wPath in WinPaths:
        if listFound(wPath, prepList(Path, 0)):
            return 1
        elif listFound(wPath, prepList(Path, 1)):
            return 2
    return 0


# WinPaths = [[1,2,3],
#             [4,5,6],
#             [7,8,9],
#             [1,4,7],
#             [2,5,8],
#             [3,6,9],
#             [1,5,9],
#             [3,5,7]]
# 
# scanAllWinPaths(WinPaths, [1,2,9,3,5,4,6,7,8])

# Prepare the List to be searched

# In[10]:


def prepList(A, oe): # oe 0 for 1st mover, 1 for 2nd mover
    retLst = []
    for i in range(len(A)):
        if oddEven(i) == oe:
            retLst.append(A[i])
    return retLst


# List found in Array?

# In[11]:


'''    f = 0
    for item in l:
        if item in nda:
            f += 1
    if f == 3:
        return 1
    else:
        return 0
'''
def listFound(l, nda):
    if set(l) & set(nda) == set(l):
        return 1
    else:
        return 0


# Odd or Even

# In[12]:


def oddEven(n):
    if n == 0 or n%2 == 0:
        return 0 # return if EVEN
    else:
        return 1 # return if ODD


# Import Libraries

# In[13]:


import time


# # Oponent has the 1st MOVE - Take Odd positions (0 occupies 0th position)
# 
# Create the Surfer object

# ##### 1. Straight line paths
# 2. Initiate paths

# In[14]:


WinPaths = [[1,2,3],
            [4,5,6],
            [7,8,9],
            [1,4,7],
            [2,5,8],
            [3,6,9],
            [1,5,9],
            [3,5,7]]

head = Surfer([9,8,7,6,5,4,3,2,1])
pathMatrix = []
lastGen = go2End(head)
array2Col = []


# Evaluate Paths

# In[15]:


ts1 = time.time()
with open('TicTacToePaths.txt', 'w') as f:
    f.write('paths' + "\t" + 'winner' + "\t" + 'count' + "\r")
    while len(lastGen.stack) > 0:
        last, mover = buildABranch(lastGen, array2Col)
        f.write("%s" % ''.join([str(elem) for elem in array2Col]) + "\t" + "%s" % mover + "\t" + str(len(array2Col)) + "\r")
        pathMatrix.insert(len(pathMatrix), array2Col)
        LU = searchAndDeleteEmptyStack(last)
        array2Col = gatherEiops(head, LU, [])
        lastGen = go2End(head)

ts2 = time.time()
print(f' Execution time {(ts2 - ts1)/60} min(s)')


# Read possible paths to the Pandas df

# In[16]:


#possiblePaths = pd.read_csv('C:/Users/SaswatSahoo/Downloads/Python/TicTacToePaths.txt', sep='\t', lineterminator='\r')


# In[17]:


#possiblePaths

