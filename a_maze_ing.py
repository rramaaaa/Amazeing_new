import sys
import os
import random
from parsing import read_config, Check_Corners, Check_not_in_lock
from maze import MazeGenerator
from maze_printer import Maze_Printer, Maze_Printer_withPath
from fortytwo_lock import FortyTwo_Lock, FortyTwo_Check
from shortest_path import Finding_shortest_path
from hexa_output import Output_Maze
from imperfect import remove_walls, check_again


def call_maze(
        rows: int, columns: int, perfect: bool,
        entry: tuple[int, int], ext: tuple[int, int],
        colors: list[str], config: dict[str, str],
        seed: int | None = None,
        small: bool = False
        ) -> list[list[MazeGenerator.Cell]]:

    '''To create maze'''

    entry_row, entry_column = entry
    exit_row, exit_column = ext

    if small:
        print("Maze size is too small")
        obj = MazeGenerator()
        grid = obj.Create_Grid(rows, columns)
        grid = obj.Generate_Maze(grid, perfect, seed)
        if not perfect:
            grid = remove_walls(grid)
            # grid = check_again(grid)
        Maze_Printer(grid, rows, columns, entry, ext, colors)
        Output_Maze(grid, config["output_file"], entry, ext)
    else:
        obj = MazeGenerator()
        grid = obj.Create_Grid(rows, columns)
        grid = FortyTwo_Lock(grid, rows, columns)
        Check_not_in_lock(
            grid,
            int(entry_row), int(entry_column),
            int(exit_row), int(exit_column)
            )
        grid = obj.Generate_Maze(grid, perfect, seed)
        grid = FortyTwo_Check(grid, rows, columns)
        if not perfect:
            grid = remove_walls(grid)
            # grid = check_again(grid)
        Maze_Printer(grid, rows, columns, entry, ext, colors)
        Output_Maze(grid, config["output_file"], entry, ext)

    return grid


def menu(input_num: int, config: dict[str, str],
         rows: int, columns: int,
         maze: list[list[MazeGenerator.Cell]],
         show_path: bool, entry: tuple[int, int],
         ext: tuple[int, int], perfect: bool, small: bool = False,
         seed: int | None = None
         ) -> list[list[MazeGenerator.Cell]]:

    '''handle the user's choice'''

    entry_row, entry_column = entry
    exit_row, exit_column = ext

    if input_num == 1:
        # colors = ["\033[38;2;181;235;237m", "\033[38;2;245;230;168m"]
        colors = ["\033[38;2;255;0;0m", "\033[38;2;255;255;255m"]

        os.system("clear")
        grid = call_maze(
            rows, columns,
            perfect, entry, ext,
            colors, config, seed, small
            )
        print()
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        return grid

    elif input_num == 2:
        os.system("clear")
        # colors = ["\033[38;2;181;235;237m", "\033[38;2;245;230;168m"]
        colors = ["\033[38;2;255;0;0m", "\033[38;2;255;255;255m"]

        if show_path:
            path, _ = Finding_shortest_path(maze, entry, ext)
            '''if not perfect:
                maze = remove_walls(maze)
                maze = check_again(maze)'''
            Maze_Printer_withPath(
                maze,
                rows, columns,
                entry, ext,
                colors, path)
            Output_Maze(maze, config["output_file"], entry, ext)

        else:
            Maze_Printer(maze, rows, columns, entry, ext, colors)
            Output_Maze(maze, config["output_file"], entry, ext)

        print()
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

    elif input_num == 3:
        os.system("clear")
        all_colors = [
            ["\033[38;2;243;182;210m", "\033[38;2;181;235;237m"],
            ["\033[38;2;197;179;230m", "\033[38;2;181;235;237m"],
            ["\033[38;2;154;255;155m", "\033[38;2;245;230;168m"],
            ["\033[38;2;181;235;237m", "\033[38;2;243;182;210m"],
            ["\033[38;2;85;191;194m", "\033[38;2;181;235;237m"],
            ["\033[38;2;141;216;232m", "\033[38;2;245;230;168m"],
            ["\033[38;2;243;182;210m", "\033[38;2;245;230;168m"],
            ["\033[38;2;181;235;237m", "\033[38;2;245;230;168m"]
        ]

        colors = random.choice(all_colors)
        if show_path:
            path, _ = Finding_shortest_path(maze, entry, ext)
            '''if not perfect:
                maze = remove_walls(maze)
                maze = check_again(maze)'''
            Maze_Printer_withPath(maze,
                                  rows, columns,
                                  entry, ext,
                                  colors, path)
            Output_Maze(maze, config["output_file"], entry, ext)

        else:
            '''if not perfect:
                maze = remove_walls(maze)
                maze = check_again(maze)'''
            Maze_Printer(maze, rows, columns, entry, ext, colors)
            Output_Maze(maze, config["output_file"], entry, ext)

        print()
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

    elif input_num == 4:
        Output_Maze(maze, config["output_file"], entry, ext)
        print("Quitting the Maze!")
        exit()

    else:
        print("Please choice number (1-4)!")

    return maze


def main() -> None:
    '''to run the program and generate the maze'''
    try:
        file_name = sys.argv[1]
        config = read_config(file_name)

        if "seed" in config:
            seed = int(config["seed"])
        else:
            seed = None
        try:
            columns = int(config["width"])
            rows = int(config["height"])
            try:
                entry_row, entry_column = config["entry"].split(",")
                exit_row, exit_column = config["exit"].split(",")
            except ValueError:
                raise ValueError(
                    "Enter a correct format (ENTRY or EXIT)=(value,value)"
                    )

        except ValueError:
            raise ValueError("please enter only numbers")
        if columns < 0 or rows < 0:
            raise ValueError("Enter only positive values!")

        value_perfect = config["perfect"]
        if value_perfect == "true":
            perfect = True
        elif value_perfect == "false":
            perfect = False
        else:
            raise ValueError(
                "Insert (True) for perfect, (False) for imperfect!"
                )
        entry = (int(entry_row), int(entry_column))
        ext = (int(exit_row), int(exit_column))
        Check_Corners(rows, columns,
                      int(entry_row), int(entry_column),
                      int(exit_row), int(exit_column)
                      )

        if rows < 4 or columns < 4:
            raise ValueError(
                "Maze size is too small!\n"
                "Please enter height and width values larger than 4"
            )
        if rows > 50 or columns > 50:
            raise ValueError(
                "Maze size is too large!\n"
                "Please enter height and width values smaller than 50"
                )

        else:
            # colors = ["\033[38;2;181;235;237m", "\033[38;2;245;230;168m"]
            colors = ["\033[38;2;255;0;0m", "\033[38;2;255;255;255m"]

            if rows < 12 or columns < 10:

                small = True
                print("Maze size is too small")
                obj = MazeGenerator()
                grid = obj.Create_Grid(rows, columns)
                grid = obj.Generate_Maze(grid, perfect, seed)
                if not perfect:
                    grid = remove_walls(grid)
                    grid = check_again(grid)
                Maze_Printer(grid, rows, columns, entry, ext, colors)
                Output_Maze(grid, config["output_file"], entry, ext)
                print("=== A-Maze-ing ===")
                print("1. Re-generate a new maze")
                print("2. Show/Hide path from entry to exit")
                print("3. Rotate maze colors")
                print("4. Quit")

                path = False
                while True:
                    try:
                        try:
                            ent = int(input("Choice? (1-4): "))
                        except ValueError:
                            raise ValueError("Please enter a number")
                        if ent == 2:
                            if path:
                                path = False
                            else:
                                path = True
                        if ent == 1:
                            grid = menu(
                                ent, config,
                                rows, columns,
                                grid, path,
                                entry, ext, perfect,
                                small
                                )
                        else:
                            menu(
                                ent, config,
                                rows, columns,
                                grid, path,
                                entry, ext, perfect,
                                small
                                )
                        # Output_Maze(grid, config["output_file"], entry, ext)

                    except KeyboardInterrupt:
                        raise KeyboardInterrupt("")

            obj = MazeGenerator()
            grid = obj.Create_Grid(rows, columns)
            grid = FortyTwo_Lock(grid, rows, columns)
            Check_not_in_lock(grid,
                              int(entry_row), int(entry_column),
                              int(exit_row), int(exit_column)
                              )
            grid = obj.Generate_Maze(grid, perfect, seed)
            grid = FortyTwo_Check(grid, rows, columns)
            if not perfect:
                grid = remove_walls(grid)
                grid = check_again(grid)
            grid = FortyTwo_Check(grid, rows, columns)
            Maze_Printer(grid,
                         rows, columns,
                         entry, ext, colors)
            Output_Maze(grid, config["output_file"], entry, ext)
            print()
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")

            path = False
            while True:
                try:
                    try:
                        ent = int(input("Choice? (1-4): "))
                    except ValueError:
                        raise ValueError("Please enter a number")
                    if ent == 2:
                        if path:
                            path = False
                        else:
                            path = True
                    if ent == 1:
                        grid = menu(
                            ent, config,
                            rows, columns,
                            grid, path,
                            entry, ext, perfect
                            )
                    else:
                        menu(
                            ent, config,
                            rows, columns,
                            grid, path,
                            entry, ext, perfect
                            )

                    # Output_Maze(grid, config["output_file"], entry, ext)

                except KeyboardInterrupt:
                    raise KeyboardInterrupt("")

                # Output_Maze(grid, config["output_file"], entry, ext)

    except KeyboardInterrupt:
        print("\nQuitting the Maze!")
    except Exception as e:
        print(e)


main()
