import numpy as np

from pyics import Model
import random

import matplotlib
import matplotlib.pyplot as plt



class CASim(Model):
    def __init__(self):
        Model.__init__(self)

        self.t = 0
        self.grid = None

        self.make_param('width', 256)
        self.make_param('height', 256)
        self.make_param('percentage_trees', 0.5) 
        self.make_param('amount_of_states', 4)

        self.cmap = matplotlib.colors.ListedColormap(['white', 'green', 'black', 'red'])

    def setup_initial_grid(self):
        """
        0: empty
        1: Tree
        2: Burned Tree
        3: Burning

        """
        
        self.grid = np.zeros([self.height, self.width])
        self.grid[:,0] = 3

        for i in range(self.height):
            for j in range(1, self.width):
                if random.random() <= self.percentage_trees:
                    self.grid[i,j] = 1
                else:
                    self.grid[i,j] = 0

        self.amount_initial_trees = np.count_nonzero(self.grid == 1)


    def check_rule(self):

        grid_copy = self.grid.copy()

        indices = np.where(grid_copy == 3)
        for index in range(len(indices[0])):
            i = indices[0][index]
            j = indices[1][index]

            # blocking boundary conditions
            if i - 1 >= 0 and grid_copy[i - 1, j] == 1:
                self.grid[i - 1, j] = 3
            if i + 1 <= self.height - 1 and grid_copy[i + 1, j] == 1:
                self.grid[i + 1, j] = 3
            if j - 1 >= 0 and grid_copy[i, j - 1] == 1:
                self.grid[i, j - 1] = 3
            if j + 1 <= self.width - 1 and grid_copy[i, j + 1] == 1:
                self.grid[i, j + 1] = 3
                

            self.grid[i,j] = 2



    def reset(self):
        """Initializes the configuration of the cells and converts the entered
        rule number to a rule set."""

        self.t = 0
        self.setup_initial_grid()


    def draw(self):
        """Draws the current state of the grid."""

        amount_trees = np.count_nonzero(self.grid == 1)
        percentage_burned = round((1 - amount_trees / self.amount_initial_trees), 3) * 100

        plt.cla()
        if not plt.gca().yaxis_inverted():
            plt.gca().invert_yaxis()
        plt.imshow(self.grid, interpolation='none', vmin=0, vmax=self.amount_of_states - 1,
                cmap=self.cmap)
        plt.axis('image')
        plt.title(f't = {self.t} \npercentage burned = {percentage_burned}%')

    def step(self):
        """Performs a single step of the simulation by advancing time (and thus
        row) and applying the rule to determine the state of the cells."""
        self.t += 1
        if 3 not in self.grid:
            return True

        self.check_rule()


if __name__ == '__main__':
    sim = CASim()
    from pyics import GUI
    cx = GUI(sim)
    cx.start()
