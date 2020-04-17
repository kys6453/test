import datetime
import json
import time
import zmq
import sys
import numpy as np
import multiprocessing

np.set_printoptions(threshold=sys.maxsize)

def parse(msg):
   msg_list = msg.splitlines()
   topicfilter = msg_list.pop(0)
   print(f'topicfilter pop {topicfilter}')
   
   val = []
   time = []

   for i in msg_list:
       tmp = i[1:-1].replace(' ', '')
       val.append(tmp.split(sep=',')[0].split(sep='=')[1])
       time.append(tmp.split(sep=',')[1].split(sep='=')[1])

   return val, time

def processor(port, pyzmq_host='127.0.0.1'):
    
    ctx = zmq.Context()

    sock_recv = ctx.socket(zmq.SUB) 
    sock_recv.connect(f'tcp://{pyzmq_host}:5557')
    topicfilter = f'port{port}'
    sock_recv.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
    
    # Create Socket(PUB)
    sock_send = ctx.socket(zmq.PUB)
    #sock_send.connect(f'tcp://{pyzmq_host}:5558')
    
    while True:

        msg = sock_recv.recv_string()

        print(f'msg_len : {len(msg)}') 
        #if len(msg) <= 100:
            #print(f'msg : {msg}')

        #if not msg:
            #continue

        val, timestamp = parse(msg)

        start_time = time.time()
    
        y = np.fft.fft(val)
        y = 2 * np.abs(y)
        n = len(val)
        timestep = 0.0001
        freq = np.fft.fftfreq(n, d=timestep)
        freq = np.fft.fftshift(freq)
        msg = f'port{port}, fourier : {y}, freq : {freq}'

        end_time = time.time()
        print(f'FFT[{port}] Time : {end_time - start_time} sec.')

        #sock_send.send_string(msg)

if __name__ == '__main__':
    import os

    pyzmq_host = os.environ.get('PYZMQ_HOST', '127.0.0.1')
    port = os.environ.get('PORT', 0)
    
    start_time = time.time()
    #processor(port, pyzmq_host)
    p = multiprocessing.Pool()
    p.map_async(processor, (port, pyzmq_host))
    p.close()
    p.join()
    end_time = time.time()
    print(f'Working time = {end_time - start_time} sec.')
