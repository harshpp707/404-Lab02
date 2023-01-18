#!/usr/bin/env python3
import socket
from multiprocessing import Process

# define global address and buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
    
    #create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # allow reused addresses
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)

        while True:
            #connect proxy_start 
            conn, addr = s.accept() 
            p = Process(target=handle_AnotherProcess, args=(addr, conn))
            p.daemon = True
            p.start()
            print("Started process ", p)
        s.close()
                
def handle_AnotherProcess(addr, conn):
    print("Connect by", addr)
    #recieve data, wait, then send it back
    full_data = conn.recv(BUFFER_SIZE)
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

if __name__ == "__main__":
    main()
