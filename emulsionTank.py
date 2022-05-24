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
  if 'input-1' in message:
    print("recevi do 1")
    Emulsion.emulsion+=0.24
    res = "emulsion-received"
    conn.sendall(res.encode())
    conn.close()
  elif 'input-2' in message:
    print("recevi do 2")
    Emulsion.emulsion+=0.0375
    res = "emulsion-received"
    conn.sendall(res.encode())
    conn.close()
  elif 'input-3' in message:
    print("recevi do 3")
    Emulsion.emulsion+=0.0365625
    res = "emulsion-received"
    conn.sendall(res.encode())
    conn.close()


def main():
  server = OpenSocket()
  server.settimeout(0.2)
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  time_count = 0
  

  while True:
    try:
      conn, addr = server.accept()
      threading.Thread(target=management(conn, addr), args=(conn, addr))
    except socket.timeout:
      pass

    if time_count%10 == 0:
      print(Emulsion.emulsion)
    
      
    time.sleep(1)
    time_count += 1



main()