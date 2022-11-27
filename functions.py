import random

# generate random numbers for the cells
def rand():
    irand = random.randint(0,3)
    return irand

# for each round, randomly insert to an empty cell, and make it equals 2
def rand_for_each_round(n_matrix):
    r_row = rand()
    r_col = rand()
    while n_matrix[r_row][r_col] != 0: # avoid replacing the existing cell
        r_row = rand()
        r_col = rand()
        if n_matrix[r_row][r_col] == 0:
            n_matrix[r_row][r_col] = 2
            return n_matrix
    n_matrix[r_row][r_col] = 2
    return n_matrix

# call this function to create the matrix
def createOriginalMatrix():
    matrix = []
    for i in range(4):
        matrixs = []
        for j in range(4):
            x = 0
            matrixs.append(x)
        matrix.append(matrixs) # append to the matrix
    # initialize first 2 random cell at the beginning
    fnS_row = rand()
    fnS_col = rand()
    matrix[fnS_row][fnS_col] = 2
    snF_row = rand()
    snF_col = rand()
    while snF_row == fnS_row and snF_col == fnS_col: # make sure there must be 2 valued cell
        snF_row = rand()
        snF_col = rand()
    matrix[snF_row][snF_col] = 2
    # # test case to test the edge cases
    # matrix[0][0], matrix[0][1], matrix[0][2], matrix[0][3] = 8, 4, 4, 4
    # matrix[1][0], matrix[1][1], matrix[1][2] = 4, 2, 2
    # matrix[2][0], matrix[2][1] = 4, 2 # test case sample
    for x in range(4):
        print(matrix[x])
    return matrix

# get action from user
# 2 ways:
#       either while loop to get the correct choice
#       or using the try/except
def getUsersInput():
    # str_move = input(f'press "w", "s", "a", "d" to make a move: ("q" to quit)')
    # while str_move not in 'wsadq': # avoid the invalid inputs
    #     str_move = input(f'wrong button\npress "w", "s", "a", "d" again to make a move: ("q" to quit)')
    while True:
        try:
            str_move = input(f'press "w", "s", "a", "d" to make a move: ("q" to quit)')
            if str_move in 'asdwq':
                break
        except TypeError:
            continue
        except EOFError:
            continue
    return str_move

# ask users if they want to try again when they lose
def lose(b_ifWin):
    if b_ifWin: # input for win
        str_lose = input(f'victory! take another shot? (y/any other keys)')
    else: # input for lose
        str_lose = input(f'you reached the deadend, try again? (y/any other keys)')
    return str_lose


# make the move action
# logic:
#       left&up('a'&'w') in a same method, which is tracked the cells under ascending order
#       right&down('d'&'s') in a descending order, reversed tracking as above
def movements(m_matrix, s_move):
    # move left
    if s_move == 'a':
        left_bigAdd = [] # store the coordinate of the manipulated cell
        for ileft in range(4): # row
            for jleft in range(1,4): # since it's horizontal move, from right to left, loop from 2nd to the last col
                if m_matrix[ileft][jleft] != 0: # first check if curr cell is 0
                    b_ifAdd = False # make a boolean for each horizontal cell, to check if it's manipulated
                    i_ded = 1 # a pointer in the for loop for the cells in 3rd and 4th col
                    # combined these 2 conditions to save lines
                    if m_matrix[ileft][jleft-i_ded] == m_matrix[ileft][jleft] or m_matrix[ileft][jleft-i_ded] == 0: # left cell
                        if m_matrix[ileft][jleft-i_ded] == m_matrix[ileft][jleft]:
                            m_matrix[ileft][jleft-i_ded] += m_matrix[ileft][jleft] # if curr cell = the left cell, add it to the left
                            b_ifAdd = True # in this row, mark the cell as manipulated
                            left_bigAdd.append([ileft, jleft-i_ded]) # append the appended cell coordination to the array
                        elif m_matrix[ileft][jleft-i_ded] == 0:
                            m_matrix[ileft][jleft-i_ded] = m_matrix[ileft][jleft] # replace the value to the left cell if left's 0
                        m_matrix[ileft][jleft] = 0 # after manipulated, make the curr cell 0
                        if jleft > 1: # need to push further to the left, not only 1 space
                            for z1 in range(1,3):
                                # keep tracking the further left cell to see whether equals
                                if m_matrix[ileft][jleft-z1-1] == 0: # if 0, replace
                                    m_matrix[ileft][jleft-z1-1] = m_matrix[ileft][jleft-i_ded]
                                    m_matrix[ileft][jleft-i_ded] = 0
                                    i_ded += 1 # pointer in this loop
                                elif m_matrix[ileft][jleft-z1-1] == m_matrix[ileft][jleft-i_ded]: # if equals
                                    if b_ifAdd or [ileft, jleft-z1-1] in left_bigAdd: break # if the coordiation been marked as manipulated, quit for the next cell
                                    else:
                                        m_matrix[ileft][jleft-z1-1] += m_matrix[ileft][jleft-i_ded] # add up to left
                                        m_matrix[ileft][jleft-i_ded] = 0
                                        b_ifAdd = True # in this row, mark the cell as manipulated
                                        i_ded += 1
                                else: break # if further left cell either not 0 or not equal to the compared cell,
                else: continue # if detected the curr cell is 0, just skip

    # move right
    # same method as the down movement, just the horizontal and vertical diffs
    # more details of the comments below in the down movement conditions part
    elif s_move == 'd':
        right_bigAdd = []
        for iright in range(4):
            for jright in range(2,-1,-1): # make the col reversely ordered
                if m_matrix[iright][jright] != 0:
                    if m_matrix[iright][jright] == m_matrix[iright][jright+1]: # right cell
                        m_matrix[iright][jright+1] += m_matrix[iright][jright]
                        m_matrix[iright][jright] = 0
                        right_bigAdd.append([iright, jright+1])
                    elif m_matrix[iright][jright+1] == 0:
                        m_matrix[iright][jright+1], m_matrix[iright][jright] = m_matrix[iright][jright], 0
                    else: continue # if the forward one is an integer that doesnt equals the curr one or 0, then skip
                    if jright <= 1:
                        if m_matrix[iright][jright+2] == m_matrix[iright][jright+1] and [iright, jright+1] not in right_bigAdd and [iright, jright+2] not in right_bigAdd:
                            m_matrix[iright][jright+2] += m_matrix[iright][jright+1]
                            m_matrix[iright][jright+1] = 0
                            right_bigAdd.append([iright, jright+2])
                        elif m_matrix[iright][jright+2] == 0:
                            if [iright, jright+1] not in right_bigAdd:
                                m_matrix[iright][jright+2], m_matrix[iright][jright+1] = m_matrix[iright][jright+1], 0
                            else: # if the curr cell is marked as added, then remove the previous stored location and add the new one
                                m_matrix[iright][jright + 2], m_matrix[iright][jright + 1] = m_matrix[iright][jright + 1], 0
                                right_bigAdd.remove([iright, jright+1])
                                right_bigAdd.append([iright, jright+2])
                        else: continue
                        if jright == 0:
                            if m_matrix[iright][jright+3] == m_matrix[iright][jright+2] and [iright, jright+2] not in right_bigAdd and [iright, jright+3] not in right_bigAdd:
                                m_matrix[iright][jright + 3] += m_matrix[iright][jright+2]
                                m_matrix[iright][jright+2] = 0
                            elif m_matrix[iright][jright+3] == 0:
                                m_matrix[iright][jright + 3], m_matrix[iright][jright + 2] = m_matrix[iright][jright + 2], 0

                            else: continue

    # move up
    # differences to the left move:
    #       from horizontal to vertical, so change the range of row and col
    #       and to make comparison between cell's row in matrix
    elif s_move == 'w':
        up_bigAdd = [] # store the coordinate of the manipulated cell
        for iup in range(1,4):  # row
            for jup in range(4):  # col
                if m_matrix[iup][jup] != 0:
                    b_ifAdd = False # boolean to check if already added
                    i_ded = 1 # track the index
                    if m_matrix[iup-i_ded][jup] == m_matrix[iup][jup] or m_matrix[iup - i_ded][jup] == 0: # upper cell
                        if m_matrix[iup-i_ded][jup] == m_matrix[iup][jup]:
                            m_matrix[iup-i_ded][jup] += m_matrix[iup][jup]
                            b_ifAdd = True
                            up_bigAdd.append([iup-i_ded, jup])
                        elif m_matrix[iup-i_ded][jup] == 0:
                            m_matrix[iup - i_ded][jup] += m_matrix[iup][jup]
                        m_matrix[iup][jup] = 0
                        if iup > 1:
                            for z1 in range(1,3): # check if the upper cells are 0
                                if m_matrix[iup-z1-1][jup] == 0:
                                    m_matrix[iup-z1-1][jup] += m_matrix[iup - i_ded][jup]
                                    m_matrix[iup-i_ded][jup] = 0
                                    i_ded += 1
                                elif m_matrix[iup-z1-1][jup] == m_matrix[iup - i_ded][jup]:
                                    if b_ifAdd or [iup-z1-1, jup] in up_bigAdd: break
                                    else:
                                        m_matrix[iup-z1-1][jup] += m_matrix[iup - i_ded][jup]
                                        m_matrix[iup - i_ded][jup] = 0
                                        b_ifAdd = True
                                        i_ded += 1
                                else:
                                    break
                    else: # when the upper one not equals tp the curr one and also not 0
                        continue

    # move down
    elif s_move == 's':
        down_bigAdd = []
        for idown in range(2,-1,-1): # make it reverse since we need to check from bottom to top, but it also works if check from top to bottom
            for jdown in range(4):
                if m_matrix[idown][jdown] != 0:
                    if m_matrix[idown][jdown] == m_matrix[idown+1][jdown]: # lower cell
                        m_matrix[idown+1][jdown] += m_matrix[idown][jdown]
                        m_matrix[idown][jdown] = 0
                        down_bigAdd.append([idown+1, jdown]) # append the coordination for manipulated cell
                    elif m_matrix[idown+1][jdown] == 0:
                        m_matrix[idown+1][jdown], m_matrix[idown][jdown] = m_matrix[idown][jdown], 0 # pass it to the lower cell
                    else: continue # if the forward one is an integer that doesnt equals the curr one or 0, then skip

                    if idown <= 1: # reversely, both 3rd and 4th cell go through it
                        # check if they are equal or not / whether they are in the coordination stored array
                        if m_matrix[idown+2][jdown] == m_matrix[idown+1][jdown] and [idown+1, jdown] not in down_bigAdd and [idown+2, jdown] not in down_bigAdd:
                            m_matrix[idown+2][jdown] += m_matrix[idown+1][jdown]
                            m_matrix[idown+1][jdown] = 0
                            down_bigAdd.append([idown+2, jdown])
                        elif m_matrix[idown+2][jdown] == 0:
                            if [idown+1, jdown] not in down_bigAdd:
                                m_matrix[idown+2][jdown], m_matrix[idown+1][jdown] = m_matrix[idown+1][jdown], 0
                            else: # if the curr cell is marked as added, then remove the previous stored location and add the new one
                                m_matrix[idown+2][jdown], m_matrix[idown+1][jdown] = m_matrix[idown+1][jdown], 0
                                down_bigAdd.remove([idown+1, jdown])
                                down_bigAdd.append([idown+2, jdown])
                        else: continue # pass if not equal or not 0
                        if idown == 0: # one more push trial for the cell at last row
                            if m_matrix[idown+3][jdown] == m_matrix[idown+2][jdown] and [idown+2, jdown] not in down_bigAdd and [idown+3, jdown] not in down_bigAdd:
                                m_matrix[idown+3][jdown] += m_matrix[idown+2][jdown]
                                m_matrix[idown+2][jdown] = 0
                            elif m_matrix[idown+3][jdown] == 0:
                                m_matrix[idown+3][jdown], m_matrix[idown+2][jdown] = m_matrix[idown+2][jdown], 0
                            else: continue # pass if not equal or not 0

    return m_matrix