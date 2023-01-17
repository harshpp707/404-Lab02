#!/usr/bin/env python3
import socket
import sys
from multiprocessing import Process

# define global address and buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024


def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()
    print(f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():
    
    host = 'www.google.com'
    port = 80

    #create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Starting proxy server")
        # allow reused addresses, bind, and set to listening mode
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while True:
            #connect proxy_start 
            conn, addr = proxy_start.accept() 
            print("Connected by", addr) 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google") 
                remote_ip = get_remote_ip(host) 
                #connect proxy end 
                proxy_end.connect( (remote_ip , port) ) 

                p = Process(target=send_data, args=(conn, proxy_end))
                p.daemon = True
                p.start()
                print("Started process ", p)

            conn.close()

def send_data(conn, proxy_end):
    #send data 
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending recieved data {send_full_data} to google") 
    proxy_end.sendall(send_full_data) 
    #shut down  
    proxy_end.shutdown(socket.SHUT_WR) 

    data = proxy_end.recv(BUFFER_SIZE)
    print(f"Sending received data {data} to client")
    #send data back
    conn.send(data)

if __name__ == "__main__":
    main()
