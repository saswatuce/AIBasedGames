#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import math


# Define Class

# In[2]:


class Blocks:
    def __init__(self, content):
        self.content = content
        self.contentbkp=' '
        self.dir=[0,1,2,3]
        self.dir[0] = None # RIGHT ->
        self.dir[1] = None # Down  |
        self.dir[2] = None # Left <-
        self.dir[3] = None # UP   |
        self.toVisit = []


# Ask for MxN matrix input

# In[3]:


def askForMxN():
    L = list(range(1,10))
    R = input('Enter number of Rows you want in the matrix [1 - 9] only, Q / q to exit\n')
    while(R not in list(map(lambda x: str(x), L))):
        if R.upper() != 'Q':
             R = input('Enter number of Rows you want in the matrix [1 - 9] only, Q / q to exit\n')
        else:
            return -1, -1

    C = input('Enter number of Columns you want in the matrix [1 - 9] only, Q / q to exit\n')
    while(C not in list(map(lambda x: str(x), L))):
        if C.upper() != 'Q':
            C = input('Enter number of Columns you want in the matrix [1 - 9] only, Q / q to exit\n')
        else:
            return -1, -1
    return R, C


# Computer Prepares Maze and Blockades

# In[4]:


def initiateMaze(LL, cntr):
    R, C = askForMxN()
    if R == C == -1:
        return -1, -1
    else:
        blocker = random.sample(range(2, int(R)*int(C)-1),math.floor((int(R)*int(C)-2)*0.4))
        for i in range(int(R)):
            LC = []
            for j in range(int(C)):
                cntr += 1
                if cntr in blocker:
                    LC.append(Blocks(' '))
                else:
                    LC.append(Blocks(cntr))
            LL.append(LC)
        return LL, int(R) * int(C)


# Prepare Maze

# In[5]:


def initiateMazeSelf(LL, cntr):
    R, C = askForMxN()
    if R == C == -1:
        return -1, -1
    else:
        for i in range(int(R)):
            LC = []
            for j in range(int(C)):
                cntr += 1
                LC.append(Blocks(cntr))
            LL.append(LC)
        return LL, int(R) * int(C)


# Link Objects

# In[6]:


def linkColumns(LL):
    for RI in range(len(LL)):
        for CI in range(len(LL[RI])):
            if CI != 0:
                LL[RI][CI].dir[2] = LL[RI][CI-1]
                LL[RI][CI-1].dir[0] = LL[RI][CI]


# In[7]:


def linkRows(LL):
    for CI in range(len(LL[0])):
        for RI in range(len(LL)):
            if RI != 0:
                LL[RI][CI].dir[3] = LL[RI-1][CI]
                LL[RI-1][CI].dir[1] = LL[RI][CI]    


# Print Maze

# In[8]:


def printMaze(LL):
    for RV in LL:
        CV = []
        for j in RV:
            if j.content != ' ':
                if j.content < 10:
                    CV.append('| '+str(j.content) + '  ')
                else:
                    CV.append('| '+str(j.content) + ' ')
            else:
                CV.append('| '+str(j.content) + '  ')
        print(''.join(CV) + '|')
        print('|----'*len(CV) + '|')


# Check for No path completion

# In[9]:


def pathNoComplete(dirstack):
    empty=0
    for i in dirstack:
        empty += len(i.toVisit)
    if empty == 0:
        return True
    else:
        return False


# Check for Path Completion

# In[10]:


def pathComplete(dirstack):
    winpath = []
    for i in dirstack:
        winpath.append(i.content)
    return winpath


# Create your own blockades

# In[11]:


def askForBlockades(LL, elemCount):
    contentTemp = 0
    blocklist = list(range(1, elemCount+1))
    printMaze(LL)
    num = input('Enter the number you want to block/ unblock, number shown in the maze only, Q / q to exit\n')
    while num.upper() != 'Q':
        if num in list(map(lambda x: str(x), blocklist)):
            B = getContent(LL, int(num))
            contentTemp = B.content
            B.content = B.contentbkp
            B.contentbkp = contentTemp
            printMaze(LL)
            num = input('Enter the number you want to block/ unblock, number shown in the maze only, Q / q to exit\n')
        else:
            num = input('Entered number is not in the Maze list.\nEnter the number you want to block/ unblock, number shown in the maze only, Q / q to exit\n')
    return LL


# Search the content in the Linked List

# In[12]:


def getContent(LL, contentVar):
    for RI in range(len(LL)):
        for CI in range(len(LL[RI])):
            if LL[RI][CI].content == contentVar or LL[RI][CI].contentbkp == contentVar:
                return LL[RI][CI]


# Ask For Start and End numbers

# In[13]:


def askForStEnd(elemCount, LL):
    St = End = 0
    blocklist = []
    
    for RI in range(len(LL)):
        for CI in range(len(LL[RI])):
            if LL[RI][CI].content != ' ':
                blocklist.append(LL[RI][CI].content)

    num = input('Enter the number you want the rat to START on the Maze, number shown in the maze only, Q / q to exit\n')
    while num.upper() != 'Q':
        if num in list(map(lambda x: str(x), blocklist)):
            St = num
            break
        else:
            num = input('Enter the number you want the rat to START on the Maze, number shown in the maze only, Q / q to exit\n')

    num = input('Enter the number you want the rat to STOP on the Maze, number shown in the maze only, Q / q to exit\n')
    while num.upper() != 'Q':
        if num in list(map(lambda x: str(x), blocklist)):
            End = num
            break
        else:
            num = input('Enter the number you want the rat to STOP on the Maze, number shown in the maze only, Q / q to exit\n')
    
    return St, End


# Push Directions to Stack and find a path

# In[164]:


def dirtoStack(NB, d, path, pathContent, END): # send 0 for the start
    if d > 1:
        d -= 2
    else:
        d += 2
        
    if NB not in path:
        L = [d]
        L.extend(list({0, 1, 2, 3}.difference({d})))
        NB.toVisit=[]
        for i in L:
            if NB.dir[i] != None:
                if NB.dir[i].content != ' ':
                    NB.toVisit.append(i) # visited contains directions
    
    path.append(NB)
    pathContent.append(NB.content)
    if NB.content in pathContent:
            del pathContent[pathContent.index(NB.content)+1:len(pathContent)]
    
    if pathNoComplete(path) or len(NB.toVisit) == 0: # path contains linkedLists
        print('There is no path to the End of the Maze')
        return -1
    elif NB.content == int(END):
        print('The path to the End of the Maze is found as:')
        print(pathContent)
        return 1
    else:
        currdir = NB.toVisit.pop() # direction 0,1,2,3
        currpath = NB.dir[currdir]  # path contains the linked list
        
        return dirtoStack(currpath, currdir, path, pathContent, END)
    


# Main Function

# In[166]:


cntr = 0
LL = []

C = input('Welcome to the Rat on Maze an AI based program.\nDo you want to design the Maze yourself (type 1) or let computer do it (type anything else)?')
if C == str(1):
    LL1, elemCount = initiateMazeSelf(LL, cntr)
    if LL1 == elemCount == -1:
        print('No problem, exiting....')
    else:
        LL1 = askForBlockades(LL1, elemCount)
        St, End = askForStEnd(elemCount, LL1)
else:
    LL1, elemCount = initiateMaze(LL, cntr)
    if LL1 == elemCount == -1:
        print('No problem, exiting....')
    else:
        printMaze(LL1)
        St, End = askForStEnd(elemCount, LL1)
    
# Start processing

if St == 0 or End == 0:
    print('No problem, exiting....')
else:
    linkColumns(LL1)
    linkRows(LL1)
    path = []
    pathContent = []
    startBlock = getContent(LL1, int(St))
    path.append(startBlock)
    for i in [0, 1, 2, 3]:
            if startBlock.dir[i] != None:
                if startBlock.dir[i].content != ' ':
                    startBlock.toVisit.append(i)
    curdir = startBlock.toVisit.pop()
    pathContent.append(startBlock.content)
    if input('Ready to reveal the path? type Y/ y or anything else to quit the show:  \n').upper() == 'Y':
        dirtoStack(startBlock.dir[curdir], curdir, path, pathContent, End)
    else:
        print('No problem, exiting....')

exiter = input('type any key to exit\n')
exit

