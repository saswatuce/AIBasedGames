#!/usr/bin/env python
# coding: utf-8

# In[1]:


print('Please be patient while Pandas being loaded, depends on your machine configuration.....')


# Import libraries

# In[2]:


import pandas as pd
import re
import random


# Read the Possible Paths

# In[3]:


possiblePaths = pd.read_csv('TicTacToePaths.txt', sep='\t', lineterminator='\r')


# Draw TicTacToe board

# In[4]:


def initTTTB():
    TTTB= ([
        [' 1 ', '|', ' 2 ', '|', ' 3 '],
        ['---', '|', '---', '|', '---'],
        [' 4 ', '|', ' 5 ', '|', ' 6 '],
        ['---', '|', '---', '|', '---'],
        [' 7 ', '|', ' 8 ', '|', ' 9 ']
        ])
    return TTTB


# Choose your Mark and Move

# In[5]:


def markMove():
    markL = ['x', 'X', 'o', 'O']
    moveL = ['1', '2']
    
    mark = input('\n1. Chose your mark(x / o) or (q / Q) to quit:  ')
    while mark not in markL:
        if mark == 'q' or mark == 'Q':
            return -1, -1
        else:
            mark = input('\n1. Chose your mark(x / o) or (q / Q) to quit:  ')
            
    move = input('2. Enter 1 to move first or 2 to move second:  ')
    while move not in moveL:
        if move == 'q' or move == 'Q':
            return -1, -1
        else:
            move = input('2. Enter 1 to move first or 2 to move second:  ')
    return mark.upper(), move


# Choose the position for each move

# In[6]:


def Choice():
    choiceL = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            
    choice = input('Press the digit (NOT marked) you want to mark(1-9 ONLY) or (q / Q) to quit:  ')
    while choice not in choiceL:
        if choice == 'q' or choice == 'Q':
            return -1
        else:
            choice = input('Press the digit (NOT marked) you want to mark(1-9 ONLY) or (q / Q) to quit:  ')       
    return choice


# Assign the mark on the board

# In[7]:


def assignTTTB(TTTB, mark, choice):
    for lists in TTTB:
        if ' ' + choice + ' ' in lists:
            lists[lists.index(' ' + choice + ' ')] = ' ' + mark + ' '
            return 1
    print('oops. The choice is already taken')
    return -1


# Show the board

# In[8]:


def showTTTB(TTTB):
    for item in TTTB:
        print(''.join(item))


# Initialize the parameters

# In[9]:


def Init(mark, move, TTTB, runningPath):
    
    if mark == 'X':
        markC = 'O'
    else:
        markC = 'X'
    
    if move == '1':
        moveC = '2'
        return runOponent(mark, move, markC, moveC, TTTB, runningPath)
    else:
        moveC = '1'
        return runAI(mark, move, markC, moveC, TTTB, runningPath)


# Interface for Opponent (Human)

# In[10]:


def runOponent(mark, move, markC, moveC, TTTB, runningPath):
    print(f'\nPlayer {move} , your mark is {mark}')
    choice = Choice()
    if choice == -1:
        return -1
    else:
        AV = assignTTTB(TTTB, mark, choice)
        while(AV == -1):
            print(f'\nPlayer {move} :')
            choice = Choice()
            if choice == -1:
                return -1
            AV = assignTTTB(TTTB, mark, choice)
        runningPath.append(choice)
        showTTTB(TTTB)
        
        winCheck = checkForWin(runningPath, move)
        if winCheck == 1:
            print('You won.! Congratulations..')
            return 1 # Person win
        elif winCheck == 0 and set(runningPath) == set(['1','2','3','4','5','6','7','8','9']):
            print('Match drawn. Well Played.')
            return 0
        else:
            runAI(mark, move, markC, moveC, TTTB, runningPath)


# Interface for AI

# In[11]:


def runAI(mark, move, markC, moveC, TTTB, runningPath):
    
    if moveC == '1' and len(runningPath) == 0:
        choice = random.choice([1, 3, 5, 7, 9])
        AV = assignTTTB(TTTB, markC, str(choice))
        runningPath.append(str(choice))
        print('\nAI''s move.....\n')
        showTTTB(TTTB)
        
    elif moveC == '2' and len(runningPath) == 1:
        print('pls wait, calculating AI''s move for the first time.........')
        fstMove = possiblePaths[possiblePaths['paths'].apply(lambda row: re.match(''.join(runningPath), str(row))).notna()]
        fstMove_flag = pd.concat([fstMove,fstMove['paths'].apply(lambda row: scanApath(row, move, moveC)).copy()], axis = 1) 
        fstMove_flag.columns = ['paths', 'winner', 'count', 'flag']
        choice = getNxtMove(fstMove_flag, runningPath, move, moveC)
        AV = assignTTTB(TTTB, markC, str(choice))
        runningPath.append(str(choice))
        print('\nAI''s move.....\n')
        showTTTB(TTTB)
    
    else:
        fstMove = possiblePaths[possiblePaths['paths'].apply(lambda row: re.match(''.join(runningPath), str(row))).notna()]
        fstMove_flag = pd.concat([fstMove,fstMove['paths'].apply(lambda row: scanApath(row, move, moveC)).copy()], axis = 1) 
        fstMove_flag.columns = ['paths', 'winner', 'count', 'flag']
        choice = getNxtMove(fstMove_flag, runningPath, move, moveC)
        AV = assignTTTB(TTTB, markC, str(choice))
        runningPath.append(str(choice))
        print('\nAI''s move.....\n')
        showTTTB(TTTB)

    winCheck = checkForWin(runningPath, moveC)
    if winCheck == 1:
        print('AI won.! Better luck next time..')
        return 1 # AI win
    elif winCheck == 0 and set(runningPath) == set(['1','2','3','4','5','6','7','8','9']):
        print('Match drawn. Well Played.')
        return 0
    else:
        runOponent(mark, move, markC, moveC, TTTB, runningPath)


# Scan A Path

# In[12]:


def scanApath(path, mover, moverC):
    pathStr = list(map(lambda x: int(x), str(path)))
    flag = 0
###################################    
    if mover == '2':
        move = mover
    else:
        move = moverC
###################################        
    for pathIndex in list(range(len(pathStr))):
        pathPart = pathStr[:pathIndex+1]
         
        oddPath = list(map(lambda n: int(pathPart[n]), list(filter(lambda x: int(x) != 0 and int(x)%2 != 0, range(len(pathPart))))))
        evenPath = list(map(lambda n: int(pathPart[n]),list(filter(lambda x: int(x) == 0 or int(x)%2 == 0,range(len(pathPart)))))) 
        
###################################
        winCheck = checkForWin(pathPart, mover)
        winCheckC = checkForWin(pathPart, moverC)
        
        if winCheck == 1 or winCheckC == 1:
            break
        elif winCheck == 0 and set(pathPart) == set([1,2,3,4,5,6,7,8,9]):
            break        
###################################
        if len(pathPart) < 3:
            move = updateMove(move)
            continue
###################################
        if move == moverC:
            OpntNxtMove = moverFor3rdPos(evenPath, oddPath, mover)
            AINxtMove = moverFor3rdPos(evenPath, oddPath, moverC)
            if len(AINxtMove) == 1 and AINxtMove[0] == pathStr[pathIndex + 1]:
                flag = 4
                move = updateMove(move)
                continue
            elif len(OpntNxtMove) == 1 and OpntNxtMove[0] == pathStr[pathIndex + 1]:
                flag = 5
                move = updateMove(move)
                continue
            elif len(AINxtMove) == 1 and AINxtMove[0] > -1: # AI's st.line move is possible
                flag = 3
                break
            elif len(OpntNxtMove) == 2: # If Opponent has a chance to double win
                flag = 1
                break  
            elif len(AINxtMove) == 2: #AI has a chance to double win?
                flag = 2
                break
            elif len(AINxtMove) == 1 and AINxtMove[0] == -1: # No other st.line move possible for AI
                flag = 6
                break
            elif len(OpntNxtMove) == 1 and OpntNxtMove[0] not in [pathStr[pathIndex + 1], -1, -2]:
                break
            else:
                flag = 7
                move = updateMove(move)
###################################

        else:
            OpntNxtMove = moverFor3rdPos(evenPath, oddPath, mover)
            AINxtMove = moverFor3rdPos(evenPath, oddPath, moverC)
            if len(AINxtMove) == 1 and AINxtMove[0] == pathStr[pathIndex + 1]: # AI can take the last position of the stline?
                flag = 4
                move = updateMove(move)
                continue
            elif len(OpntNxtMove) == 1 and OpntNxtMove[0] == pathStr[pathIndex + 1]: # Opnt can take the last position of the stline?
                flag = 5
                move = updateMove(move)
                continue
            elif len(OpntNxtMove) == 2: # If Opponent has a chance to double win
                flag = 1
                break
            elif len(AINxtMove) == 2: #AI has a chance to double win?
                flag = 2
                break
            else:
                flag = 7
                move = updateMove(move)         
    return flag


# Update Move

# In[13]:


def updateMove(move):
    if move == '1':
        return '2'
    else:
        return '1'


# Move for 3rd Position

# In[14]:


def moverFor3rdPos(evenPath, oddPath, move):
    L=[]
    flag = 0
    if move == '1':
        for winpath in WinPaths:
            if len(set(winpath).difference(set(evenPath))) == 1 and list(set(winpath).difference(set(evenPath)))[0] not in oddPath:
                L.extend(list(set(winpath).difference(set(evenPath))))
                flag = 1
            elif flag != 1 and len(set(winpath).difference(set(evenPath))) == 1 and list(set(winpath).difference(set(evenPath)))[0] in oddPath:
                flag = 2
    else:
        for winpath in WinPaths:
            if len(set(winpath).difference(set(oddPath))) == 1 and list(set(winpath).difference(set(oddPath)))[0] not in evenPath:
                L.extend(list(set(winpath).difference(set(oddPath))))
                flag = 1
            elif flag != 1 and len(set(winpath).difference(set(oddPath))) == 1 and list(set(winpath).difference(set(oddPath)))[0] in evenPath:
                flag = 2
    if flag == 1:
        return L
    elif flag == 2:
        return [-2]
    else:
        return [-1]


# Check for Win

# In[15]:


def checkForWin(runningPath, move):
    if move == '1': # Second Mover
        if list(filter(lambda path: set(path).issubset(set(list(map(lambda n: int(runningPath[n]),
                                                                    list(filter(lambda x: int(x) == 0 or int(x)%2 == 0, 
                                                                                range(len(runningPath)))))))), WinPaths)) == []:
            return 0
        else:
            return 1
    else: # First Mover
        if list(filter(lambda path: set(path).issubset(set(list(map(lambda n: int(runningPath[n]),
                                                                    list(filter(lambda x: int(x) != 0 and int(x)%2 != 0, 
                                                                                range(len(runningPath)))))))), WinPaths)) == []:
            return 0
        else:
            return 1


# Get Next Move

# In[16]:


def getNxtMove(fstMove_flag, result, mover, moverC):
    flag_1 = []
    flag_2 = [] 
    flag_3 = []
    flag_4 = []
    flag_5 = []
    flag_6 = []
    flag_7 = []

    oddPath = list(map(lambda n: int(result[n]), list(filter(lambda x: int(x) != 0 and int(x)%2 != 0, range(len(result))))))
    evenPath = list(map(lambda n: int(result[n]),list(filter(lambda x: int(x) == 0 or int(x)%2 == 0,range(len(result)))))) 
    OpntNxtMove = moverFor3rdPos(evenPath, oddPath, mover)
    AINxtMove = moverFor3rdPos(evenPath, oddPath, moverC)

    for flag in (1, 2, 3, 4, 5, 6, 7):
        for i in list(set(['1', '2', '3', '4', '5', '6', '7', '8', '9']).difference(set(result))):
            cnt = len(fstMove_flag[(fstMove_flag['paths'].apply(lambda row: False if len(str(row)) <= len(result) 
                                                                else str(row)[len(result)] == i)) 
                                   & (fstMove_flag['flag'] == flag)])
            if flag == 1 and cnt == 0:
                flag_1.append(i)
            elif flag == 2 and cnt > 0:
                flag_2.append(i)
            elif flag == 3 and cnt > 0:
                flag_3.append(i)
            elif flag == 4 and cnt > 0:
                flag_4.append(i)
            elif flag == 5 and cnt > 0:
                flag_5.append(i)
            elif flag == 6 and cnt > 0:
                flag_6.append(i)
            elif flag == 7 and cnt > 0:
                flag_7.append(i)

    if len(AINxtMove) == 1 and AINxtMove[0] > -1:
        return AINxtMove[0]
    elif len(OpntNxtMove) == 1 and OpntNxtMove[0] > -1:
        return OpntNxtMove[0]
    elif len(flag_1) == 1:
        return flag_1[0]
    elif checkFlag(flag_2, AINxtMove, OpntNxtMove) != 0:
        return checkFlag(flag_2, AINxtMove, OpntNxtMove)
    elif checkFlag(flag_3, AINxtMove, OpntNxtMove) != 0:
        return checkFlag(flag_3, AINxtMove, OpntNxtMove)
    elif checkFlag(flag_4, AINxtMove, OpntNxtMove) != 0:
        return checkFlag(flag_4, AINxtMove, OpntNxtMove)
    elif checkFlag(flag_5, AINxtMove, OpntNxtMove) != 0:
        return checkFlag(flag_5, AINxtMove, OpntNxtMove)
    elif checkFlag(flag_6, AINxtMove, OpntNxtMove) != 0:
        return checkFlag(flag_6, AINxtMove, OpntNxtMove)
    elif checkFlag(flag_7, AINxtMove, OpntNxtMove) != 0:
        return checkFlag(flag_7, AINxtMove, OpntNxtMove)


# Check Flag

# In[17]:


def checkFlag(flagList, AINxtMove, OpntNxtMove):
    if len(flagList) > 1:
        evaltr = 0
        for pos in flagList:
            if (len(AINxtMove) == 1 and AINxtMove[0] == int(pos)) or (len(OpntNxtMove) == 1 and OpntNxtMove[0] == int(pos)):
                evaltr = 1
                return pos
        if evaltr == 0:
            return random.choice(flagList)
    elif len(flagList) == 1:
        return flagList[0]
    else:
        return 0


# Callable Main Program

# In[27]:


def main():
    TTTB = initTTTB()
    showTTTB(TTTB)
    runningPath = []
    print('\nWelcome to the Tic Tac Toe.\nFirst chose your mark (x / o).\nThen chose whether you want to move first or second.\nThen press the digit (NOT marked) from 1 - 9, where you want to place the mark\n')

    mark, move = markMove()

    if -1 in [mark, move]:
        print('\nNo Problem.! You didnt want to play anymore')
        return -1

    else:
        retval = Init(mark, move, TTTB, runningPath)
        return retval


# Calling Main program

# In[30]:


WinPaths = [[1,2,3],
            [4,5,6],
            [7,8,9],
            [1,4,7],
            [2,5,8],
            [3,6,9],
            [1,5,9],
            [3,5,7]]

play = 'a'
while(play.upper() != 'Q'):
    mainReturn = main()
    if mainReturn != -1:
        play = input('Do you want to play further? Just press Enter\nPress Q / q to exit: ')
    else:
        play = 'q'

