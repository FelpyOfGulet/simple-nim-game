import random

game_board = [
    5,
    3,
    8,
    2,
    6
]

def find_binary(board):
    max_len = 0
    raw_bins = [bin(x)[2:] for x in board]
    for binary in raw_bins:
        if len(binary) >= max_len:
            max_len = len(binary)
    
    new_bins = []
    for binary in raw_bins:
        new_bins.append("0" * (max_len - len(binary)) + binary)
    
    return new_bins

def subtract_from_binary(binary_str, integer):
    # Convert binary string to decimal
    decimal = int(binary_str, 2)

    # Subtract the integer
    result = decimal - integer

    # Convert back to binary and format
    return format(result, '03b')

def print_board(board):
    binaries = find_binary(game_board)
    for i in range(len(board)):
        display_row = "*" * board[i]
        length = 10 - len(display_row)
        binary = bin(board[i])[2:]
        print(str(i+1) + ": " + display_row + " " * length  + binaries[i])

def check_win(board):
    win = True
    for row in board:
        if row != 0:
            win = False
            return win

    return win

def find_columns(board):
    binaries = find_binary(board)
    populated_list = [0] * len(binaries[0])
    for i in range(len(binaries)):
        for j in range(len(binaries[i])):
            populated_list[j] += int(binaries[i])
    
    columns = [digit for digit in str(populated_list[0])]
    return columns

def check_balance(cols):
    balance = True
    for col in cols:
        if int(col) % 2 == 1:
            balance = False
            return balance
    
    return balance

def find_suggested_move(board):
    bins = find_binary(board)
    cols = find_columns(board)
    move = []
    balanced = check_balance(cols)
    while not balanced:
        temp_bins = bins.copy()  
        for i in range(len(bins)):
            bin_value = int(bins[i], 2)
            for j in range(bin_value + 1):
                temp = subtract_from_binary(bins[i], j)
                
                if int(temp, 2) < 0 or int(temp, 2) > bin_value:
                    continue

                temp_bins[i] = temp
                temp_board = [int(x, 2) for x in temp_bins]
                temp_cols = find_columns(temp_board)
                balanced = check_balance(temp_cols)
                
                if balanced:
                    move = [i+1, j]
                    return move

            temp_bins[i] = bins[i]

    return move

def player_move(player, practice = False):
    if practice:
        print(find_suggested_move(game_board))

    invalid_row = True
    while invalid_row:
        print(f"{player}: Which row do you want to remove coins from?")
        row = int(input()) - 1

        if row < 0 or row >= len(game_board):
            print("Invalid row")
        else:
            invalid_row = False
    
    invalid_coins = True
    while invalid_coins:
        print("How many coins do you want to remove?")
        coin_amount = int(input())

        if coin_amount <= 0:
            print("That move is invalid")
        elif coin_amount <= game_board[row]:
            game_board[row] -= coin_amount
            invalid_coins = False
        else:
            print("That is too many coins")

    if check_win(game_board):
        print(f"{player} wins")
    else:
        print_board(game_board)
    
def cpu_move():
    move = find_suggested_move(game_board)
    if move:
        choice_row = int(move[0]) - 1
        coin_amount = move[1]
    else:
        for i in range(len(game_board)):
            if game_board[i] != 0:
                choice_row = i
        coin_amount = 1

    print([choice_row + 1, coin_amount])
    game_board[choice_row] -= coin_amount
    print_board(game_board)

    if check_win(game_board):
        print("CPU Wins")

player1_turn = True

print("(S)ingle Player, (M)ultiplayer, (P)ractice?")
game_type = input()

print_board(game_board)

if game_type == "M" or game_type == "m":

    while not check_win(game_board):
        if player1_turn:
            player_move("Player 1")
            player1_turn = False
            
        else:
            player_move("Player 2")
            player1_turn = True

elif game_type == "S" or game_type == "s":

    while not check_win(game_board):
        if player1_turn:
            player_move("Player 1")
            player1_turn = False
            
        else:
            cpu_move()
            player1_turn = True

elif game_type == "P" or game_type == "p":

    while not check_win(game_board):
        if player1_turn:
            player_move("Player 1", True)
            player1_turn = False
            
        else:
            cpu_move()
            player1_turn = True
