import multiprocessing
import numpy as np
import processor
import time

def func(val, timestamp):
    start_time = time.time()
    
    y = np.fft.fft(val)
    y = 2 * np.abs(y)
    n = len(val)
    timestep = 0.0001
    freq = np.fft.fftfreq(n, d=timestep)
    freq = np.fft.fftshift(freq)
    msg = f'port0, fourier : {y}, freq : {freq}'

    end_time = time.time()
    
    print(f'FFT[0] Time : {end_time - start_time} sec.')


procs = []
for i in range(8):
    with open('../data/0/data0.txt', 'r') as f:
        msg = f'port0' + f.read()
        val, timestamp = processor.parse(msg)
        print(f'{len(val)} // {len(timestamp)}')
        p = multiprocessing.Process(target=func, args=(np.split(np.array(val), 3), np.split(np.array(timestamp), 3)))
        p.start()
        procs.append(p)



print('started', len(procs), 'processes')

start_time = time.time()

for p in procs:
    p.join()
    print('process done')

end_time = time.time()

print(f'Working time : {end_time - start_time}')

print('all done')
