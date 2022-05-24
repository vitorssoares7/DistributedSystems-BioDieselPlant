import socket
import time
import threading

class Washer2:
  water = 0
  washedSolution = 0
  unwashed = 0
  emulsion = 0


def OpenSocket():
  host = 'localhost'
  port = 50010
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
    Washer2.unwashed += 1.5
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

    if time_count%1 == 0 and Washer2.unwashed == 1.5:
      Washer2.unwashed -= 1.5
      Washer2.washedSolution += 1.4625
      Washer2.emulsion += 0.0375
      message = "input-2"
      client.connect(("localhost", 50009))
      client.sendall(message.encode())
      response = client.recv(1024)
      if b'emulsion-received' in response:
        Washer2.emulsion -= 0.0375
      elif b'cannot-receive' in response:
        print("Emulsion tank can not receive")
        pass
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(Washer2.washedSolution)

    if time_count%1 == 0 and Washer2.washedSolution == 1.4625:
      print("vou mandar pro 3")
      message = "input-solution"
      client.connect(("localhost", 50011))
      client.sendall(message.encode())
      response = client.recv(1024)
      if b'solution-received' in response:
        Washer2.washedSolution -= 1.4625
      elif b'cannot-receive' in response:
        print("Washer2 can not receive")
        pass
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
    time.sleep(1)
    time_count += 1



main()