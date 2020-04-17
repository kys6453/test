from datetime import datetime
from random import *
import time
import zmq
import json
import zmq.asyncio
import asyncio

async def run(sock, port_num):
    # Debug
    flag = 0
        
    # File Open
    #data_dir = f'/app/data/{port_num}/data{port_num}.txt'
    data_dir = f'../data/{port_num}/data{port_num}.txt'
    #f = open(data_dir, 'r')

    while True:

        f = open(data_dir, 'r')
        start_time = time.time()

        msg = f'port{port_num}\n' + f.read()
        print(f'Sent : {len(msg)}')
        sock.send_string(msg)
        end_time = time.time()
        time_diff = end_time - start_time
        print(f'Loop time : {time_diff}')
        
        await asyncio.sleep(1 - time_diff)
        f.close()
        
async def receiver(max_port, pyzmq_host='127.0.0.1'):
    print('Receiver is ready...')
    print('pyzmq_host : ', pyzmq_host)
    
    # ZeroMQ Socket Open & Bind
    ctx = zmq.asyncio.Context()
    sock = ctx.socket(zmq.PUB)
    sock.bind(f'tcp://{pyzmq_host}:5557')

    time.sleep(1)

    fts = [asyncio.ensure_future(run(sock, wk_id)) for wk_id in range(max_port)]

    for f in asyncio.as_completed(fts):
        await f

if __name__ == '__main__':
    import os
    import sys
    
    print('START!')
    pyzmq_host = os.environ.get('PYZMQ_HOST', '127.0.0.1')
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(receiver(8, pyzmq_host))
    loop.close()
    end_time = time.time()
    print(f'Working time {end_time - start_time} sec.')

