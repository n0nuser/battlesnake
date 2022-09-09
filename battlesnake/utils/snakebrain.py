from battlesnake.utils.classes import Coordinate, Board, Snake
from battlesnake.utils.astar import astar
from typing import List, Tuple, Union


def up(head):
    return Coordinate(x=head.x, y=head.y + 1)


def down(head):
    return Coordinate(x=head.x, y=head.y - 1)


def left(head):
    return Coordinate(x=head.x - 1, y=head.y)


def right(head):
    return Coordinate(x=head.x + 1, y=head.y)


def is_move_safe(board: Board, you: Snake, move: str) -> bool:
    possible_moves = {"up": up(you.head), "down": down(you.head), "left": left(you.head), "right": right(you.head)}
    return (
        not at_wall(possible_moves[move], board)
        and not at_snake(possible_moves[move], board)
        and not at_hazard(possible_moves[move], board)
    )


def is_move_safe_with_heads(board: Board, you: Snake, move: str) -> bool:
    possible_moves = [up(you.head), down(you.head), left(you.head), right(you.head)]
    for coord in possible_moves:
        return not (at_wall(coord, board) or at_snake(coord, board) or at_hazard(coord, board))


def at_wall(coord: Coordinate, board: Board):
    """Return true if coord is at outer edge of board"""
    return coord.x == 0 or coord.y == 0 or coord.x == board.width - 1 or coord.y == board.height - 1


def out_of_wall(coord: Coordinate, board: Board):
    """Return true if coord is at outer edge of board"""
    return coord.x < 0 or coord.y < 0 or coord.x > board.width - 1 or coord.y > board.height - 1


def at_snake(coord: Coordinate, board: Board):
    return any(coord == snake.head for snake in board.snakes)


def at_snake_body(coord: Coordinate, board: Board):
    return any(coord != snake.head and coord in snake.body for snake in board.snakes)


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


def get_direction_of_snake(head: Coordinate, neck: Coordinate) -> str:
    if neck.x < head.x:  # Neck is left of head, so move is right
        return "right"
    elif neck.x > head.x:  # Neck is right of head, so move is left
        return "left"
    if neck.y < head.y:  # Neck is below head, so move is up
        return "up"
    elif neck.y > head.y:  # Neck is above head, so move is down
        return "down"


def get_last_position_of_tail(you: Snake) -> Coordinate:
    direction = get_direction_of_snake(you.body[0], you.body[1])
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
    if not coords:
        return None
    coords_values = sorted({manhattan_distance(start, coord): index for index, coord in enumerate(coords)}.items())
    return coords[coords_values[0][1]]


def get_furthest_coord(start: Coordinate, coords: List[Coordinate], LOGGER) -> Coordinate:
    """Return the furthest coord from you"""
    if not coords:
        return None
    coords_values = sorted({manhattan_distance(start, coord): index for index, coord in enumerate(coords)}.items())
    return coords[coords_values[-1][1]]


def get_closest_snake(board: Board, you: Snake) -> Union[Snake, None]:
    """Return the closest snake to you"""
    if len(board.snakes) == 1:
        return None
    snakes = sorted(
        {manhattan_distance(you.head, snake.head): index for index, snake in enumerate(board.snakes)}.items()
    )
    return board.snakes[snakes[0][1]]


def get_next_coord(head: Coordinate, direction: str) -> Coordinate:
    if direction == "up":
        return Coordinate(x=head.x, y=head.y + 1)
    elif direction == "down":
        return Coordinate(x=head.x, y=head.y - 1)
    elif direction == "left":
        return Coordinate(x=head.x - 1, y=head.y)
    elif direction == "right":
        return Coordinate(x=head.x + 1, y=head.y)


def chase_tail(board: Board, you: Snake, LOGGER) -> Union[List[Tuple[int, int]], None]:
    # tail = you.body[len(you.body) - 1]
    tail = get_last_position_of_tail(you)
    board = get_board_as_maze(board, you, LOGGER=LOGGER)
    return astar(board, you.head, tail, LOGGER)


def chase_tail_avoid_food(board: Board, you: Snake, LOGGER) -> Union[List[Tuple[int, int]], None]:
    # tail = you.body[len(you.body) - 1]
    tail = get_last_position_of_tail(you)
    board = get_board_as_maze(board, you, food=True, goal=tail, LOGGER=LOGGER)
    return astar(board, you.head, tail, LOGGER)


def chase_close_food(board: Board, you: Snake, LOGGER) -> Union[List[Tuple[int, int]], None]:
    food = get_nearest_coord(you.head, board.food, LOGGER)
    board = get_board_as_maze(board, you, goal=food, LOGGER=LOGGER)
    return astar(board, you.head, food, LOGGER)


def chase_far_food(board: Board, you: Snake, LOGGER) -> Union[List[Tuple[int, int]], None]:
    food = get_furthest_coord(you.head, board.food, LOGGER)
    board = get_board_as_maze(board, you, goal=food, LOGGER=LOGGER)
    return astar(board, you.head, food, LOGGER)


def chase_head(board: Board, you: Snake, snake: Snake, LOGGER) -> Union[List[Tuple[int, int]], None]:
    head = snake.body[0]
    neck = snake.body[1]
    direction = get_direction_of_snake(head, neck)
    head_next_coord = get_next_coord(head, direction)
    board = get_board_as_maze(board, you, goal=head_next_coord, LOGGER=LOGGER)
    return astar(board, you.head, head, LOGGER)


def get_index(coordinate: Coordinate, board: Board):
    return coordinate.y * board.width + coordinate.x


def get_coord_from_index(index, board: Board):
    return Coordinate(index % board.width, index // board.width)


def manhattan_distance(start: Coordinate, goal: Coordinate):
    """
    Manhattan distance.
    Ref: https://en.wikipedia.org/wiki/Taxicab_geometry.
    """
    return abs(start.x - goal.x) + abs(start.y - goal.y)


def get_board_as_maze(
    board: Board,
    you: Snake,
    hazards: bool = True,
    snakes: bool = True,
    heads: bool = False,
    food: bool = False,
    goal: Coordinate = None,
    LOGGER=None,
) -> List[List[int]]:
    maze = [[0 for _ in range(board.width)] for _ in range(board.height)]
    # LOGGER.critical(f"len of maze (x): {len(maze)}")
    # LOGGER.critical(f"len of maze (y): {len(maze[0])}")

    if food:
        for food in board.food:
            # LOGGER.debug(f"Adding food {food}")
            maze[food.y][food.x] = 1

    if goal:
        # LOGGER.debug(f"Adding goal {goal}")
        maze[goal.y][goal.x] = 0

    if hazards:
        for hazard in board.hazards:
            # LOGGER.debug(f"Adding hazard {hazard}")
            maze[hazard.y][hazard.x] = 1

    if snakes:
        for snake in board.snakes:
            for coordinate in snake.body:
                if heads and coordinate == snake.head and coordinate != you.head:
                    LOGGER.debug("CHASING HEAD - MAZE")
                    continue
                LOGGER.debug(f"Adding snake coordinate {coordinate}")
                maze[coordinate.y][coordinate.x] = 1
    return maze
