import socket
import time
import threading

class Washer1:
  water = 0
  washedSolution = 0
  unwashed = 0
  emulsion = 0


def OpenSocket():
  host = 'localhost'
  port = 50008
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
    Washer1.unwashed += 9.6
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
    if time_count%1 == 0 and Washer1.unwashed == 9.6:
      Washer1.unwashed -= 9.6
      Washer1.washedSolution += 9.36
      Washer1.emulsion += 0.24
      message = "input-1"
      client.connect(("localhost", 50009))
      client.sendall(message.encode())
      response = client.recv(1024)
      if b'emulsion-received' in response:
        Washer1.emulsion -= 0.24
      elif b'cannot-receive' in response:
        print("Emulsion tank can not receive")
        pass
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if time_count%1 == 0 and Washer1.washedSolution >= 1.5:
      message = "input-solution"
      client.connect(("localhost", 50010))
      client.sendall(message.encode())
      response = client.recv(1024)
      if b'solution-received' in response:
        Washer1.washedSolution -= 1.5
      elif b'cannot-receive' in response:
        print("Washer2 can not receive")
        pass
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
    time.sleep(1)
    time_count += 1



main()