from games.chess.board import *
from games.chess import game_piece as gp
# from board import *
# import game_piece as gp

import random

# Calculate the utility in the player's perspective
def calculate_hEval(board, color):
    white_piece_value = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1000}
    black_piece_value = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 1000}
    # Assigns negative values to the opponent's pieces
    if color == 'white':
        black_piece_value.update((x, y*-1) for x, y in black_piece_value.items())
    else:
        white_piece_value.update((x, y*-1) for x, y in white_piece_value.items())

    # Find the utility score of the board
    utility = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] in white_piece_value.keys():
                utility += white_piece_value[board[row][col]]
            elif board[row][col] in black_piece_value.keys():
                utility += black_piece_value[board[row][col]]
    return utility

# Returns true if game over condition has been met
def game_over(board):
    white_king = []
    black_king = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 'K':
                white_king = [row, col]
            elif board[row][col] == 'k':
                black_king = [row, col]
    if white_king == [] or black_king == []:
        return True
    else:
        return False

# Generate valid moves for the given game state
def generate_moves(board, color, en_passant, castling):
    king_moves = gp.get_king_moves(board, color)
    queen_moves = gp.get_queen_moves(board, color)
    bishop_moves = gp.get_bishop_moves(board, color)
    rook_moves = gp.get_rook_moves(board, color)
    knight_moves = gp.get_knight_moves(board, color)
    pawn_moves = gp.get_pawn_moves(board, color)
    castle_moves = gp.get_castle_moves(board, castling, color)
    moves = king_moves + queen_moves + bishop_moves + rook_moves + knight_moves + pawn_moves + castle_moves
    valid_moves = gp.check_valid_moves(board, color, moves)

    # Generate en passant moves if available
    if en_passant != '-':
        en_passant_moves = gp.get_en_passant(board, color, en_passant)
        valid_moves.extend(en_passant_moves)
    # print('moves: ',valid_moves)
    return valid_moves

# Returns the max value
def max_value(board, depth, color, en_passant, castling):
    if game_over(board) == True or depth == 0:
        return calculate_hEval(board, color)
    value = -10000
    moves = generate_moves(board, color, en_passant, castling)
    for move in moves:
        board_new = [row[:] for row in board]
        initial_pos = gp.convert_position_to_index(move[:2])
        final_pos = gp.convert_position_to_index(move[2:])
        updated_board = perform_move(board_new, initial_pos, final_pos)
        value = max(value, min_value(updated_board, depth-1, color, '-', castling))
    return value

# Returns the min value
def min_value(board, depth, color, en_passant, castling):
    if game_over(board) == True or depth == 0:
        return calculate_hEval(board, color)
    value = 10000
    moves = generate_moves(board, color, en_passant, castling)
    for move in moves:
        board_new = [row[:] for row in board]
        initial_pos = gp.convert_position_to_index(move[:2])
        final_pos = gp.convert_position_to_index(move[:2])
        updated_board = perform_move(board_new, initial_pos, final_pos)
        value = min(value, max_value(updated_board, depth-1, color, '-', castling))
    return value

# Starts the minimax algorithm
def max_choice(board, depth, color, en_passant, castling, last_5_moves):
    moves = generate_moves(board, color, en_passant, castling)
    max_value = -1000
    best_moves = []
    for move in moves:
        if move in last_5_moves:
            continue
        value = min_value(board, depth, color, en_passant, castling)
        if value >= max_value:
            max_value = value
            best_moves.append(move)
    if len(best_moves) == 0:
        return random.choice(moves)
    return random.choice(best_moves)

