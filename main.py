from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime

# to imitate an event for process with id=pid
def grab_cider(pid, name, counter):
    # increase this process' counter
    counter[pid] += 1
    # print the event information
    print('* {} ordered more cider *'.format(name.upper()))
    return counter

# compare received timestamp and the current timestamp and return max (element-wise)
def update_vector_timestamp(received, counter):
    for pid in range(len(counter)):
        counter[pid] = max(received[pid], counter[pid])
    return counter

# send a message through the pipe from process with id=pid
def send_msg(pipe, pid, name_from, name_to, counter, msg):
    # increase this process' counter because sending a message is an event
    counter[pid] += 1
    # send the message
    pipe.send((msg, counter))
    # print the event information
    print('{} to {}: {}'.format(name_from.upper(), name_to.upper(), msg))
    return counter

# receive a message through the pipe (process with id=pid is a receiver)
def recv_msg(pipe, pid, counter):
    # receive a message itself
    msg, vector_timestamp = pipe.recv()
    # update the counter (get max for each of the two corresponding elements)
    counter = update_vector_timestamp(vector_timestamp, counter)
    return counter

# A's process according to 'processes.jpg'
def process_a(to_b):
    pid = 0
    name = "a"
    counter = [0] * 3
    counter = send_msg(to_b, pid, name, "b", counter, "i dont wanna drink anymore :c")
    counter = send_msg(to_b, pid, name, "b", counter, "dude you hear me?")
    counter = grab_cider(pid, name, counter)
    counter = recv_msg(to_b, pid, counter)
    counter = grab_cider(pid, name, counter)
    counter = grab_cider(pid, name, counter)
    counter = recv_msg(to_b, pid, counter)

# B's process according to 'processes.jpg'
def process_b(to_a, to_c):
    pid = 1
    name = "b"
    counter = [0] * 3
    counter = recv_msg(to_a, pid, counter)
    counter = recv_msg(to_a, pid, counter)
    counter = send_msg(to_a, pid, name, "a", counter, "yeah i hear you. i'm done too")
    counter = recv_msg(to_c, pid, counter)
    counter = grab_cider(pid, name, counter)
    counter = send_msg(to_a, pid, name, "a", counter, "hey, we should stop drinking")
    counter = send_msg(to_c, pid, name, "c", counter, "A got shitfaced, let's go pls")
    counter = send_msg(to_c, pid, name, "c", counter, "duude you should stop, let's go")

# C's process according to 'processes.jpg'
def process_c(to_b):
    pid = 2
    name = "c"
    counter = [0] * 3
    counter = send_msg(to_b, pid, name, "b", counter, "i wanna get one more cider and then we can go")
    counter = recv_msg(to_b, pid, counter)
    counter = grab_cider(pid, "c", counter)
    counter = recv_msg(to_b, pid, counter)

# main function
def main():
    # create a pipe between A and B
    a_b, b_a = Pipe()
    # create a pipe between B and C
    b_c, c_b = Pipe()
    
    # create two processes: A, B, C and initialize the pipes
    a = Process(target=process_a, args=(a_b,))
    b = Process(target=process_b, args=(b_a, b_c))
    c = Process(target=process_c, args=(c_b,))

    # start the processes
    a.start()
    b.start()
    c.start()

    # make sure they are all done
    a.join()
    b.join()
    c.join()
    

main()