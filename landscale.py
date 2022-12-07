import random

from numpy import floor
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt

class Map(object):
    def __init__(self, seed):
        self.seed = seed
        self.noise = PerlinNoise(octaves=1, seed=self.seed)
        self.amp = 8
        self.freq = 24
        self.terrain_width = 128
        self.levels = 10

        self.landscale_mask = [[0 for i in range(self.terrain_width)] for i in range(self.terrain_width)]
        self.mine_mask = [0 for level in range(self.levels)]

        self.__landscale()
        #self.__mine()

    def __landscale(self):
        for position in range(self.terrain_width ** 2):
            x = floor(position / self.terrain_width)
            z = floor(position % self.terrain_width)
            y = floor(self.noise([x / self.freq, z / self.freq]) * self.amp)

            self.landscale_mask[int(x)][int(z)] = int(y)

    def __mine(self):
        for level in range(self.levels):
            local_mask = [[0 for i in range(self.terrain_width)] for i in range(self.terrain_width)]
            for position in range(self.terrain_width ** 2):
                koef = 0.9 + 0.1*level
                x = floor(position / self.terrain_width)
                z = floor(position % self.terrain_width)
                y = floor(self.noise([x / (self.freq * koef), z / (self.freq * koef)]) * (self.amp))
                if y > 0:
                    y = 0
                elif y < 0:
                    y = -1

                local_mask[int(x)][int(z)] = int(y)
                self.mine_mask[level] = local_mask

map = Map(2325)