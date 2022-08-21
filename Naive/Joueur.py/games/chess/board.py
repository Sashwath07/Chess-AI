from games.chess.game_state import GameState
# from game_state import GameState


def generate_board(fen):
    game_string = fen.split(' ')
    rows = game_string[0].split('/')
    board = []

    for row in rows:
        rank = []
        for char in row:
            try:
                for i in range(int(char)):
                    rank.append(' ')
            except:
                rank.append(char)
        board.append(rank)
    active_color = game_string[1]
    castling = game_string[2]
    en_passant = game_string[3]
    halfmove = game_string[4]
    fullmove = game_string[5]
    return GameState(board, active_color, castling, en_passant, halfmove, fullmove)

# Performs a move and returns the resulting board
def perform_move(board, initial_pos, final_pos):
    piece = board[initial_pos[0]][initial_pos[1]]
    board[initial_pos[0]][initial_pos[1]] = ' '
    board[final_pos[0]][final_pos[1]] = piece       
    return board

# Performs an en passant move and returns the resulting board
def perform_move_en_passant(board, initial_pos, final_pos, color):
    piece = board[initial_pos[0]][initial_pos[1]]
    board[initial_pos[0]][initial_pos[1]] = ' '
    board[final_pos[0]][final_pos[1]] = piece  
    if color == 'black':
        board[final_pos[0] - 1][final_pos[1]] = ' '
    else:
        piece_check = board[final_pos[0] - 1][final_pos[1]]
        board[final_pos[0] + 1][final_pos[1]] = ' '
    return board