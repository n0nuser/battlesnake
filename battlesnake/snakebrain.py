from battlesnake.classes import Coordinate, Board, Snake


def up(head):
    return Coordinate(x=head.x, y=head.y + 1)


def down(head):
    return Coordinate(x=head.x, y=head.y - 1)


def left(head):
    return Coordinate(x=head.x - 1, y=head.y)


def right(head):
    return Coordinate(x=head.x + 1, y=head.y)


def get_safe_moves(board: Board, you: Snake):
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    possible_moves = {"up": up(you.head), "down": down(you.head), "left": left(you.head), "right": right(you.head)}

    avoid_moving_backwards(you.body, is_move_safe)
    avoid_moving_out_of_board(board, is_move_safe, possible_moves)
    avoid_myself(you, is_move_safe, possible_moves)
    avoid_other_snakes(board, is_move_safe, possible_moves)

    safe_moves_list = [move for move, isSafe in is_move_safe.items() if isSafe]
    return is_move_safe, safe_moves_list


def avoid_other_snakes(board: Board, is_move_safe: dict, possible_moves: dict):
    opponents_bodies = [snake.body for snake in board.snakes]
    for opponent_coords in opponents_bodies:
        for key, value in possible_moves.items():
            if value in opponent_coords:
                is_move_safe[key] = False


def avoid_myself(you: Snake, is_move_safe: dict, possible_moves: dict):
    for key, value in possible_moves.items():
        if at_body(value, you):
            is_move_safe[key] = False


def avoid_moving_out_of_board(board: Board, is_move_safe: dict, possible_moves: dict):
    for key, value in possible_moves.items():
        if out_of_wall(value, board):
            is_move_safe[key] = False


def avoid_moving_backwards(body: Coordinate, is_move_safe: dict):
    if body[1].x < body[0].x:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif body[1].x > body[0].x:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif body[1].y < body[0].y:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif body[1].y > body[0].y:  # Neck is above head, don't move up
        is_move_safe["up"] = False


def at_wall(coord: Coordinate, board: Board):
    """Return true if coord is at outer edge of board"""
    return coord.x <= 0 or coord.y <= 0 or coord.x >= board.width - 1 or coord.y >= board.height - 1


def out_of_wall(coord: Coordinate, board: Board):
    """Return true if coord is at outer edge of board"""
    return coord.x < 0 or coord.y < 0 or coord.x > board.width - 1 or coord.y > board.height - 1


def at_body(coord: Coordinate, you: Snake):
    """Return true if coord is at body"""
    return coord in you.body


def get_shortest_distance(start_coord: Coordinate, end_coord: Coordinate, board: Board):
    x_distance = abs(end_coord["x"] - start_coord["x"])
    y_distance = abs(end_coord["y"] - start_coord["y"])
    choices = [
        x_distance + y_distance,
        abs(x_distance + board.width) + y_distance,
        x_distance + abs(y_distance + board.height),
        abs(x_distance + board.width) + abs(y_distance + board.height),
    ]
    print(choices)
    return min(choices)
