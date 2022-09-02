from battlesnake.__version__ import version
from battlesnake.classes import Game, Snake, Board
import logging
import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": version,
        "author": "n0nuser",  # TODO: Your Battlesnake Username
        "color": "#007bff",  # TODO: Choose color
        "head": "bonhomme",  # TODO: Choose head
        "tail": "bonhomme",  # TODO: Choose tail
    }


def start(game: Game, turn: int, board: Board, you: Snake):
    """Ref: https://docs.battlesnake.com/api/requests/start"""
    logging.warning("START!")


def end(game: Game, turn: int, board: Board, you: Snake):
    """Ref: https://docs.battlesnake.com/api/requests/end"""
    logging.warning("\nEND OF GAME!")
    logging.warning(game)
    logging.warning(turn)
    logging.warning(board)
    logging.warning(you)


# Called on every turn. Returns your next move.
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game: Game, turn: int, board: Board, you: Snake) -> typing.Dict:
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    head = you.body[0]  # Coordinates of your head
    neck = you.body[1]  # Coordinates of your neck

    # TODO: Step 0 - Prevent your Battlesnake from moving backwards
    not_move_backwards(head, neck, is_move_safe)

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    not_move_out_of_bounds(board, is_move_safe, head)

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    not_collide_with_myself(you, is_move_safe, head)

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    not_collide_with_other_snakes(board, is_move_safe, head)

    # Are there any safe moves left?
    safe_moves = [move for move, isSafe in is_move_safe.items() if isSafe]
    if not safe_moves:
        logging.critical(f"MOVE {turn}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = board.food

    logging.info(f"MOVE {turn}: {next_move}")
    return {"move": next_move, "shout": f"{next_move.upper()} SUUUUUUU"}


def not_collide_with_other_snakes(board, is_move_safe, head):
    opponents_bodies = [snake.body for snake in board.snakes]
    opponents_bodies_coords_x = []
    opponents_bodies_coords_y = []
    for opponent_body in opponents_bodies:
        for coordinates in opponent_body:
            opponents_bodies_coords_x.append(coordinates.x)
            opponents_bodies_coords_y.append(coordinates.y)

    if head.x + 1 in opponents_bodies_coords_x:
        is_move_safe["right"] = False
    elif head.x - 1 in opponents_bodies_coords_x:
        is_move_safe["left"] = False
    if head.y + 1 in opponents_bodies_coords_y:
        is_move_safe["up"] = False
    elif head.y - 1 in opponents_bodies_coords_y:
        is_move_safe["down"] = False


def not_collide_with_myself(you, is_move_safe, head):
    my_body_chords_x = [i.x for i in you.body]
    my_body_chords_y = [i.x for i in you.body]
    if head.x + 1 in my_body_chords_x:
        is_move_safe["right"] = False
    elif head.x - 1 in my_body_chords_x:
        is_move_safe["left"] = False
    if head.y + 1 in my_body_chords_y:
        is_move_safe["up"] = False
    elif head.y - 1 in my_body_chords_y:
        is_move_safe["down"] = False


def not_move_out_of_bounds(board, is_move_safe, head):
    possible_x_moves = list(range(board.width))
    possible_y_moves = list(range(board.height))
    if head.x + 1 not in possible_x_moves:
        is_move_safe["right"] = False
    elif head.x - 1 not in possible_x_moves:
        is_move_safe["left"] = False
    if head.y + 1 not in possible_y_moves:
        is_move_safe["up"] = False
    elif head.y - 1 not in possible_y_moves:
        is_move_safe["down"] = False


def not_move_backwards(head, neck, is_move_safe):
    if neck.x < head.x:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif neck.x > head.x:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif neck.y < head.y:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif neck.y > head.y:  # Neck is above head, don't move up
        is_move_safe["up"] = False


# Start server when `python main.py` is run
if __name__ == "__main__":
    from battlesnake.api import run_server

    run_server()
