import heapq
from battlesnake.classes import Coordinate, Board
from typing import List, Tuple, Union


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


def get_board_as_maze(board: Board, hazards: bool = True, snakes: bool = True, food: bool = False) -> List[List[int]]:
    maze = [[0 for _ in range(board.width)] for _ in range(board.height)]
    if hazards:
        for hazard in board.hazards:
            index = get_index(hazard, board)
            maze[index % board.width][index // board.width] = 1
    if snakes:
        for snake in board.snakes:
            for coordinate in snake.body:
                index = get_index(coordinate, board)
                maze[index % board.width][index // board.width] = 1
    if food:
        for food in board.food:
            index = get_index(food, board)
            maze[index % board.width][index // board.width] = 1
    return maze


class Node:
    """
    A node class for A* Pathfinding.
    """

    def __init__(self, parent=None, position: Tuple[int, int] = None):
        self.parent = parent
        self.position: tuple[int, int] = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f

    # defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f


def return_path(current_node: Node) -> Tuple[int, int]:
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def print_board(board: List[List[int]], path: List[Tuple[int, int]] = None):
    if path:
        for step in path:
            board[step[0]][step[1]] = 2

    for row in board:
        line = []
        for col in row:
            if col == 1:
                line.append("\u2588")
            elif col == 0:
                line.append(" ")
            elif col == 2:
                line.append(".")
        print("".join(line))


def astar(maze: List[List[int]], start_coord: Coordinate, end_coord: Coordinate, LOGGER) -> Union[List[Tuple[int, int]], None]:
    """
    Adaptation of https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc
    """

    # Adapt Params to A* algorithm
    start = (start_coord.x, start_coord.y)
    end = (end_coord.x, end_coord.y)

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    max_iterations = len(maze[0]) * len(maze) // 2

    # what squares do we search
    adjacent_squares = (
        (0, -1),
        (0, 1),
        (-1, 0),
        (1, 0),
    )

    # Loop until you find the end
    while open_list:
        outer_iterations += 1

        if outer_iterations > max_iterations:
            # if we hit this point return the path such as it is
            # it will not contain the destination
            LOGGER.warning("Giving up on pathfinding too many iterations")
            path = return_path(current_node)
            print_board(maze, path)
            return path

        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = return_path(current_node)
            print_board(maze, path)
            return path

        # Generate children
        children = []

        for new_position in adjacent_squares:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if (
                node_position[0] > (len(maze) - 1)
                or node_position[0] < 0
                or node_position[1] > len(maze[-1]) - 1
                or node_position[1] < 0
            ):
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child is on the closed list
            if [closed_child for closed_child in closed_list if closed_child == child]:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                (child.position[1] - end_node.position[1]) ** 2
            )
            child.f = child.g + child.h

            # Child is already in the open list
            if child in open_list:
                idx = open_list.index(child)
                if child.g < open_list[idx].g:
                    # update the node in the open list
                    open_list[idx].g = child.g
                    open_list[idx].f = child.f
                    open_list[idx].h = child.h
            else:
                # Add the child to the open list
                heapq.heappush(open_list, child)

    LOGGER.warning("Couldn't get a path to destination")
    return None