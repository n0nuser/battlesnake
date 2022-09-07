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
        "color": "#119484",  # TODO: Choose color
        "head": "cosmic-horror",  # TODO: Choose head
        "tail": "cosmic-horror",  # TODO: Choose tail
    }


def start(game: Game, turn: int, board: Board, you: Snake, LOGGER):
    """Ref: https://docs.battlesnake.com/api/requests/start"""
    LOGGER.info("START!")


def end(game: Game, turn: int, board: Board, you: Snake, LOGGER):
    """Ref: https://docs.battlesnake.com/api/requests/end"""
    LOGGER.info("\nEND OF GAME!")
    LOGGER.info(game + "\n")
    LOGGER.info(turn + "\n")
    LOGGER.info(board + "\n")
    LOGGER.info(you + "\n")


def move(game: Game, turn: int, board: Board, you: Snake, LOGGER) -> typing.Dict:
    begin_time = time.perf_counter()
    safe_moves_list = snakebrain.get_safe_moves(board, you)
    safe_time = time.perf_counter() - begin_time
    smart_coord, smart_move = snakebrain.get_smart_moves(board, you, game, LOGGER)
    smart_time = time.perf_counter() - begin_time

    if smart_move and smart_move in safe_moves_list:
        LOGGER.info(f"Smart! {smart_coord} ({smart_move})")
        move = smart_move
    elif safe_moves_list:
        move = random.choice(safe_moves_list)
        LOGGER.info(f"Safe! {safe_moves_list} -> {move}")
    else:
        LOGGER.critical("No safe moves! Moving down")
        move = "down"

    total_time = time.perf_counter() - begin_time
    LOGGER.debug(
        f"Moved {move} in {total_time/1000:2f}ms (safe: {safe_time/1000:2f}ms, smart: {smart_time/1000:2f}ms)"
    )
    return {"move": move, "shout": f"{move.upper()} SUUUUUUU"}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from battlesnake.api import run_server

    run_server()
