import socket
import time
import threading

class Washer3:
  water = 0
  washedSolution = 0
  unwashedSolution = 0
  emulsion = 0


def OpenSocket():
  host = 'localhost'
  port = 50011
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
  if 'input-solution' in message:
    Washer3.unwashedSolution += 1.4625
    res = "solution-received"
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
    
    if time_count%1 == 0 and Washer3.unwashedSolution == 1.4625:
      Washer3.unwashedSolution -= 1.4625
      Washer3.washedSolution += 1.4259375
      Washer3.emulsion += 0.0365625
      message = "input-3"
      client.connect(("localhost", 50009))
      client.sendall(message.encode())
      response = client.recv(1024)
      if b'emulsion-received' in response:
        Washer3.emulsion -= 0.0365625
      elif b'cannot-receive' in response:
        print("Emulsion tank can not receive")
        pass
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if time_count%1 == 0 and Washer3.washedSolution >= 1.4259375:
      print(Washer3.washedSolution)
      message = "input-solution"
      client.connect(("localhost", 50012))
      client.sendall(message.encode())
      response = client.recv(1024)
      if b'solution-received' in response:
        Washer3.washedSolution -= 1.4259375
        print("mandei pro secador ", Washer3.washedSolution)
      elif b'cannot-receive' in response:
        print("secador can not receive")
        pass
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
    time.sleep(1)
    time_count += 1



main()