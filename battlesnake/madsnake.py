from battlesnake.utils.classes import Game, Snake, Board, Coordinate
from battlesnake.utils.logger import CustomFormatter
from fastapi import FastAPI, Request, status
import battlesnake.utils.snakebrain as snakebrain
import logging
import random
import time
import typing
import uvicorn


CONFIG = {
    "backlog": 2048,
    "debug": True,
    "host": "0.0.0.0",
    "log_level": "info",
    "port": 8000,
    "reload": True,
    "timeout_keep_alive": 5,
    "workers": 4,
}

# Create logger with 'spam_application'
LOGGER = logging.getLogger("BattleSnake")
LOGGER.setLevel(logging.DEBUG)

# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())

LOGGER.addHandler(ch)

api = FastAPI(title="Battlesnake API", version="1.0")
api.logger = LOGGER

##############################################################################################################
##############################################################################################################


@api.get("/", status_code=status.HTTP_200_OK)
async def info(request: Request) -> typing.Dict:
    return {
        "apiversion": "1.0",
        "author": "MadSnake",  # TODO: Your Battlesnake Username
        "color": "#eba134",  # TODO: Choose color
        "head": "cosmic-horror",  # TODO: Choose head
        "tail": "cosmic-horror",  # TODO: Choose tail
    }


@api.post("/start", status_code=status.HTTP_200_OK)
async def start(game: Game, board: Board, you: Snake, turn: int = None):
    """Ref: https://docs.battlesnake.com/api/requests/start"""
    LOGGER.info("START!")
    return "ok"


@api.post("/end", status_code=status.HTTP_200_OK)
async def end(game: Game, board: Board, you: Snake, turn: int = None):
    """Ref: https://docs.battlesnake.com/api/requests/end"""
    LOGGER.info("\nEND OF GAME!")
    LOGGER.info(f"{game}\n")
    # LOGGER.info(f"{turn}\n")
    # LOGGER.info(f"{board}\n")
    LOGGER.info(f"{you}\n")
    return "ok"


@api.post("/move", status_code=status.HTTP_200_OK)
async def move(game: Game, board: Board, you: Snake, turn: int = None) -> typing.Dict:
    begin_time = time.perf_counter()
    safe_moves_list = get_safe_moves(board, you)
    safe_time = time.perf_counter() - begin_time
    smart_coord, smart_move, function = get_smart_moves(board, you, game, LOGGER)
    smart_time = time.perf_counter() - begin_time

    if smart_move and smart_move in safe_moves_list:
        LOGGER.info(f"Smart! - {function}: {smart_coord} ({smart_move})")
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


##############################################################################################################
##############################################################################################################


def get_safe_moves(board: Board, you: Snake) -> typing.List[str]:
    moves = {"up": True, "down": True, "left": True, "right": True}
    closest_snake = snakebrain.get_closest_snake(board, you)
    if closest_snake:
        if you.length > closest_snake.length:
            for key in moves:
                moves[key] = snakebrain.is_move_safe_with_heads(board, you, key)
    else:
        for key in moves:
            moves[key] = snakebrain.is_move_safe(board, you, key)

    return [move for move, isSafe in moves.items() if isSafe]


def get_smart_moves(board: Board, you: Snake, game: Game, LOGGER) -> str:
    closest_snake = snakebrain.get_closest_snake(board, you)
    function = ""
    if closest_snake:
        if you.length > closest_snake.length:
            path = snakebrain.chase_head(board, you, closest_snake, LOGGER)
            function = "Chase Head"
    else:
        path = snakebrain.chase_close_food(board, you, LOGGER)
        function = "Chase Close Food"

    if not path:
        return None, None

    coord = path[1] if len(path) > 1 else path[0]
    move_coord = Coordinate(x=coord[1], y=coord[0])  # First coord is current position, second is next move
    move = snakebrain.get_move_from_coord(move_coord, you)
    return move_coord, move, function


##############################################################################################################
##############################################################################################################

if __name__ == "__main__":
    """Starts the Uvicorn server with the provided configuration."""
    uviconfig = {"app": "madsnake:api", "interface": "asgi3"}
    uviconfig.update(CONFIG)
    LOGGER.info(f"\nRunning Battlesnake at http://{CONFIG.get('host')}:{CONFIG.get('port')}")
    try:
        uvicorn.run(**uviconfig)
    except Exception as e:
        print("Unable to run server.", e)
