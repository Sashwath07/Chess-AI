from games.chess.board import *
# from board import *

class GamePiece:
    def __init__(self, color, type, position, has_moved):
        self.color = color
        self.type = type
        self.position = position
        self.has_moved = has_moved

# Convert a position from 2d list representation to rank and file
def convert_position(position):
    row = 8 - position[0]
    col = chr(ord('`') + position[1]+1)
    return str(col) + str(row)

# Convert a position from rank and file to 2d list representation
def convert_position_to_index(position):
    if len(position) > 4:
        position = position[:4]
    row = 8 - int(position[1])
    col = ord(position[0]) - 97
    return [row, col]

# Get the possible move directions for king, queen, knight, bishop, and rook pieces
def possible_moves(type):
    knight_moves = [[-2, 1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1]]
    bishop_moves = [[-1, -1], [-1, 1], [1, 1], [1, -1]]
    rook_moves = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    queen_moves = bishop_moves + rook_moves

    if type == 'knight':
        possible_moves = knight_moves
    elif type == 'bishop':
        possible_moves = bishop_moves
    elif type == 'rook':
        possible_moves = rook_moves
    elif type == 'queen' or 'king':
        possible_moves = queen_moves
    return possible_moves

# get the position of the king on the board
def get_king_pos(board, color):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if color == 'black':
                if board[i][j] == 'k':
                    king_pos = [i, j]
                    return king_pos
            else:
                if board[i][j] == 'K':
                    king_pos = [i, j]
                    return king_pos
    return None

# Get the possible moves of the king
def get_king_moves(board, color):
    king_pos = get_king_pos(board, color)
    initial_pos = convert_position(king_pos)
    move_directions = possible_moves('king')
    moves = []
    for i in move_directions:
        try:
            next_position = board[king_pos[0] + i[0]][king_pos[1] + i[1]]
            if next_position == ' ' or next_position.isupper() and color == 'black' or next_position.islower() and color == 'white':
                final_pos = convert_position([king_pos[0] + i[0], king_pos[1] + i[1]])
                if final_pos.isalnum() == False or int(final_pos[1:]) > 8 or int(final_pos[1:]) < 1:
                        continue
                moves.append(initial_pos + final_pos)
        except:
            pass
    return moves

# Get the possible moves for the queen
def get_queen_moves(board, color):
    queen_pos = []
    # Find the position of the queens
    for i in range(len(board)):
        for j in range(len(board[i])):
            if color == 'black':
                if board[i][j] == 'q':
                    queen_pos.append([i,j])
            else:
                if board[i][j] == 'Q':
                    queen_pos.append([i,j])
    move_directions = possible_moves('queen')
    moves = []
    for i in queen_pos:
        for move in move_directions:
            initial_pos = convert_position(i)
            n = 1
            try:
                while board[i[0] + move[0] * n][i[1] + move[1] * n] == ' ' or \
                board[i[0] + move[0] * n][i[1] + move[1] * n].isupper() and color == 'black' or \
                    board[i[0] + move[0] * n][i[1] + move[1] * n].islower() and color == 'white':
                    next_position = board[i[0] + move[0] * n][i[1] + move[1] * n]
                    final_pos = convert_position([i[0] + move[0] * n, i[1] + move[1] * n])
                    n += 1
                    if final_pos.isalnum() == False or int(final_pos[1:]) > 8 or int(final_pos[1:]) < 1:
                        continue
                    board_new = [row[:] for row in board]
                    board_new[i[0]][i[1]] = ' '
                    moves.append(initial_pos + final_pos)
                    # Stop queen from moving the direction if there is a capture
                    if next_position.isupper() and color == 'black' or next_position.islower() and color == 'white':
                        break
            except:
                pass
    return moves
    
# Get the possible moves for the bishops
def get_bishop_moves(board, color):
    bishop_pos = []
    # Find the position of bishops
    for i in range(len(board)):
        for j in range(len(board[i])):
            if color == 'black':
                if board[i][j] == 'b':
                    bishop_pos.append([i,j])
            else:
                if board[i][j] == 'B':
                    bishop_pos.append([i,j])
    move_directions = possible_moves('bishop')
    moves = []
    for i in bishop_pos:
        for j in move_directions:
            n = 1
            try:
                while board[i[0] + j[0] * n][i[1] + j[1] * n] == ' ' or \
                board[i[0] + j[0] * n][i[1] + j[1] * n].isupper() and color == 'black' or \
                    board[i[0] + j[0] * n][i[1] + j[1] * n].islower() and color == 'white':
                    next_position = board[i[0] + j[0] * n][i[1] + j[1] * n]
                    final_pos = convert_position([i[0] + j[0] * n, i[1] + j[1] * n])
                    n += 1
                    if final_pos.isalnum() == False or int(final_pos[1:]) > 8 or int(final_pos[1:]) < 1:
                        continue
                    initial_pos = convert_position(i)
                    moves.append(initial_pos + final_pos)
                    # stop queen from moving the direction if there is a capture
                    if next_position.isupper() and color == 'black' or next_position.islower() and color == 'white':
                        break
            except:
                pass
    return moves

# Get the possible moves for the rooks
def get_rook_moves(board, color):
    rook_pos = []
    # Find the position of rooks
    for i in range(len(board)):
        for j in range(len(board[i])):
            if color == 'black':
                if board[i][j] == 'r':
                    rook_pos.append([i,j])
            else:
                if board[i][j] == 'R':
                    rook_pos.append([i,j])
    move_directions = possible_moves('rook')
    moves = []
    for i in rook_pos:
        for j in move_directions:
            n = 1
            try:
                while board[i[0] + j[0] * n][i[1] + j[1] * n] == ' ' or \
                board[i[0] + j[0] * n][i[1] + j[1] * n].isupper() and color == 'black' or \
                    board[i[0] + j[0] * n][i[1] + j[1] * n].islower() and color == 'white':
                    next_position = board[i[0] + j[0] * n][i[1] + j[1] * n]
                    final_pos = convert_position([i[0] + j[0] * n, i[1] + j[1] * n])
                    n += 1
                    if final_pos.isalnum() == False or int(final_pos[1:]) > 8 or int(final_pos[1:]) < 1:
                        continue
                    initial_pos = convert_position(i)
                    moves.append(initial_pos + final_pos)
                    # stop queen from moving the direction if there is a capture
                    if next_position.isupper() and color == 'black' or next_position.islower() and color == 'white':
                        break
            except:
                pass
    return moves

# Get the possible castling moves
def get_castle_moves(board, castle, color):
    moves = []
    if castle == '-':
        return moves
    if color == 'white':
        if 'K' in castle:
            next_pos = board[7][6]
            if next_pos == ' ' and board[7][5] == ' ':
                initial_pos = convert_position([7, 4])
                final_pos = convert_position([7, 6])
                under_attack = check_space_under_attack(board, color, [[7, 4], [7, 5], [7, 6]])
                if under_attack == False:
                    moves.append(initial_pos + final_pos)
        if 'Q' in castle:
            next_pos = board[7][2]
            if next_pos == ' ' and board[7][3] == ' ' and board[7][1] == ' ':
                initial_pos = convert_position([7, 4])
                final_pos = convert_position([7, 2])
                under_attack = check_space_under_attack(board, color, [[7, 2], [7, 3], [7, 4]])
                if under_attack == False:
                    moves.append(initial_pos + final_pos)
    else:
        if 'k' in castle:
            next_pos = board[0][6]
            if next_pos == ' ' and board[0][5] == ' ':
                initial_pos = convert_position([0, 4])
                final_pos = convert_position([0, 6])
                under_attack = check_space_under_attack(board, color, [[0, 4], [0, 5], [0, 6]])
                if under_attack == False:
                    moves.append(initial_pos + final_pos)
        if 'q' in castle:
            next_pos = board[0][2]
            if next_pos == ' ' and board[0][3] == ' ' and board[7][1] == ' ':
                initial_pos = convert_position([0, 4])
                final_pos = convert_position([0, 2])
                under_attack = check_space_under_attack(board, color, [[0, 2], [0, 3], [0, 4]])
                if under_attack == False:
                    moves.append(initial_pos + final_pos) 
    return moves

# Check if a space is under attack, used to check if castling is valid
def check_space_under_attack(board, color, spaces_to_check):
    for space in spaces_to_check:
        opponent_color = 'black' if color == 'white' else 'white'
        opponent_moves = get_king_moves(board, opponent_color) + get_bishop_moves(board, opponent_color) + get_rook_moves(board, opponent_color) + get_knight_moves(board, opponent_color) + get_queen_moves(board, opponent_color) + get_pawn_moves(board, opponent_color)
        for opponent_move in opponent_moves:
            board_new =  [row[:] for row in board]
            initial_pos_opponent = convert_position_to_index(opponent_move[:2])
            final_pos_opponent = convert_position_to_index(opponent_move[2:4])
            board_new = perform_move(board_new, initial_pos_opponent, final_pos_opponent)
            if final_pos_opponent == space:
                return True
    return False
    
# Get the possible moves for the knights
def get_knight_moves(board, color):
    knight_pos = []
    # Find the position fo knights
    for i in range(len(board)):
        for j in range(len(board[i])):
            if color == 'black':
                if board[i][j] == 'n':
                    knight_pos.append([i,j])
            else:
                if board[i][j] == 'N':
                    knight_pos.append([i,j])
    move_directions = possible_moves('knight')
    moves = []
    for i in knight_pos:
        for j in move_directions:
            try:
                next_position = board[i[0] + j[0]][i[1] + j[1]]
                if next_position == ' ' or next_position.isupper() and color == 'black' or next_position.islower() and color == 'white':
                    final_pos = convert_position([i[0] + j[0], i[1] + j[1]])
                    if final_pos.isalnum() == False or int(final_pos[1:]) > 8 or int(final_pos[1:]) < 1:
                        continue
                    initial_pos = convert_position(i)
                    moves.append(initial_pos + final_pos)
            except:
                pass
    return moves

# Find the position of the pawns
def get_pawn_pos(board, color):
    pawn_pos = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if color == 'black':
                if board[i][j] == 'p':
                    pawn_pos.append([i,j])
            else:
                if board[i][j] == 'P':
                    pawn_pos.append([i,j])
    return pawn_pos

# Get the possible moves for the pawns
def get_pawn_moves(board, color):
    pawn_pos = get_pawn_pos(board, color)
    moves = []
    for i in pawn_pos:
        initial_pos = convert_position(i)
        if color == 'black':
                if i[0] == 1:   # Check if pawn is at starting position (black)
                    move_directions = [[1, 0], [2, 0]]
                else:
                    move_directions = [[1, 0]]
        else:
            if i[0] == 6:   # Check if pawn is at starting position (white)
                move_directions = [[-1, 0], [-2, 0]]
            else:
                move_directions = [[-1, 0]]
        try:
            for move in move_directions:
                next_pos = board[i[0] + move[0]][i[1]]
                # Check if there is a blocking piece for a 2 step move
                if move == [2,0] and board[i[0] + 1][i[1]] != ' ':
                    continue
                elif move == [-2, 0] and board[i[0] - 1][i[1]] != ' ':
                    continue
                if next_pos == ' ':
                    final_pos = convert_position([i[0] + move[0], i[1]])
                    if final_pos.isalnum() == False or int(final_pos[1:]) > 8 or int(final_pos[1:]) < 1:
                        continue
                    if color == 'black' and int(final_pos[1]) == 1:
                        possible_promotions = ['q', 'r', 'b', 'n']
                        for promotion in possible_promotions:
                            moves.append(initial_pos + final_pos + promotion)
                        continue
                    elif color == 'white' and int(final_pos[1]) == 8:
                        possible_promotions = ['Q', 'R', 'B', 'N']
                        for promotion in possible_promotions:
                            moves.append(initial_pos + final_pos + promotion)
                        continue
                    moves.append(initial_pos + final_pos)
            pawn_captures = check_pawn_capture(board, color, pawn_pos)
            moves.extend(pawn_captures)
        except:
            pass
    return moves

# Check if the pawns can perform captues
def check_pawn_capture(board, color, pawn_pos):
    move_directions_white = [[-1, -1], [-1, 1]]
    move_directions_black = [[1, -1], [1, 1]]
    moves = []
    for i in pawn_pos:
        initial_pos = convert_position(i)
        # check if the square diagonally ahead of the pawn can be captured
        if color == 'black':
            for move in move_directions_black:
                try:
                    if board[i[0] + move[0]][i[1] + move[1]].isupper() == True:
                        final_pos = convert_position([i[0] + move[0], i[1] + move[1]])
                        if final_pos.isalnum() == False or int(final_pos[1:]) > 8 or int(final_pos[1:]) < 1:
                            continue
                        moves.append(initial_pos + final_pos)
                except:
                    pass
        else:
            for move in move_directions_white:
                try:
                    if board[i[0] + move[0]][i[1] + move[1]].islower() == True:
                        final_pos = convert_position([i[0] + move[0], i[1] + move[1]])
                        if final_pos.isalnum() == False or int(final_pos[1:]) > 8 or int(final_pos[1:]) < 1:
                            continue
                        moves.append(initial_pos + final_pos)
                except:
                    pass
    return moves

# Check if the moves generated are valid
def check_valid_moves(board, color, moves_to_check):
    opponent_color = 'black' if color == 'white' else 'white'
    invalid_moves = []
    for move in moves_to_check:
        board_new =  [row[:] for row in board]
        initial_pos = convert_position_to_index(move[:2])
        final_pos = convert_position_to_index(move[2:4])
        updated_board = perform_move(board_new, initial_pos, final_pos)
        opponent_moves = get_king_moves(updated_board, opponent_color) + get_bishop_moves(updated_board, opponent_color) + get_rook_moves(updated_board, opponent_color) + get_knight_moves(updated_board, opponent_color) + get_queen_moves(updated_board, opponent_color) + get_pawn_moves(updated_board, opponent_color)
        for opponent_move in opponent_moves:
            updated_board_new =  [row[:] for row in updated_board]
            initial_pos_opponent = convert_position_to_index(opponent_move[:2])
            final_pos_opponent = convert_position_to_index(opponent_move[2:4])
            updated_board_new = perform_move(updated_board_new, initial_pos_opponent, final_pos_opponent)
            king_pos = get_king_pos(updated_board_new, color)
            if king_pos is None:
                invalid_moves.append(move)
                break
            if 'Z' in move:
                invalid_moves.append(move)
                break
    valid_moves = list(set(moves_to_check) - set(invalid_moves))
    return valid_moves

# Get the en passant moves
def get_en_passant(board, color, en_passant):
    pawn_pos = get_pawn_pos(board, color)
    en_passant_pos = convert_position_to_index(en_passant)
    moves = []
    for i in pawn_pos:
        initial_pos = convert_position(i)
        try:
            if color == 'black':
                if [i[0], i[1] - 1] == [en_passant_pos[0] - 1, en_passant_pos[1]] or [i[0], i[1] + 1] == [en_passant_pos[0] - 1, en_passant_pos[1]]:
                    final_pos = en_passant
                    moves.append(initial_pos + final_pos)
                pass
            else:
                if [i[0], i[1] - 1] == [en_passant_pos[0] + 1, en_passant_pos[1]] or [i[0], i[1] + 1] == [en_passant_pos[0] + 1, en_passant_pos[1]]:
                    final_pos = en_passant
                    moves.append(initial_pos + final_pos)
        except:
            pass
    # Check if en passant moves are valid
    invalid_moves = []
    opponent_color = 'black' if color == 'white' else 'white'
    for move in moves:
        board_new =  [row[:] for row in board]
        initial_pos = convert_position_to_index(move[:2])
        final_pos = convert_position_to_index(move[2:4])
        updated_board = perform_move_en_passant(board_new, initial_pos, final_pos, color)
        opponent_moves = get_king_moves(updated_board, opponent_color) + get_bishop_moves(updated_board, opponent_color) + get_rook_moves(updated_board, opponent_color) + get_knight_moves(updated_board, opponent_color) + get_queen_moves(updated_board, opponent_color) + get_pawn_moves(updated_board, opponent_color)
        for opponent_move in opponent_moves:
            updated_board_new =  [row[:] for row in updated_board]
            initial_pos_opponent = convert_position_to_index(opponent_move[:2])
            final_pos_opponent = convert_position_to_index(opponent_move[2:4])
            updated_board_new = perform_move(updated_board_new, initial_pos_opponent, final_pos_opponent)
            king_pos = get_king_pos(updated_board_new, color)
            if king_pos is None:
                invalid_moves.append(move)
                break
            if 'Z' in move:
                invalid_moves.append(move)
                break
    valid_moves = list(set(moves) - set(invalid_moves))
    return valid_moves
