from battlesnake.classes import Coordinate, Board, Snake, Game
from battlesnake.astar import astar, manhattan_distance, get_board_as_maze
from typing import List, Tuple, Union


def get_safe_moves(board: Board, you: Snake):
    moves = {"up": True, "down": True, "left": True, "right": True}

    for key in moves:
        moves[key] = is_move_safe(board, you, key)

    return [move for move, isSafe in moves.items() if isSafe]


def get_smart_moves(board: Board, you: Snake, game: Game, LOGGER) -> str:
    # food_percentage = get_food_percentage(board)
    if you.health < 20:
        # Low health, chase food
        path = chase_close_food(board, you, LOGGER)
        # path = chase_far_food(board, you, LOGGER)
    # elif food_percentage > 40:
    #     # Too much food, chase tail
    #     path = chase_tail(board, you, LOGGER)
    # else:
    #     path = chase_tail_avoid_food(board, you, LOGGER)
    else:
        path = chase_tail_avoid_food(board, you, LOGGER)

    if not path:
        return None, None

    coord = path[1] if len(path) > 1 else path[0]
    move_coord = Coordinate(x=coord[1], y=coord[0])  # First coord is current position, second is next move
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


def is_move_safe(board: Board, you: Snake, move: str) -> bool:
    if move == "up":
        return (
            not at_wall(up(you.head), board)
            and not at_hazard(up(you.head), board)
            and not at_snake(up(you.head), board)
        )
    elif move == "down":
        return (
            not at_wall(down(you.head), board)
            and not at_hazard(down(you.head), board)
            and not at_snake(down(you.head), board)
        )
    elif move == "left":
        return (
            not at_wall(left(you.head), board)
            and not at_hazard(left(you.head), board)
            and not at_snake(left(you.head), board)
        )
    elif move == "right":
        return (
            not at_wall(right(you.head), board)
            and not at_hazard(right(you.head), board)
            and not at_snake(right(you.head), board)
        )


def at_wall(coord: Coordinate, board: Board):
    """Return true if coord is at outer edge of board"""
    return coord.x == 0 or coord.y == 0 or coord.x == board.width - 1 or coord.y == board.height - 1


def out_of_wall(coord: Coordinate, board: Board):
    """Return true if coord is at outer edge of board"""
    return coord.x < 0 or coord.y < 0 or coord.x > board.width - 1 or coord.y > board.height - 1


def at_snake(coord: Coordinate, board: Board):
    return any(coord in snake.body for snake in board.snakes)


def at_body(coord: Coordinate, you: Snake):
    """Return true if coord is at body"""
    return coord in you.body


def at_hazard(coord: Coordinate, board: Board):
    return coord in board.hazards


def get_move_from_coord(coord: Coordinate, you: Snake):
    if coord.x > you.head.x:
        return "right"
    elif coord.x < you.head.x:
        return "left"
    elif coord.y > you.head.y:
        return "up"
    elif coord.y < you.head.y:
        return "down"


def get_direction_of_snake(you: Snake) -> str:
    if you.body[1].x < you.body[0].x:  # Neck is left of head, so move is right
        return "right"
    elif you.body[1].x > you.body[0].x:  # Neck is right of head, so move is left
        return "left"
    if you.body[1].y < you.body[0].y:  # Neck is below head, so move is up
        return "up"
    elif you.body[1].y > you.body[0].y:  # Neck is above head, so move is down
        return "down"


def get_last_position_of_tail(you: Snake) -> Coordinate:
    direction = get_direction_of_snake(you)
    if direction == "right":
        return Coordinate(x=you.body[-1].x - 1, y=you.body[-1].y)
    elif direction == "left":
        return Coordinate(x=you.body[-1].x + 1, y=you.body[-1].y)
    elif direction == "up":
        return Coordinate(x=you.body[-1].x, y=you.body[-1].y - 1)
    elif direction == "down":
        return Coordinate(x=you.body[-1].x, y=you.body[-1].y + 1)


def get_food_percentage(board: Board) -> int:
    return int((len(board.food) / (board.width * board.height)) * 100)


def get_nearest_coord(start: Coordinate, coords: List[Coordinate], LOGGER) -> Coordinate:
    """Return the nearest coord from you"""
    coords_values = sorted({manhattan_distance(start, coord): index for index, coord in enumerate(coords)}.items())
    return coords[coords_values[0][1]]


def get_furthest_coord(start: Coordinate, coords: List[Coordinate], LOGGER) -> Coordinate:
    """Return the nearest coord from you"""
    coords_values = sorted({manhattan_distance(start, coord): index for index, coord in enumerate(coords)}.items())
    return coords[coords_values[-1][1]]


def chase_tail(board: Board, you: Snake, LOGGER) -> Union[List[Tuple[int, int]], None]:
    # tail = you.body[len(you.body) - 1]
    tail = get_last_position_of_tail(you)
    board = get_board_as_maze(board, LOGGER=LOGGER)
    return astar(board, you.head, tail, LOGGER)


def chase_tail_avoid_food(board: Board, you: Snake, LOGGER) -> Union[List[Tuple[int, int]], None]:
    # tail = you.body[len(you.body) - 1]
    tail = get_last_position_of_tail(you)
    board = get_board_as_maze(board, food=True, goal=tail, LOGGER=LOGGER)
    return astar(board, you.head, tail, LOGGER)


def chase_close_food(board: Board, you: Snake, LOGGER) -> Union[List[Tuple[int, int]], None]:
    food = get_nearest_coord(you.head, board.food, LOGGER)
    board = get_board_as_maze(board, goal=food, LOGGER=LOGGER)
    return astar(board, you.head, food, LOGGER)


def chase_far_food(board: Board, you: Snake, LOGGER) -> Union[List[Tuple[int, int]], None]:
    food = get_furthest_coord(you.head, board.food, LOGGER)
    board = get_board_as_maze(board, goal=food, LOGGER=LOGGER)
    return astar(board, you.head, food, LOGGER)
