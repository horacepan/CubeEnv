'''
Source implementation: https://github.com/zamlz/dlcampjeju2018-I2A-cube.git
'''
import pdb
import resource
import time
import random
import os
import numpy as np
import argparse
import sys
from termcolor import colored

RIGHT = -1
LEFT = 0
TOP = 0
BOT = -1

BLANKTILE = '   '
TILE = ' + '
COLORDICT = {
    'W': 'white',
    'R': 'red',
    'G': 'green',
    'Y': 'yellow',
    'B': 'blue',
    'M': 'magenta', # no orange?!
}
TILES = np.array([[0, 1, 2], [3, 4,5], [6, 7, 8]])

FACES = ['u', 'd', 'l', 'r', 'f', 'b']
ACTIONS = [
    'u', 'd', 'l', 'r', 'f', 'b', 'u\'', 'd\'', 'l\'', 'r\'', 'f\'', 'b\''
]

class Cube:
    def __init__(self, size=3):
        self.size = size
        self.u = np.array([['G' for _ in range(size)] for _ in range(size)])
        self.d = np.array([['B' for _ in range(size)] for _ in range(size)])
        self.l = np.array([['R' for _ in range(size)] for _ in range(size)])
        self.r = np.array([['M' for _ in range(size)] for _ in range(size)])
        self.f = np.array([['W' for _ in range(size)] for _ in range(size)])
        self.b = np.array([['Y' for _ in range(size)] for _ in range(size)])

    def reset(self):
        self.u = np.array([['G' for _ in range(self.size)] for _ in range(self.size)])
        self.d = np.array([['B' for _ in range(self.size)] for _ in range(self.size)])
        self.l = np.array([['R' for _ in range(self.size)] for _ in range(self.size)])
        self.r = np.array([['M' for _ in range(self.size)] for _ in range(self.size)])
        self.f = np.array([['W' for _ in range(self.size)] for _ in range(self.size)])
        self.b = np.array([['Y' for _ in range(self.size)] for _ in range(self.size)])

    def render(self, _ascii=False):
        if _ascii:
            pass
        else:
            # top portion
            for row in range(self.size):
                self.render_face()
                sys.stdout.write(' ')
                self.render_face('u', row)
                self.render_face()
                sys.stdout.write('\n')

            sys.stdout.write('\n')
            # mid portion
            for row in range(self.size):
                self.render_face('l', row)
                sys.stdout.write(' ')
                self.render_face('f', row)
                sys.stdout.write(' ')
                self.render_face('r', row)
                sys.stdout.write(' ')
                self.render_face('b', row)
                sys.stdout.write('\n')

            sys.stdout.write('\n')

            # bot portion
            for row in range(self.size):
                self.render_face()
                sys.stdout.write(' ')
                self.render_face('d', row)
                self.render_face()
                sys.stdout.write('\n')

    def get_face(self, face_orientation):
        pass

    def render_face(self, face_orientation=None, row=0):
        # renders a single row of the given face
        # we render row by row b/c we need to render the row of a whole bunch of faces
        # before getting to the next line for the middle section(left, front, right, back)
        if face_orientation is None:
            for i in range(self.size):
                sys.stdout.write(BLANKTILE)
        else:
            _face = getattr(self, face_orientation)
            for i in range(self.size):
                color = _face[row][i]
                coloredtile = colored(TILE, COLORDICT[color], attrs=['reverse'])
                sys.stdout.write(coloredtile)

    def rot_u(self):
        new_colors = (
            tuple(self.r[TOP, :]),
            tuple(self.f[TOP, :]),
            tuple(self.l[TOP, :]),
            tuple(self.b[TOP, :])
        )
        self.f[TOP, :] = new_colors[0]
        self.l[TOP, :] = new_colors[1]
        self.b[TOP, :] = new_colors[2]
        self.r[TOP, :] = new_colors[3]

    def rot_d(self):
        new_colors = (
            tuple(self.r[BOT, :]),
            tuple(self.f[BOT, :]),
            tuple(self.l[BOT, :]),
            tuple(self.b[BOT, :])
        )
        self.f[BOT, :] = new_colors[0]
        self.l[BOT, :] = new_colors[1]
        self.b[BOT, :] = new_colors[2]
        self.r[BOT, :] = new_colors[3]

    def rot_r(self):
        new_colors = (
            tuple(self.d[:, RIGHT]),
            tuple(self.f[:, RIGHT]),
            tuple(reversed(self.u[:, RIGHT])),
            tuple(reversed(self.b[:, LEFT]))
        )
        # thats just the colors!
        self.f[:, RIGHT] = new_colors[0]
        self.u[:, RIGHT] = new_colors[1]
        self.b[:, LEFT]  = new_colors[2]
        self.d[:, RIGHT] = new_colors[3]

    def rot_l(self):
        new_colors = (
            tuple(self.d[:, LEFT]),
            tuple(self.f[:, LEFT]),
            tuple(reversed(self.u[:, LEFT])),
            tuple(reversed(self.b[:, RIGHT]))
        )
        self.f[:, LEFT] = new_colors[0]
        self.u[:, LEFT] = new_colors[1]
        self.b[:, RIGHT]  = new_colors[2]
        self.d[:, LEFT] = new_colors[3]

    def rot_f(self):
        new_colors = (
            tuple(self.l[:, RIGHT]),
            tuple(self.u[BOT, :]),
            tuple(reversed(self.r[:, LEFT])),
            tuple(self.d[TOP, :])
        )
        self.u[BOT, :] = new_colors[0]
        self.r[:, LEFT] = new_colors[1]
        self.d[TOP, :]  = new_colors[2]
        self.l[:, RIGHT] = new_colors[3]

    def rot_b(self):
        new_colors = (
            tuple(self.r[:, RIGHT]),
            tuple(reversed(self.u[TOP, :])),
            tuple(self.l[:, LEFT]),
            tuple(reversed(self.d[BOT, :]))
        )
        self.u[TOP, :] = new_colors[0]
        self.l[:, LEFT] = new_colors[1]
        self.d[BOT, :]  = new_colors[2]
        self.r[:, RIGHT] = new_colors[3]

    def get_face(self, face_char):
        if face_char == 'u':
            return self.u
        elif face_char == 'd':
            return self.d
        elif face_char == 'l':
            return self.l
        elif face_char == 'r':
            return self.r
        elif face_char == 'f':
            return self.f
        elif face_char == 'b':
            return self.b
        else:
            raise ValueError('Not a valid face orientation')

    def rotate(self, face):
        # TODO: should probably avoid doing the copy
        # TODO: inverse moves
        # TODO: using setattr is a little gross...
        _face = getattr(self, face)
        rotated_face = np.rot90(_face, axes=(1,0)) # this needs to act on self.u/d/l/r/f/b
        setattr(self, face, rotated_face)

        if face is 'u':
            self.rot_u()
        elif face is 'd':
            self.rot_d()
        elif face is 'l':
            self.rot_l()
        elif face is 'r':
            self.rot_r()
        elif face is 'f':
            self.rot_f()
        elif face is 'b':
            self.rot_b()


    def step(self, moves):
        for m in moves:
            self.rotate(m)

def benchmark(n_moves):
    cube = Cube(3)
    start = time.time()
    for _ in range(n_moves):
        face = random.choice(FACES)
        cube.rotate(face)
    end = time.time() - start

    print('Scrambles: {}'.format(n_moves))
    print("Elapsed: {:.2f}".format(end))
    print("Consumed {}mb memory".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1024.0 * 1024.0)))

if __name__ == '__main__':
    n_moves = int(sys.argv[1])
    benchmark(n_moves)
