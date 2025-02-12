import numpy as np
import socket
from random import randint
import subprocess 

def string_to_tuples(input_string):
    # Remove the parentheses and split the string by the commas
    input_string = input_string.strip('()')
    points = input_string.split('),(')
    
    # Convert each part into a tuple of integers
    tuple1 = tuple(map(int, points[0].split(',')))
    tuple2 = tuple(map(int, points[1].split(',')))
    
    return tuple1, tuple2

PAWN_TABLE = np.array([
    [  0,   0,   0,   0,   0,   0,   0,   0],
    [ 10,  10,  10, 10, 10,  10,  10,  10],
    [  5,   5,  10,  20,  20,  10,   5,   5],
    [  0,   0,  10,  30,  30,  10,   0,   0],
    [  5,   5,  20,  40,  40,  20,   5,   5],
    [ 10,  10,  20,  50,  50,  20,  10,  10],
    [ 20,  20,  30,  20,  20,  30,  20,  20],
    [  0,   0,   0,   0,   0,   0,   0,   0],
])

KNIGHT_TABLE = np.array([
    [0,   0,   0,   0,   0,   0,   0,  0],
    [10, 20,   0,   5,   5,   0,  20, 10],
    [-30, 5,  30,  30,  30,  30,   5, -30],
    [10, 10,  30,  30,  30,  30,  10, 10],
    [10, 10,  30,  30,  40,  30,  10, 10],
    [-30, 5,  30,  30,  30,  30,   5, -30],
    [10, 20,   0,   5,   5,   0,  20, 10],
    [0,   0,   0,   0,   0,   0,   0,  0],
])

BISHOP_TABLE = np.array([
    [20,  10, 10,  10,  10, 10, 10, 20],
    [10,  30,   0,   0,   0,   0,  30, 10],
    [10,   0,   5,  10,  10,   5,   0, 10],
    [10,   5,  10,  15,  15,  10,   5, 10],
    [10,   5,  10,  15,  15,  10,   5, 10],
    [10,   0,   5,  10,  10,   5,   0, 10],
    [10,  30,   0,   0,   0,   0,  30, 10],
    [20,  10, 10,  10,  10, 10, 10, 20],
])

ROOK_TABLE = np.array([
    [0,   -50,  10,  15,  15,  10,  -50,  0], 
    [5,   10,  15,  20,  20,  15,   10,  5],
    [10,  15,  20,  25,  25,  20,   15, 10],
    [15,  20,  25,  30,  30,  25,   20, 15],
    [20,  25,  30,  35,  35,  30,   25, 20],
    [15,  20,  25,  30,  30,  25,   20, 15],
    [10,  15,  20,  25,  25,  20,   15, 10],
    [0,   -50,  10,  15,  15,  10,  -50,  0],
])

QUEEN_TABLE = np.array([
    [20, 10, 10,   5,   5, 10, 10, 20],
    [10,  0,  0,   0,   0,  0,  0, 10],
    [10,  0, 50,  50,  50, 50,  0, 10],
    [ 5,  0, 50, 100, 100, 50,  0,  5],
    [ 0, 50, 50, 100, 100, 50, 50,  0],
    [10, 50, 50,  50,  50, 50,  0, 10],
    [10,  0, 50,   0,   0,  0,  0, 10],
    [20, 10, 10,   5,   5, 10, 10, 20],
])

KING_TABLE = np.array([
    [30, 40, 40, 50,  50, 40, 40, 30],
    [30, 40, 40, 50,  50, 40, 40, 30],
    [30, 40, 40, 50,  50, 40, 40, 30],
    [30, 40, 40, 50,  50, 40, 40, 30],
    [20, 30, 30, 40,  40, 30, 30, 20],
    [10, 20, 20, 20,  20, 20, 20, 10],
    [20, 20,  0,  0,   0,  0, 20, 20],
    [20, 30,100,-40,   0,-40,100,20],
])


tables = {
    'N': (300, KNIGHT_TABLE),
    'Q': (900, QUEEN_TABLE),
    'P': (100, PAWN_TABLE),
    'R': (500, ROOK_TABLE),
    'B': (300, BISHOP_TABLE),
    'K': (100000, KING_TABLE)
}

def evaluate_piece(piece, x, y):
    """Evaluate a single piece's score based on type, position, and color."""
    if piece == '--':
        return 0
    color = piece[0]
    ptype = piece[1]
    my = y if color == 'w' else 7 - y

    if ptype in tables:
        base, table = tables[ptype]
        piece_position_score = table[my][x]
        score = base + piece_position_score
        return score if color == 'w' else -score
    return 0


def evaluate_material(game):
    """Sum material and positional table values."""
    return sum(evaluate_piece(game.chess_board[y][x], x, y) 
               for y in range(8) for x in range(8) 
               if game.chess_board[y][x] != '--')


def get_game_phase(game):
    """
    Determine the game phase based on material.
    A simple heuristic:
    - Count total material (excluding kings).
    - The less material on the board, the closer to the endgame.
    Returns a value between 0 (opening) and 1 (endgame).
    """
    # Example heuristic: sum up material and normalize
    white_material = 0
    black_material = 0
    for y in range(8):
        for x in range(8):
            piece = game.chess_board[y][x]
            if piece != '--':
                p_color = piece[0]
                p_type = piece[1]
                if p_type in tables:
                    val, _ = tables[p_type]
                    if p_color == 'w':
                        white_material += val
                    else:
                        black_material += val

    total_material = white_material + black_material

    phase = max(0, min(1, (5600 - total_material) / 3600))
    return phase


def get_legal_moves_for_color(game, color):
    """Utility to get all legal moves for a given color."""
    return game.white_moves if color == 'white' else game.black_moves

def evaluate_control_of_key_squares(game):
    """Evaluate control of central and other important squares."""
    # As a simple example, still emphasize center squares but now variable based on phase:
    center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    return sum(20 if game.chess_board[y][x][0] == 'w' else -20
               for x, y in center_squares
               if game.chess_board[y][x] != '--')



def is_in_endgame(game):
    """Heuristic to decide if in endgame."""
    # Use the get_game_phase function. If phase > 0.7, consider endgame.
    return get_game_phase(game) > 0.7


def king_is_active(king_pos):
    """Check if king is active (centralized) - relevant in endgame."""
    if king_pos is None:
        return False
    x, y = king_pos
    # Active if closer to center in endgame
    return (2 <= x <= 5 and 2 <= y <= 5)


def evaluate_endgame_features(game):
    """Evaluate features specific to the endgame."""
    score = 0
    if is_in_endgame(game):
        white_king_pos = find_king_position(game, 'white')
        black_king_pos = find_king_position(game, 'black')
        if king_is_active(white_king_pos):
            score += 50
        if king_is_active(black_king_pos):
            score -= 50
    return score


def find_king_position(game, color):
    """Returns the position of the king for a given color."""
    for y in range(8):
        for x in range(8):
            piece = game.chess_board[y][x]
            if piece == f'{color[0]}K':  # White king or black king
                return (x, y)
    return None
def center_control(game) :
    score = 0 
    for start_pos, possible_moves in game.white_moves.items():
        for end_pos in possible_moves :
            x,y = end_pos 
            if (x>2 and x<5 and y>2 and y<5) :
                score+=1
    for start_pos, possible_moves in game.black_moves.items():
        for end_pos in possible_moves :
            x,y = end_pos 
            if (x>2 and x<5 and y>2 and y<5) :
                score-=1
    return score

def evaluate(game,transporation_table):
    """Calculates the total evaluation score for the game based on various factors."""
    # Control of key squares
    material_score = evaluate_material(game)
    control_score = evaluate_control_of_key_squares(game)

    # Endgame features
    endgame_score = evaluate_endgame_features(game)

    # Determine game phase and interpolate
    phase = get_game_phase(game)  
    opening_weight = 1 - phase
    endgame_weight = phase

    # Combine scores
    # Material remains essential throughout, but other factors change importance over time.
    total_score = (
        material_score*1 +
        control_score * (0.6 * opening_weight + 0.3 * endgame_weight) +
        endgame_score * endgame_weight
    )

    return total_score



def AI(game, start_pos, end_pos,conn):

    while True:
                response = "("+str(start_pos[0])+","+str(7-start_pos[1])+"),("+ str(end_pos[0])+"," + str(7-end_pos[1])+ ")"
                print(response)
                print(conn)
                conn.sendall(response.encode())
                # Receive data from C++ client
                data = conn.recv(1024)
                print('data is None ',data is None)
                print(data)
                print(data.decode())
                print('new line')
                if not data:
                    break
                print("Received from client:", data.decode())
                start_pos_0,end_pos_0 = string_to_tuples(data.decode())
                print('star pos is ',start_pos_0)
                print('end pos is ',end_pos_0)
                return start_pos_0,end_pos_0
            
def AI_hard(game) :
    game.all_moves()
    game.change_player()
    game.all_moves()        
    game.change_player()
    moves_scores = []

    moves = game.white_moves if game.turn == 'white' else game.black_moves
    for start_pos, possible_moves in moves.items():
        for end_pos in possible_moves:
            copy_game = game.copy_game()
            copy_game.all_moves()
            x, y = end_pos
            copy_game.move_piece(start_pos, x, y)
            copy_game.change_player()
            score = copy_game.evaluate_hard()
            moves_scores.append((score, (start_pos, end_pos)))

    
    moves_scores.sort(reverse=False, key=lambda x: x[0])

    # Return the move with the best score
    print(moves_scores)
    if moves_scores:
        print(f"Best move: {moves_scores[0][1]} with score {moves_scores[0][0]}")
        return moves_scores[0][1]
    print("No valid moves found")
    return None


    