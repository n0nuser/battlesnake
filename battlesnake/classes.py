from pydantic import BaseModel
from typing import List


class _Squad(BaseModel):
    allowBodyCollisions: bool
    # Allow members of the same squad to move over each other without dying

    sharedElimination: bool
    # All squad members are eliminated when one is eliminated

    sharedHealth: bool
    # All squad members share health.

    sharedLength: bool
    # All squad members share length


class _Royale(BaseModel):
    shrinkEveryNTurns: int
    # The number of turns between generating new hazards
    # Shrinks the safe board space


class _RuleSetSettings(BaseModel):
    foodSpawnChance: int
    # Percentage chance of spawning a new food every round

    minimumFood: int
    # Minimum food to keep on the board every turn

    hazardDamagePerTurn: int
    # Health damage a snake will take when ending its turn in a hazard.
    # This stacks on top of the regular 1 damage a snake takes per turn.

    royale: _Royale
    # Royale Mode settings

    squad: _Squad
    # Squad Mode settings


class RuleSet(BaseModel):
    name: str
    # Name of the ruleset being used to run this game

    version: str
    # The release version of the Rules module used in this game

    settings: _RuleSetSettings
    # A collection of specific settings being used by the current game that control how the rules are applied


class Game(BaseModel):
    id: str
    # A unique identifier for this Game

    ruleset: RuleSet
    # Information about the ruleset being used

    map: str
    # Name of the map used to populate the game board with snakes, food, and hazards

    timeout: int
    # How much time your snake has to respond to requests for this Game

    source: str
    # [tournament, league, arena, challenge, custom]


class Coordinate(BaseModel):
    x: int
    y: int


class _Customizations(BaseModel):
    color: str
    #

    head: str
    # The URL of the head image for this snake

    tail: str
    # The URL of the tail image for this snake


class Snake(BaseModel):
    id: str
    # Unique identifier for this Battlesnake in the context of the current Game

    name: str
    # Name given to this Battlesnake by its author

    health: int
    # Health value of this Battlesnake, between 0 and 100 inclusively

    body: List[Coordinate]
    # Array of coordinates representing this Battlesnake's location on the game board
    # This array is ordered from head to tail

    latency: str
    # The previous response time of this Battlesnake, in milliseconds

    head: Coordinate
    # Coordinates for this Battlesnake's head
    # Equivalent to the first element of the body array

    length: int
    # Length of this Battlesnake from head to tail.
    # Equivalent to the length of the body array

    shout: str
    # Message shouted by this Battlesnake on the previous turn

    squad: str
    # The squad that the Battlesnake belongs to

    customizations: _Customizations
    # The collection of customizations applied to this Battlesnake


class Board(BaseModel):
    height: int
    # The number of rows in the y-axis of the game board

    width: int
    # The number of columns in the x-axis of the game board

    food: List[Coordinate]
    # Array of coordinates representing food locations on the game board

    hazards: List[Coordinate]
    # Array of coordinates representing hazardous locations on the game board

    snakes: List[Snake]
    # Array of Battlesnake Objects representing all Battlesnakes remaining on the game board
    # Including yourself if you haven't been eliminated


class Request(BaseModel):
    game: Game
    turn: int
    board: Board
    you: Snake
