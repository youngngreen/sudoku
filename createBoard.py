f = open('testname.txt')
filename = f.read().strip()
f.close()

try:
    f = open(f'tests/{filename}')
    file = f.readlines()
    f.close()
    board = [i.strip().split() for i in file]
    n = len(board)
    for i in range(0, n):
        for j in range(0, n):
            board[i][j] = int(board[i][j])

except FileNotFoundError:
    print('\nERROR: No file: ', filename[0:-4])


