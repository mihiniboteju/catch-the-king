from checkmate import checkmate
import random


def kpos_generator(size): 
    return random.randint(0, size - 1) # <--- to get the king position randomly

def chessgame():
    print("==== Let's Play Chess Game (Catch The King If You Can!!!) ====")

    piece_limits = { #<--- limiting the count ot each piece base on standard chess
        'B': 2,
        'R': 2,
        'Q': 1,
        'P': 8,
    }

    piece_counts = {} #<--- to storing piece and count for ex:  {'B': 2, 'R': 1, 'Q': 1}
    total_pieces = 0
    # Here is to ask the user about piece and their count
    for piece, max_allowed in piece_limits.items():
        while True:
            try:
                count = int(input(f"How many {piece}s do you want to place? (0 to {max_allowed}): "))
                if 0 <= count <= max_allowed: #<--- checking the limit
                    piece_counts[piece] = count
                    total_pieces += count
                    break
                else:
                    print(f"Invalid!!! You can only place up to {max_allowed} {piece}(s).")
            except ValueError:
                print("Please Enter A Valid Number!")

    total_pieces += 1  #<---- we need to add 1 coz we are using random function to generate King position so to check the valid chess board we need to consider also for King

#this part is for board grid
    while True:
        try:
            rows = int(input("Enter number of rows (2 to 8): "))
            cols = int(input("Enter number of columns (2 to 8): "))
            if not (2 <= rows <= 8 and 2 <= cols <= 8):
                print("Both row and column must be between 2 and 8.")
                continue
            if rows != cols: #<--- checking square or not
                print(f"The grid is not square ({rows}x{cols})!") 
                return
            else:
                print(f"The grid is square ({rows}x{cols})!")
                size = rows 
            if total_pieces > size * size: #<--- Checking the total number of pieces is availabe with the input size of borad or not
                print("Not Enough Space For All Pieces On This Board!!!")
                continue
            break
        except ValueError:
            print("Invalid Input!!! Please Enter A Number.")

    board = [['.' for _ in range(size)] for _ in range(size)] #<---- for board
    used_positions = set() #<--- checking the duplicate position placement
#for here is for asking the position of each piece
    for piece, count in piece_counts.items():
        for i in range(count):
            while True:
                try:
                    row = int(input(f"{piece}[{i+1}] Row (0 to {size-1}): "))
                    col = int(input(f"{piece}[{i+1}] Col (0 to {size-1}): "))
                    if not (0 <= row < size and 0 <= col < size): #<--- checking the avalible input size or not
                        print("The Input Position Is Out Of Range!!!")
                        continue
                    if (row, col) in used_positions:
                        print("That Square Is already Taken!") #<--- checking the position not to be duplicate
                        continue
                    board[row][col] = piece
                    used_positions.add((row, col))
                    break
                except ValueError:
                    print("Please Enter Valid Numbers!")
# generating the king position
    while True:
        king_row, king_col = kpos_generator(size), kpos_generator(size)
        if (king_row, king_col) not in used_positions:
            board[king_row][king_col] = 'K'
            break
# print the board with pieces
    print("\n=== Final Board===")
    for row in board:
        print(" ".join(row))
    

    board_str = "\n".join(" ".join(row) for row in board)
    print("\nChecking The Result.....")
    checkmate(board_str)