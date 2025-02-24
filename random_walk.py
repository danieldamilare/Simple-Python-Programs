import random
import matplotlib.pyplot as plt
from typing import List

class Location:
    def __init__(self, x_loc: int, y_loc: int):
        self.x_loc = x_loc
        self.y_loc = y_loc
    def move(self, delta_x, delta_y):
        return Location(self.x_loc + delta_x, self.y_loc + delta_y)

    def get_y(self):
        return self.y_loc

    def get_x(self):
        return self.x_loc

    def dist_from(self, other: 'Location'):
        ox, oy = other.x_loc, other.y_loc
        x_dist, y_dist = self.x_loc - ox, self.y_loc - oy
        return (x_dist**2 + y_dist**2) ** 0.5

    def __str__(self):
        return f'<{self.x_loc}, {self.y_loc}>'

class Field:
    def __init__(self):
        self.drunks = {}

    def add_drunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError("Duplicate drunk")
        else:
            self.drunks[drunk] = loc

    def move_drunk(self, drunk):
        if drunk not in self.drunks:
            raise ValueError("Drunk not in field")
        x_dist, y_dist = drunk.take_step()
        current_location: 'Location' = self.drunks[drunk]
        self.drunks[drunk] = current_location.move(x_dist, y_dist)

    def get_loc(self, drunk):
        if drunk not in self.drunks:
            raise ValueError("Drunk not in field")
        return self.drunks[drunk]

class OddField(Field):
    def __init__(self, numHoles, x_range, y_range):
        super().__init__()
        self.wormholes = {}
        for i in range(numHoles):
            x, y = random.randint(-x_range, x_range), random.randint(-y_range, y_range)
            newx = random.randint(-x_range, x_range)
            newy = random.randint(-y_range, y_range)
            self.wormholes[(x, y)] = Location(newx, newy)

    def move_drunk(self, drunk):
        super().move_drunk(drunk)
        x = self.drunks[drunk].get_x()
        y = self.drunks[drunk].get_y()
        if (x, y) in self.wormholes:
            self.drunks[drunk] = self.wormholes[(x, y)]


class Drunk:
    def __init__(self, name = None):
        self.name = name

    def __str__(self):
        return self.name

    def take_step(self):
        pass


class Usual_drunk(Drunk):
    def take_step(self):
        step_choices = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        return random.choice(step_choices)

class Cold_drunk(Drunk):
    def take_step(self):
        step_choices = [(0.0, 1.0), (0, -2.0), (-1, 0), (1, 0)]
        return random.choice(step_choices)

class EW_drunk(Drunk):
    def take_step(self):
        step_choices = [(-1, 0), (1, 0)]
        return random.choice(step_choices)

class style_iterator:
    def __init__(self, styles):
        self.index = 0
        self.styles = styles

    def next_style(self):
        result = self.styles[self.index]
        self.index += 1
        if  self.index >= len(self.styles):
            self.index = 0
        return result

def walk(f: Field, d: Drunk, num_steps: int):
    start = f.get_loc(d)
    for s in range(num_steps):
        f.move_drunk(d)
    return start.dist_from(f.get_loc(d))

def sim_walks(num_steps: int, num_trials: int, d_class: Drunk):
    Homer = d_class("Homer")
    origin = Location(0, 0)
    distances = []
    for t in range(num_trials):
        f = Field()
        f.add_drunk(Homer, origin)
        distances.append(round(walk(f, Homer, num_steps), 1))
    return distances


def drunk_test(walk_lengths: List[int], num_trials: int, d_class: Drunk):
    for num_steps in walk_lengths:
        distances = sim_walks(num_steps, num_trials, d_class)
        # print("distances", distances)
        print(d_class.__name__, 'Walk of', num_steps, 'steps: Mean =', 
              f'{sum(distances)/ len(distances):.3f}), Max =',
              f'{max(distances)}, Min = {min(distances)}')

def plot_drunk(walk_lengths: List[int], num_trials: int, d_class: Drunk):
    mean_distance = []
    mean_square_root = []

    for num_steps in walk_lengths:
        distances = sim_walks(num_steps, num_trials, d_class)
        distances_sqrt = sim_walks(int(num_steps**0.5), num_trials, d_class)
        mean_distance.append(sum(distances)/len(distances))
        mean_square_root.append(sum(distances_sqrt)/len(distances_sqrt))

    plt.figure("Drunkard Walk")
    plt.title(f"Mean Distance from Origin ({num_trials} trials)")
    plt.ylabel('Distance from Origin')
    plt.xlabel("Number of step")
    # plt.grid(True, which='both')
    plt.xscale('log')
    plt.yscale('log')

    plt.plot(walk_lengths, mean_distance, 'b--', label='Usual Drunk')
    walk_sqrt_lengths = [int(x**0.5) for x in walk_lengths]

    plt.plot(walk_lengths, mean_square_root, 'r', linewidth=1, label='sqrt(steps)')
    plt.legend()
    plt.show()

def get_final_locs(num_steps, num_trials, d_class):
    locs = []
    d = d_class()
    for t in range(num_trials):
        f = Field()
        f.add_drunk(d, Location(0, 0))

        for s in range(num_steps):
            f.move_drunk(d)
        locs.append(f.get_loc(d))
    return  locs

def plot_locs(drunk_kinds, num_steps, num_trials):
    style = style_iterator(('k+', 'r^', 'mo'))
    for d_class in drunk_kinds:
        locs = get_final_locs(num_steps, num_trials, d_class)
        x_vals = [x.get_x() for x in locs]
        y_vals = [y.get_y() for y in locs]
        meanx = sum(x_vals)/len(x_vals)
        meany = sum(y_vals)/len(y_vals)

        print("Class:", d_class.__name__)
        print(f"Meanx: {meanx} Meany: {meany}")

        cur_style = style.next_style()
        plt.plot(x_vals, y_vals, cur_style,
                 label = (f'{d_class.__name__} mean loc. = <' + 
                          f' {meanx}, {meany}>'))
        plt.title(f'location at End of Walks ({num_steps} steps)')
        plt.xlabel('Steps East/West of Origin')
        plt.ylabel('Steps North/South of Origin')
        plt.legend(loc = 'best')
    plt.show()


def trace_walk(drunk_kinds, num_steps):
    style_choice = style_iterator(('k+', 'r^', 'mo'))
    f = OddField(1000, 100, 200)
    for d_class in drunk_kinds:
        d = d_class()
        f.add_drunk(d, Location(0, 0))
        locs = []
        for x in range(num_steps):
            f.move_drunk(d)
            locs.append(f.get_loc(d))
        x_vals = [x.get_x() for x in locs]
        y_vals = [y.get_y() for y in locs]
        cur_style =  style_choice.next_style()
        plt.plot(x_vals, y_vals, cur_style, label = d_class.__name__)
    plt.title("Spots Visited on Walk (" +
                  str(num_steps) + ' steps)')

    plt.xlabel("Steps East/West of Origin")
    plt.xlabel("Steps North/South of Origin")
    plt.legend(loc = 'best')
    plt.show()

if __name__ == "__main__":
    # plot_locs((Cold_drunk, EW_drunk, Usual_drunk), 100, 200)
    trace_walk((Usual_drunk, Cold_drunk, EW_drunk), 500)
