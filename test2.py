import socket
import time

def main():
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect(("localhost", 50002))
  time_count = 0
  message = "Heello FEI!"

  while True:

    if time_count%5 == 0:
      print("mandei2")
      client.sendall(message.encode())
      
      time.sleep(5)
      time_count += 5


main()