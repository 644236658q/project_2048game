# Project_2048
# Will
from functions import rand_for_each_round
from functions import createOriginalMatrix
from functions import getUsersInput
from functions import lose
from functions import movements

matrix = createOriginalMatrix()
i_win = 2048 # goal
b_winOrLose = False # just check end as win or lose
while any(i_win not in row[:] for row in matrix):
    comp_matrix = [row[:] for row in matrix] # make a copy of the previous matrix that won't be affect by the manipulations
    move = getUsersInput()
    if move in 'wsad': # nothing happen when user press other keys
        new_matrix = movements(matrix, move)
        if new_matrix != comp_matrix: # if the manipulated matrix == previous one, no added cell available
            rand_for_each_round(new_matrix)
        for it in range(4):
            print(new_matrix[it])

        # when lost:
        if not any(0 in row[:] for row in new_matrix) and new_matrix == comp_matrix: # when there is no 0 and make no movement
            s_lose = lose(b_winOrLose)
            if s_lose == 'y':
                matrix = createOriginalMatrix()
            else:
                print('see you next time')
                break

        # when won:
        elif any(i_win in row[:] for row in new_matrix): # when it reaches to 2048
            b_winOrLose = True
            s_lose = lose(b_winOrLose)
            if s_lose == 'y':
                matrix = createOriginalMatrix()
            else:
                print('bye game winner')
                break
    elif move == 'q': break # users wants to quit