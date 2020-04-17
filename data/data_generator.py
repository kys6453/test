import sys
import numpy as np

def generate(route):
    f = open(route, 'w')
    n = 10000
    for t in range(1, n+1):
        sin_t = np.sin(t)
        sin_2t = np.sin(2*t)
        sin_3t = np.sin(3*t)
        time = t/n

        msg = f'{{value = {sin_t + sin_2t + sin_3t}, time = {time}}}\n'
        f.write(msg)

if __name__ == '__main__':
    generate(sys.argv[1])
