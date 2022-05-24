import socket
import time
import threading

class DieselDryer:
  solution = 0
  isResting = False


def OpenSocket():
  host = 'localhost'
  port = 50012
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
    DieselDryer.solution += 1.4259375
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

    if time_count%1 == 0 and DieselDryer.solution >= 1:
      DieselDryer.isResting = True
      time.sleep(5)

      message = "input-bio"
      client.connect(("localhost", 50013))
      client.sendall(message.encode())
      response = client.recv(1024)
      if b'bio-received' in response:
        DieselDryer.solution -= 1
      elif b'cannot-receive' in response:
        print("Bio diesel tank can not receive")
        pass

      DieselDryer.isResting = False
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      
    time.sleep(1)
    time_count += 1



main()