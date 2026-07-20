import random
from src.generator.maze_generator import MazeGenerator

def display(maze: MazeGenerator) -> None:
        RESET = "\033[0m"
        WALL_COLORS = [
            "\033[90m",
            "\033[30m",
            "\033[31m",
            "\033[33m"
                    ]
        LOGO_COLORS = [
            "\033[1;96m",
            "\033[1;92m",
            "\033[1;93m"
            "\033[1;97m"
        ]
        SPACE = "  "
        wall_color = random.choice(WALL_COLORS)
        logo_color = random.choice(LOGO_COLORS)
        WALL = f"{wall_color}██{RESET}"
        LOGO = f"{logo_color}██{RESET}"

        print(WALL * (maze.width * 2 + 1))
        for row in maze.grid:
            line = WALL
            for cell in row:
                if cell.is_logo:
                    line += LOGO
                else:
                    line += SPACE
                if cell.walls['E']:
                    line += WALL
                else:
                    line += SPACE
            print(line)

            line = WALL
            for cell in row:
                if cell.walls['S']:
                    line += WALL
                else:
                    line += SPACE
                line += WALL
            print(line)
