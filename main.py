from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime

def imitate_event(pid, name, counter):
    counter[pid] += 1
    print('event in {} occured'.format(name.upper()))
    return counter

def update_vector_timestamp(received, counter):
    for pid in range(len(counter)):
        counter[pid] = max(received[pid], counter[pid])
    return counter

def send_msg(pipe, pid, name_from, name_to, counter, msg):
    counter[pid] += 1
    pipe.send((msg, counter))
    print('{} said to {}: {}'.format(name_from.upper(), name_to.upper(), msg))
    return counter

def recv_msg(pipe, pid, counter):
    msg, vector_timestamp = pipe.recv()
    counter = update_vector_timestamp(vector_timestamp, counter)
    return counter

def process_a(to_b):
    pid = 0
    name = "a"
    counter = [0] * 3
    counter = imitate_event(pid, name, counter)
    counter = send_msg(to_b, pid, name, "b", counter, "i'm tired")
    counter = imitate_event(pid, name, counter)
    counter = recv_msg(to_b, pid, counter)
    counter = imitate_event(pid, name, counter)

def process_b(to_a, to_c):
    pid = 1
    name = "b"
    counter = [0] * 3
    counter = recv_msg(to_a, pid, counter)
    counter = send_msg(to_a, pid, name, "a", counter, "i'm tired too")
    counter = send_msg(to_c, pid, name, "c", counter, "hey, A and I are tired")
    counter = recv_msg(to_c, pid, counter)


def process_c(to_b):
    pid = 2
    name = "c"
    counter = [0] * 3
    counter = recv_msg(to_b, pid, counter)
    counter = send_msg(to_b, pid, name, "b", counter, "okay let's leave the party")

def main():
    a_b, b_a = Pipe()
    b_c, c_b = Pipe()
    
    a = Process(target=process_a, args=(a_b,))
    b = Process(target=process_b, args=(b_a, b_c))
    c = Process(target=process_c, args=(c_b,))

    a.start()
    b.start()
    c.start()

    a.join()
    b.join()
    c.join()
    

main()