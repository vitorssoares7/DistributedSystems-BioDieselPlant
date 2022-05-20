import socket
import time

def main():
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  time_count = 0
  oilAmount = 0

  while True:

    # Condition to send a request for oil every 10 seconds 
    # receiving 1 or 2 liters as response randomly
    if time_count%10 == 0:
      message = "get-oil"
      client.connect(("localhost", 50002))
      client.sendall(message.encode())
      response = client.recv(1024)
      print(response)
      if b'input-oil' in response and b'1' in response:
        oilAmount+=1
        print("total de oleo: ", oilAmount)
      else:
        oilAmount+=2
        print("total de oleo: ", oilAmount)
      client.close()
      client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Sends oil to the reactor every second if oilAmount<0.75 and checks if the reactor
    #can receive it
    if time_count%1 == 0:
      if oilAmount > 0.75:
        flowRate = 0.75
        message = "input-oil {}".format(flowRate)
        client.connect(("localhost", 50003))
        client.sendall(message.encode())
        response = client.recv(1024)
        if b'oil-received' in response:
          print("saida realizada com sucesso")
          oilAmount-=0.75
        elif b'cannot-receive' in response:
          print("reactor could not receive")
          pass
        client.close()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
      
    time.sleep(1)
    time_count += 1


main()