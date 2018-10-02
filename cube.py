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

        # make them all 3x3 for now
        self.tiles = {f: np.array([[0, 1, 2], [3, 4,5], [6, 7, 8]]) for f in FACES}
        self.faces = {
            'u': self.u,
            'd': self.d,
            'l': self.l,
            'r': self.r,
            'f': self.f,
            'b': self.b,
        }

    def reset(self):
        self.u = np.array([['G' for _ in range(self.size)] for _ in range(self.size)])
        self.d = np.array([['B' for _ in range(self.size)] for _ in range(self.size)])
        self.l = np.array([['R' for _ in range(self.size)] for _ in range(self.size)])
        self.r = np.array([['M' for _ in range(self.size)] for _ in range(self.size)])
        self.f = np.array([['W' for _ in range(self.size)] for _ in range(self.size)])
        self.b = np.array([['Y' for _ in range(self.size)] for _ in range(self.size)])
        self.faces = {
            'u': self.u,
            'd': self.d,
            'l': self.l,
            'r': self.r,
            'f': self.f,
            'b': self.b,
        }

        if self.size == 3:
            self.tiles = np.array([[0, 1, 2], [3, 4,5], [6, 7, 8]])
        elif self.size == 4:
            self.tiles = np.array([[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])

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

    def render_face(self, face_orientation=None, row=0):
        # renders a single row of the given face
        # we render row by row b/c we need to render the row of a whole bunch of faces
        # before getting to the next line for the middle section(left, front, right, back)
        if face_orientation is None:
            for i in range(self.size):
                sys.stdout.write(BLANKTILE)
        else:
            _face = self.faces[face_orientation]
            for i in range(self.size):
                color = _face[row][i]
                face_tiles = self.tiles[face_orientation]
                tile = ' {:2s}'.format(str(face_tiles[row, i]))
                coloredtile = colored(TILE, COLORDICT[color], attrs=['reverse'])
                #coloredtile = colored(tile, COLORDICT[color], attrs=['reverse'])
                sys.stdout.write(coloredtile)

    def rot_u(self):
        print('rot u new')
        new_colors = [
            tuple(self.r[TOP, :]),
            tuple(self.f[TOP, :]),
            tuple(self.l[TOP, :]),
            tuple(self.b[TOP, :])
        ]
        self.f[TOP, :] = new_colors[0]
        self.l[TOP, :] = new_colors[1]
        self.b[TOP, :] = new_colors[2]
        pdb.set_trace()
        self.r[TOP, :] = new_colors[3]

    def rot_d(self):
        new_colors = [
            tuple(self.r[BOT, :]),
            tuple(self.f[BOT, :]),
            tuple(self.l[BOT, :]),
            tuple(self.b[BOT, :])
        ]
        self.f[BOT, :] = new_colors[0]
        self.l[BOT, :] = new_colors[1]
        self.b[BOT, :] = new_colors[2]
        self.r[BOT, :] = new_colors[3]

    def rot_r(self):
        new_colors = [
            tuple(self.d[:, RIGHT]),
            tuple(self.f[:, RIGHT]),
            tuple(reversed(self.u[:, RIGHT])),
            tuple(reversed(self.b[:, LEFT]))
        ]
        # thats just the colors!
        self.f[:, RIGHT] = new_colors[0]
        self.u[:, RIGHT] = new_colors[1]
        self.b[:, LEFT]  = new_colors[2]
        self.d[:, RIGHT] = new_colors[3]

    def rot_l(self):
        new_colors = [
            tuple(self.d[:, LEFT]),
            tuple(self.f[:, LEFT]),
            tuple(reversed(self.u[:, LEFT])),
            tuple(reversed(self.b[:, RIGHT]))
        ]
        self.f[:, LEFT] = new_colors[0]
        self.u[:, LEFT] = new_colors[1]
        self.b[:, RIGHT]  = new_colors[2]
        self.d[:, LEFT] = new_colors[3]

    def rotate(self, face):
        # TODO: should probably avoid doing the copy
        # TODO: inverse moves
        _face = self.faces[face]
        self.faces[face] = np.rot90(_face, axes=(1,0))
        self.tiles[face] = np.rot90(self.tiles[face], axes=(1,0))

        if face is 'u':
            # rotate top stuff
            #self.l[TOP,:], self.b[TOP,:], self.r[TOP,:], self.f[TOP,:] = self.f[TOP, :].copy(), self.l[TOP,:].copy(), self.b[TOP,:].copy(), self.r[TOP,:].copy()
            self.rot_u()
        elif face is 'd':
            # left bot, front bot, right bot, back bot
            #self.l[BOT,:], self.f[BOT,:], self.r[BOT,:], self.b[BOT,:] = self.b[BOT, :].copy(), self.l[BOT,:].copy(), self.f[BOT,:].copy(), self.r[BOT,:].copy()
            self.rot_d()
        elif face is 'l':
            # front left -> down left -> back right -> up left
            #self.f[:,LEFT], self.d[:,LEFT], self.b[:,RIGHT], self.u[:,LEFT] = self.u[:,LEFT].copy(), self.f[:,LEFT].copy(), self.d[:,LEFT].copy(), self.b[:,RIGHT].copy()
            self.rot_l()
        elif face is 'r':
            # front right -> up right -> back left -> down right
            #self.f[:,RIGHT], self.u[:,RIGHT], self.b[:,LEFT], self.d[:,RIGHT] = self.d[:,RIGHT].copy(), self.f[:,RIGHT].copy(), self.u[:,RIGHT].copy(), self.b[:,LEFT].copy()
            self.rot_r()
        elif face is 'f':
            # up bot -> right left -> down top -> left right
            self.r[:,LEFT], self.d[TOP,:], self.l[:,RIGHT], self.u[BOT,:] = self.u[BOT,:].copy(), self.r[:,LEFT].copy(), self.d[TOP,:].copy(), self.l[:,RIGHT].copy()
        elif face is 'b':
            # left left -> down bot -> right right -> up top
            self.l[:,LEFT], self.d[BOT,:], self.r[:,RIGHT], self.u[TOP,:] = self.u[TOP, :].copy(), self.l[:,LEFT].copy(), self.d[BOT,:].copy(), self.r[:,RIGHT].copy()


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
