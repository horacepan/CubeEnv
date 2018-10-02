from cube import Cube, ACTIONS
import argparse
import time
import random
import os
import pdb

def clear_screen():
    os.system('clear')

def parse_user_cmd(s):
    '''
    s: command string
       Allowed format is: 'x.y.z.{etc}', where x, y, z are in ACTIONS
    Returns: list of allowed moves(u/d/l/r/f/b)
    '''
    moves = s.split('.')
    for m in moves:
        assert (m in ACTIONS or m == 'clear' or m == 'pdb')
    return moves

def interpreter(cube):
    while True:
        clear_screen()
        cube.render()
        user_cmd = str(input('\nMove: '))
        moves = parse_user_cmd(user_cmd)

        if 'clear' in moves:
            cube.reset()
        elif 'pdb' in moves:
            pdb.set_trace()
        else:
            cube.step(moves)

def random_run():
    cube = Cube(2)
    moves = ['u', 'd', 'l', 'r', 'f', 'b']
    for _ in range(100):
        move = random.choice(moves)
        cube.rotate(move)
        cube.render()
        time.sleep(0.1)
        print('-' * 80)

def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=int, default=3)
    return parser.parse_args()

def main():
    config = get_config()
    cube = Cube(config.size)
    interpreter(cube)

if __name__ == '__main__':
    #random_run()
    main()
