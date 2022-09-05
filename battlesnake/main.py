from battlesnake.__version__ import version
from battlesnake.classes import Game, Snake, Board
import battlesnake.snakebrain as snakebrain
import random
import time
import typing


def info() -> typing.Dict:
    return {
        "apiversion": version,
        "author": "Trovador",  # TODO: Your Battlesnake Username
        "color": "#007bff",  # TODO: Choose color
        "head": "bonhomme",  # TODO: Choose head
        "tail": "bonhomme",  # TODO: Choose tail
    }


def start(game: Game, turn: int, board: Board, you: Snake, LOGGER):
    """Ref: https://docs.battlesnake.com/api/requests/start"""
    LOGGER.warning("START!")


def end(game: Game, turn: int, board: Board, you: Snake, LOGGER):
    """Ref: https://docs.battlesnake.com/api/requests/end"""
    LOGGER.warning("\nEND OF GAME!")
    LOGGER.warning(game)
    LOGGER.warning(turn)
    LOGGER.warning(board)
    LOGGER.warning(you)


def move(game: Game, turn: int, board: Board, you: Snake, LOGGER) -> typing.Dict:
    begin_time = time.perf_counter()
    is_move_safe, safe_moves_list = snakebrain.get_safe_moves(board, you)
    safe_time = time.perf_counter() - begin_time
    # is_move_safe, smart_moves_list = snakebrain.get_smart_moves(board, you, is_move_safe)
    # smart_time = time.perf_counter() - begin_time

    # if smart_moves_list:
    #     LOGGER.info(f"Smart! {smart_moves_list}")
    #     move = random.choice(smart_moves_list)
    # elif safe_moves_list:
    if safe_moves_list:
        LOGGER.info(f"Safe! {safe_moves_list}")
        move = random.choice(safe_moves_list)
    else:
        LOGGER.critical("No safe moves! Moving down")
        move = "down"

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = board.food

    total_time = time.perf_counter() - begin_time
    LOGGER.debug(f"Moved {move} in {total_time/1000:2f}ms (safe: {safe_time/1000:2f}ms)")
    return {"move": move, "shout": f"{move.upper()} SUUUUUUU"}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from battlesnake.api import run_server
    run_server()
