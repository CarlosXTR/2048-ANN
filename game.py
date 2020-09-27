import random

import numpy as np

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


class Game2048:

    def __init__(self, grid_height, grid_width):

        self.table = []
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.score = 0
        self.n_actions_space = len(OFFSETS)

        # Compute inital row dictionary to make move code cleaner
        self.initial = {
            UP: [[0, element] for element in range(self.grid_width)],
            DOWN: [[self.grid_height - 1, element] for element in range(self.grid_width)],
            LEFT: [[element, 0] for element in range(self.grid_height)],
            RIGHT: [[element, self.grid_width - 1]
                    for element in range(self.grid_height)]
        }

    def start(self):
        self.table = np.zeros((self.grid_height, self.grid_width))
        self.score = 0

        for _ in range(2):
            self.generate()

    def generate(self):
        if self.empty():
            width = random.randrange(self.grid_width)
            height = random.randrange(self.grid_height)
            while (self.table[height, width] != 0):
                width = random.randrange(self.grid_width)
                height = random.randrange(self.grid_height)

            value = random.randrange(100)

            if value >= 90:
                self.table[height, width] = 4
            else:
                self.table[height, width] = 2

    def merge(self, line):
        # Helper function that merges a single row or column in 2048
        # Move all non-zero values of list to the left
        nonzeros_removed = []
        result = []
        merged = False
        for number in line:
            if number != 0:
                nonzeros_removed.append(number)

        while len(nonzeros_removed) != len(line):
            nonzeros_removed.append(0)

        # Double sequental tiles if same value
        for number in range(0, len(nonzeros_removed) - 1):
            if nonzeros_removed[number] == nonzeros_removed[number + 1] and not merged:
                result.append(nonzeros_removed[number] * 2)
                self.score += nonzeros_removed[number] * 2
                merged = True
            elif nonzeros_removed[number] != nonzeros_removed[number + 1] and not merged:
                result.append(nonzeros_removed[number])
            elif merged:
                merged = False

        if nonzeros_removed[-1] != 0 and not merged:
            result.append(nonzeros_removed[-1])

        while len(result) != len(nonzeros_removed):
            result.append(0)

        return result

    def move_helper(self, initial_list, direction, temporary_list, row_or_column):
        # Move all columns and merge
        before_move = str(self.table)

        for element in initial_list:
            temporary_list.append(element)

            for index in range(1, row_or_column):
                temporary_list.append(
                    [x + y for x, y in zip(temporary_list[-1], OFFSETS[direction])])

            indices = []

            for index in temporary_list:
                indices.append(self.table[index[0], index[1]])

            merged_list = self.merge(indices)

            for index_x, index_y in zip(merged_list, temporary_list):
                self.table[index_y[0], index_y[1]] = index_x

            temporary_list = []

        after_move = str(self.table)

        if before_move != after_move:
            self.generate()

    def move(self, move):
        initial_list = self.initial[move]
        temporary_list = []

        if move == UP:
            self.move_helper(initial_list, move,
                             temporary_list, self.grid_height)
        elif move == DOWN:
            self.move_helper(initial_list, move,
                             temporary_list, self.grid_height)
        elif move == LEFT:
            self.move_helper(initial_list, move,
                             temporary_list, self.grid_width)
        elif move == RIGHT:
            self.move_helper(initial_list, move,
                             temporary_list, self.grid_width)

    def reset(self):
        self.start()
        return np.asarray(self.table).reshape(1,16)

    def step(self, action):
        prevous_score = self.score
        self.move(action)
        reward = self.score - prevous_score
        new_state = np.asarray(self.table).reshape(1,16)

        return new_state, reward**2, self.lost()

    def lost(self):
        gameover = True
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                val = self.table[i, j]
                if val == 0:
                    gameover = False
                if i > 0 and self.table[i - 1, j] == val:
                    gameover = False
                if j > 0 and self.table[i, j - 1] == val:
                    gameover = False
                if i < (self.grid_height-1) and self.table[i + 1, j] == val:
                    gameover = False
                if j < (self.grid_width-1) and self.table[i, j + 1] == val:
                    gameover = False
        return gameover

    def empty(self):
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if self.table[i, j] == 0:
                    return True

        return False

    def print(self):
        print(self.table)
        print("Score: " + str(self.score))


if __name__ == "__main__":

    game = Game2048(4, 4)
    game.start()
    game.print()
    while not game.lost():
        game.move(UP)
        print("UP")
        game.print()
        game.move(DOWN)
        print("DOWN")
        game.print()
        game.move(LEFT)
        print("LEFT")
        game.print()
        game.move(RIGHT)
        print("RIGHT")
        game.print()

    print("LOST")
    # game.print()
    # game.move(UP)
    # game.print()
    # game.move(DOWN)
    # game.print()
    # game.move(LEFT)
    # game.print()
    # game.move(RIGHT)
    # game.print()
    print(game.merge([0, 8, 4, 2]))
