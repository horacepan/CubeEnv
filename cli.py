from cube import Cube, ACTIONS
import random
import os

def clear_screen():
    os.system('clear')

def parse_user_cmd(s):
    '''
    Allowed format is: 'x.y.z.{etc}', where x, y, z are in ACTIONS
    '''
    moves = s.split('.')
    for m in moves:
        assert (m in ACTIONS or m == 'clear')

    return moves

def interpreter(cube):
    while True:
        clear_screen()
        cube.render()
        user_cmd = str(input('\nMove: '))
        moves = parse_user_cmd(user_cmd)

        if 'clear' in moves:
            cube.reset()
        else:
            cube.step(moves)
        cube.render()

def random_run():
    cube = Cube(3)
    moves = ['u', 'd', 'l', 'r', 'f', 'b']
    for _ in range(100):
        move = random.choice(moves)
        cube.rotate(move)
        cube.render()
        time.sleep(0.1)
        print('-' * 80)

def main():
    cube = Cube(3)
    interpreter(cube)

if __name__ == '__main__':
    main() 
