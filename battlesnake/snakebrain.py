from battlesnake.classes import Coordinate, Board, Snake
from battlesnake.astar import astar, manhattan_distance, get_board_as_maze
from typing import List, Tuple, Union


def get_safe_moves(board: Board, you: Snake):
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    possible_moves = {"up": up(you.head), "down": down(you.head), "left": left(you.head), "right": right(you.head)}

    avoid_moving_backwards(you, is_move_safe)
    avoid_moving_out_of_board(board, is_move_safe, possible_moves)
    avoid_myself(you, is_move_safe, possible_moves)
    avoid_other_snakes(board, is_move_safe, possible_moves)

    return [move for move, isSafe in is_move_safe.items() if isSafe]


def get_smart_moves(board: Board, you: Snake, LOGGER) -> str:
    if you.health < 50:
        # Low health, chase food
        path = chase_food(board, you, LOGGER)
    else:
        # Loop until health below 50
        # path = chase_tail(board, you, LOGGER)
        path = chase_tail_avoid_food(board, you, LOGGER)

    if not path:
        return None, None

    coord = path[1] if len(path) > 1 else path[0]
    move_coord = Coordinate(x=coord[0], y=coord[1])  # First coord is current position, second is next move
    move = get_move_from_coord(move_coord, you)
    return move_coord, move


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def up(head):
    return Coordinate(x=head.x, y=head.y + 1)


def down(head):
    return Coordinate(x=head.x, y=head.y - 1)


def left(head):
    return Coordinate(x=head.x - 1, y=head.y)


def right(head):
    return Coordinate(x=head.x + 1, y=head.y)


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


def avoid_moving_backwards(you: Snake, is_move_safe: dict):
    if you.body[1].x < you.body[0].x:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif you.body[1].x > you.body[0].x:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif you.body[1].y < you.body[0].y:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif you.body[1].y > you.body[0].y:  # Neck is above head, don't move up
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


def get_move_from_coord(coord: Coordinate, you: Snake):
    if coord.x > you.head.x:
        return "right"
    elif coord.x < you.head.x:
        return "left"
    elif coord.y > you.head.y:
        return "up"
    elif coord.y < you.head.y:
        return "down"


def get_nearest_coord(start: Coordinate, coords: List[Coordinate], LOGGER) -> Coordinate:
    """Return the nearest coord from you"""
    coords_values = sorted({manhattan_distance(start, coord): index for index, coord in enumerate(coords)}.items())
    return coords[coords_values[0][1]]


def chase_tail(board: Board, you: Snake, LOGGER) -> Union[List[Tuple[int, int]], None]:
    tail = you.body[len(you.body) - 1]
    board = get_board_as_maze(board)
    return astar(board, you.head, tail, LOGGER)


def chase_tail_avoid_food(board: Board, you: Snake, LOGGER) -> Union[List[Tuple[int, int]], None]:
    tail = you.body[len(you.body) - 1]
    board = get_board_as_maze(board, food=True)
    return astar(board, you.head, tail, LOGGER)


def chase_food(board: Board, you: Snake, LOGGER) -> Union[List[Tuple[int, int]], None]:
    food = get_nearest_coord(you.head, board.food, LOGGER)
    board = get_board_as_maze(board)
    return astar(board, you.head, food, LOGGER)
