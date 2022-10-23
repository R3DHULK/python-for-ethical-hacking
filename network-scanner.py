import socket
from requests import get
#Check If Port Is Open
def isOpen(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        try:
                s.connect((ip, int(port)))
                s.shutdown(socket.SHUT_RDWR)
                file=open("rzlt.txt", "a+")
                file.write(ip)
                file.write("\n +++++++++++++++++++++++++++++ Code from R3DHULK +++++++++++++++++++++++++++++\n")
                #return True
                print(ip[0],"Is up")
        except:
                #return False
                print("Is Down")
        finally:
                s.close()
##Range Ip Function ipRange
def ipRange(start_ip, end_ip):
   start = list(map(int, start_ip.split(".")))
   end = list(map(int, end_ip.split(".")))
   temp = start
   ip_range = []

   ip_range.append(start_ip)
   while temp != end:
      start[3] += 1
      for i in (3, 2, 1):
         if temp[i] == 256:
            temp[i] = 0
            temp[i-1] += 1
      ip_range.append(".".join(map(str, temp)))

   return ip_range
   pass

#logo
print ('''
   **********************************************************************
   *  _  _     _                  _     ___                             *
   * | \| |___| |___ __ _____ _ _| |__ / __| __ __ _ _ _  _ _  ___ _ _  *
   * | .` / -_)  _\ V  V / _ \ '_| / / \__ \/ _/ _` | ' \| ' \/ -_) '_| *
   * |_|\_\___|\__|\_/\_/\___/_| |_\_\ |___/\__\__,_|_||_|_||_\___|_|   *
   *                                                                    *
   *    code from R3dHULK                                               *
   *    github page : https://github.com/R3DHULK                        *
   *                                                                    *
   **********************************************************************
''')

# main start 
From = input("Put Start From Range ➡️  " )
To = input("Put End Of Range ➡️  " )
ip_range = ipRange(From, To)
port = input("Put Port To Check  in If It is Up ➡️  ")
print("Stating 😊 😊 😊 :> From",From,"To",To)
Exteral_IP = get('https://api.ipify.org').text #get External Ip
print("HULK says your external ip is 👉 ",Exteral_IP)
ok = input("Press Enter To Start ")
print (" ")
print ("*** Hulk came up with *** ")
print (" ")
for ip in ip_range:
        print("Check For ",ip)
        isOpen(ip,port)
input("Enter To Exit")