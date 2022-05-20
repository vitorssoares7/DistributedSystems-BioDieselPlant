import socket
import _thread
import threading
import time


def bindSocket(server, host, port):
  try:
    server.bind((host, port))
    server.listen(100)
    print('server listening on port: ' + str(port))

  #auto reconnection every 3 seconds in case of errors
  except OSError as message:
    print('socket binding error: ' + str(message))
    print('retrying in 3 seconds...\n')
    time.sleep(3)
    bindSocket(server, host, port)

def management(conn, addr):
  print(f"[NEW CONNECTION] {addr} connected.")
  print("Ta saindo da jaula o monstro")
  while True:
    message = conn.recv(1024).decode() 
    print(message)



def main():
  host = 'localhost'
  port = 50002

  try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  except OSError as message:
    print('socket creation error: ' + str(message))

  bindSocket(server, host, port)

  while True:
        conn, addr = server.accept()
        thread =  threading.Thread(target=management(conn, addr), args=(conn, addr))


main()