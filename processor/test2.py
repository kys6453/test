import multiprocessing
import numpy as np
import processor
import time

def fft(val, timestamp):
    y = np.fft.fft(val)
    y = 2 * np.abs(y)
    n = len(val)
    timestep = 0.0001
    freq = np.fft.fftfreq(n, d=timestep)
    freq = np.fft.fftshift(freq)
    msg = f'port0, fourier : {y}, freq : {freq}'


if __name__ == '__main__':
    p = multiprocessing.Pool(4)
    f = open('../data/0/data0.txt', 'r')
    msg = f'port0' + f.read()
    parse_start = time.time()
    val, timestamp = processor.parse(msg)
    parse_end = time.time()
    print(f'Parsing time : {parse_end - parse_start} sec.')
    fft_start = time.time()
    p.starmap(fft, (val, timestamp))
    fft_end = time.time()
    print(f'FFT time : {fft_end - fft_start} sec.')


