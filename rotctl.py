import socket
import sys
from datetime import datetime
import os
import subprocess

def main():
    
    # The shell script to send IR commands
    dirname = os.path.dirname(os.path.abspath(__file__))
    sendir = os.path.join(dirname, 'sendir.sh')
    
    # The number of degrees of rotation per second
    rot_speed = 4.8
    
    # Assumes rotator has 12 memory buttons labeled A-L
    buttons = ["L","A","B","C","D","E","F","G","H","I","J","U","L"]
    
    # Assumes rotator button A represents 30°, B 60° etc; 
    # Each setting is made up of (min degrees, max degrees, direction)
    # L Has two list elements as it resets the degrees back to 0
    rot_pos = [
          (  0,     15,  0),
          ( 15.001, 45, 30),
          ( 45.001, 75, 60),
          ( 75.001,105, 90),
          (105.001,135,120),
          (135.001,165,150),
          (165.001,195,180),
          (195.001,225,210),
          (225.001,255,240),
          (255.001,285,270),
          (285.001,315,300),
          (315.001,345,330),
          (345.001,361,  0)
          ]
    
    # Initialise rotator
    start_time = datetime.now()
    target_pos = current_pos = start_pos = 0.00
    time = datetime.now().strftime("%H:%M:%S")
    print("[{}] >>>>>> Press button Initial".format(time))
    subprocess.run(["/bin/sh", sendir, "L"]) 
    
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the address given on the command line
    server_address = ("0.0.0.0", 65432)
    sock.bind(server_address)
    sock.listen(1)
    
    while True:
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            while True:
                data = connection.recv(16)
                
                if data:
                    time = datetime.now().strftime("%H:%M:%S")
    
                    # If we have asked the rotator to move calculate the current position
                    if current_pos != target_pos:
                        # How far has the rotator moved since we started
                        t_diff = datetime.now() - start_time
                        movement = t_diff.seconds * rot_speed
                        diff = target_pos - start_pos
                        
                        # Update the current position
                        if diff >= 0:
                            current_pos = round(start_pos + movement, 2)
                        else:
                            current_pos = round(start_pos - movement, 2)
                        
                        # Has the rotator has arrived at the target position
                        if abs(target_pos - current_pos) < rot_speed:
                            current_pos = target_pos
                            
                    # Read data from antenna control
                    cmd = data.decode("utf-8").strip().split(" ")
                    
                    # Received updated coordinates
                    if cmd[0] == "P":
                      print("[{}] Setting Az: {} El: {}".format(time,cmd[1],cmd[2]) )
    
                      for i, p in enumerate(rot_pos):
                          if p[0] <= float(cmd[1]) <= p[1]:
                              print("[{}] >>>>>> Press button {}".format(time,buttons[i]))
                              subprocess.run(["/bin/sh", sendir, buttons[i]]) 
                              
                              # Start movement countdown
                              if target_pos != float(p[2]):
                                  start_time = datetime.now() 
                                  start_pos = current_pos
                                  target_pos = float(p[2])
                                  
                      # Send OK
                      connection.sendall(b"RPRT 0\n")
                      
                    # Received get_pos request
                    if cmd[0] == "p":
                      resp = "{}\n15.000000".format(current_pos)
                      print("[{}] Sending position: {}".format(time,current_pos))
                      
                      # Send current position
                      connection.sendall(resp.encode('utf-8'))
                      
                    # Received stop request
                    if cmd[0] == "S":
                      # Send OK
                      connection.sendall(b"RPRT 0\n")

                    if cmd[0] == "_":
                      connection.sendall(b"rotctrl by steve\n")
 
                else:
                    break
        finally:
            connection.close()

main()

