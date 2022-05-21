import socket
import time
import threading

class GlicerinTank:
  glicerin = 0

def OpenSocket():
  host = 'localhost'
  port = 50005
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
  if 'input-glicerin' in message:
    GlicerinTank.glicerin += 0.1
    res = "glicerin-received"
    conn.sendall(res.encode())
    conn.close()


def main():
  server = OpenSocket()
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  time_count = 0
  

  while True:
    conn, addr = server.accept()
    threading.Thread(target=management(conn, addr), args=(conn, addr))
    
    if time_count%1 == 0:
      print("Total de glicerina: ", GlicerinTank.glicerin, "L")
      
      
    time.sleep(1)
    time_count += 1



main()