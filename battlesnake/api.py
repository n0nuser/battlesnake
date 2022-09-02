from fastapi import FastAPI, Request, status
import uvicorn
from battlesnake.main import info, start, end, move
from battlesnake.classes import Game, Snake, Board

CONFIG = {
    "backlog": 2048,
    "debug": True,
    "host": "0.0.0.0",
    "log_level": "trace",
    "port": 8000,
    "reload": True,
    "timeout_keep_alive": 5,
    "workers": 4,
}

api = FastAPI()


@api.get("/", status_code=status.HTTP_200_OK)
async def on_info(request: Request):
    return info()


@api.post("/start", status_code=status.HTTP_200_OK)
async def on_start(game: Game, board: Board, you: Snake, turn: int = None):
    start(game, turn, board, you)
    return "ok"


@api.post("/move", status_code=status.HTTP_200_OK)
async def on_move(game: Game, board: Board, you: Snake, turn: int = None):
    return move(game, turn, board, you)


@api.post("/end", status_code=status.HTTP_200_OK)
async def on_end(game: Game, board: Board, you: Snake, turn: int = None):
    end(game, turn, board, you)
    return "ok"


def run_server() -> None:
    """Starts the Uvicorn server with the provided configuration."""
    uviconfig = {"app": "api:api", "interface": "asgi3"}
    uviconfig.update(CONFIG)
    print(f"\nRunning Battlesnake at http://{CONFIG.get('host')}:{CONFIG.get('port')}")
    try:
        uvicorn.run(**uviconfig)
    except Exception as e:
        print("Unable to run server.", e)


if __name__ == "__main__":
    run_server()
