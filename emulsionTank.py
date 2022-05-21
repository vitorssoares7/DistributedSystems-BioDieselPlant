import socket
import time
import threading

class Emulsion:
  emulsion = 0

def OpenSocket():
  host = 'localhost'
  port = 50009
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  bindSocket(client, host, port)
  return client

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
  if 'input-emulsion' in message:
    Emulsion.emulsion+=0.24
    res = "oil-received"
    conn.sendall(res.encode())
    conn.close()
  elif 'input-emulsion2' in message:
    Emulsion.emulsion+=0.0375
    res = "oil-received"
    conn.sendall(res.encode())
    conn.close()
  elif 'input-emulsion3' in message:
    Emulsion.emulsion+=0.0365625
    res = "oil-received"
    conn.sendall(res.encode())
    conn.close()


def main():
  server = OpenSocket()
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  time_count = 0
  

  while True:
    conn, addr = server.accept()
    threading.Thread(target=management(conn, addr), args=(conn, addr))
    print(Emulsion.emulsion)
    if time_count%10 == 0:
      print(Emulsion.emulsion)
    
      
    time.sleep(1)
    time_count += 1



main()