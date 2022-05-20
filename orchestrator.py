import socket
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
  message = conn.recv(1024).decode()
  if message == "get-oil":
    res = "toma oleo"
    print("ta pedindo oleo")
    conn.sendall(res.encode())
    conn.close()


def main():
  host = 'localhost'
  port = 50002

  try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  except OSError as message:
    print('socket creation error: ' + str(message))

  bindSocket(server, host, port)

  while True:
    print("esperando")
    conn, addr = server.accept()
    threading.Thread(target=management(conn, addr), args=(conn, addr))
    

main()