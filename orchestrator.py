import socket
import threading
import time
import random

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
  message = conn.recv(1024).decode()
  if message == "get-oil":
    liters = random.randint(1, 2)
    res = "input-oil {}".format(liters)
    conn.sendall(res.encode())
    conn.close()
  elif message == "get-naoh":
    res = "input-naoh"
    conn.sendall(res.encode())
    conn.close()
  elif message == "get-etoh":
    res = "input-etoh"
    conn.sendall(res.encode())
    conn.close()
  elif "status" in message:
    print(message)
    conn.close()


def main():
  host = 'localhost'
  port = 50002

  try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.settimeout(0.2)

  except OSError as message:
    print('socket creation error: ' + str(message))

  bindSocket(server, host, port)

  while True:
    try:
      conn, addr = server.accept()
      threading.Thread(target=management(conn, addr), args=(conn, addr))
    except socket.timeout:
      pass
    

main()