import random
from maze import MazeGenerator


def How_Many_walls(cell: MazeGenerator.Cell) -> int:
    tot = 0
    if cell.Top:
        tot += 1
    if cell.Bottom:
        tot += 1
    if cell.Right:
        tot += 1
    if cell.Left:
        tot += 1

    return tot


def remove_walls(
        grid: list[list[MazeGenerator.Cell]]
        ) -> list[list[MazeGenerator.Cell]]:

    '''Open random walls to make the maze imperfect'''

    rows = len(grid)
    columns = len(grid[0])

    for row in grid:
        for cell in row:
            tot_walls = How_Many_walls(cell)
            if tot_walls != 3 or cell.Lock:
                continue

            walls = []
            if (
                cell.Row > 0 and cell.Top
                and not grid[cell.Row - 1][cell.Column].Lock
            ):
                walls.append("Top")
            if (
                cell.Row < rows - 1 and cell.Bottom
                and not grid[cell.Row + 1][cell.Column].Lock
            ):
                walls.append("Bottom")
            if (
                cell.Column > 0 and cell.Left
                and not grid[cell.Row][cell.Column - 1].Lock
            ):
                walls.append("Left")
            if (
                cell.Column < columns - 1 and cell.Right
                and not grid[cell.Row][cell.Column + 1].Lock
            ):
                walls.append("Right")

            if not walls:
                continue

            random_wall = random.choice(walls)
            if random_wall == "Top":
                cell.Top = False
                grid[cell.Row - 1][cell.Column].Bottom = False

            elif random_wall == "Bottom":
                cell.Bottom = False
                grid[cell.Row + 1][cell.Column].Top = False

            elif random_wall == "Left":
                cell.Left = False
                grid[cell.Row][cell.Column - 1].Right = False

            elif random_wall == "Right":
                cell.Right = False
                grid[cell.Row][cell.Column + 1].Left = False

    return grid


def check_again(
        grid: list[list[MazeGenerator.Cell]]
        ) -> list[list[MazeGenerator.Cell]]:

    imperfect = []
    for row in grid:
        for cell in row:
            if How_Many_walls(cell) == 3:
                imperfect.append(cell)

    for i in imperfect:
        if i.Top and i.Right:
            if not grid[i.Row][i.Column - 1].Lock:
                grid[i.Row][i.Column].Left = False
                grid[i.Row][i.Column - 1].Right = False

            if not grid[i.Row + 1][i.Column].Lock:
                grid[i.Row][i.Column].Bottom = False
                grid[i.Row + 1][i.Column].Top = False

        if i.Left and i.Bottom:
            if not grid[i.Row][i.Column + 1].Lock:
                grid[i.Row][i.Column].Right = False
                grid[i.Row][i.Column + 1].Left = False

            if not grid[i.Row - 1][i.Column].Lock:
                grid[i.Row][i.Column].Top = False
                grid[i.Row - 1][i.Column].Bottom = False

        if i.Left and i.Right:
            if not grid[i.Row + 1][i.Column].Lock:
                grid[i.Row][i.Column].Bottom = False
                grid[i.Row + 1][i.Column].Top = False

            if not grid[i.Row - 1][i.Column].Lock:
                grid[i.Row][i.Column].Top = False
                grid[i.Row - 1][i.Column].Bottom = False

        if i.Top and i.Left:
            if not grid[i.Row + 1][i.Column].Lock:
                grid[i.Row][i.Column].Bottom = False
                grid[i.Row + 1][i.Column].Top = False

            if not grid[i.Row][i.Column + 1].Lock:
                grid[i.Row][i.Column].Right = False
                grid[i.Row][i.Column + 1].Left = False
        if i.Top and i.Bottom:
            if not grid[i.Row][i.Column + 1].Lock:
                grid[i.Row][i.Column].Right = False
                grid[i.Row][i.Column + 1].Left = False

            if not grid[i.Row][i.Column - 1].Lock:
                grid[i.Row][i.Column].Left = False
                grid[i.Row][i.Column - 1].Right = False

        if i.Right and i.Bottom:
            if not grid[i.Row - 1][i.Column].Lock:
                grid[i.Row][i.Column].Top = False
                grid[i.Row - 1][i.Column].Bottom = False

            if not grid[i.Row][i.Column - 1].Lock:
                grid[i.Row][i.Column].Left = False
                grid[i.Row][i.Column - 1].Right = False

    return grid
