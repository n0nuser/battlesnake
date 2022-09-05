from fastapi import FastAPI, Request, status
import uvicorn
from battlesnake.main import info, start, end, move
from battlesnake.classes import Game, Snake, Board
from battlesnake.__version__ import version

from battlesnake.logger import CustomFormatter
import logging

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

api = FastAPI(title="Battlesnake API", version=version)
api.logger = LOGGER


@api.get("/", status_code=status.HTTP_200_OK)
async def on_info(request: Request):
    return info()


@api.post("/start", status_code=status.HTTP_200_OK)
async def on_start(game: Game, board: Board, you: Snake, turn: int = None):
    start(game, turn, board, you, LOGGER)
    return "ok"


@api.post("/move", status_code=status.HTTP_200_OK)
async def on_move(game: Game, board: Board, you: Snake, turn: int = None):
    return move(game, turn, board, you, LOGGER)


@api.post("/end", status_code=status.HTTP_200_OK)
async def on_end(game: Game, board: Board, you: Snake, turn: int = None):
    end(game, turn, board, you, LOGGER)
    return "ok"


def run_server() -> None:
    """Starts the Uvicorn server with the provided configuration."""
    uviconfig = {"app": "api:api", "interface": "asgi3"}
    uviconfig.update(CONFIG)
    LOGGER.info(f"\nRunning Battlesnake at http://{CONFIG.get('host')}:{CONFIG.get('port')}")
    try:
        uvicorn.run(**uviconfig)
    except Exception as e:
        print("Unable to run server.", e)


if __name__ == "__main__":
    run_server()
