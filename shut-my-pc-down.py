import os
import subprocess
print("1. Shutdown Computer Immediately")
print("2. Shutdown Computer after Given Time")
print("3. Restart Computer Immediately")
print("4. Restart Computer after Given Time")
print("5. Lock My Computer Screen")
print("6. Exit")
print(end="Enter Your Choice: ")
choice = int(input())

if choice==1:
    os.system("shutdown /s /t 0")
elif choice==2:
    print(end="Enter Number of Seconds: ")
    sec = int(input())
    strOne = "shutdown /s /t "
    strTwo = str(sec)
    str = strOne+strTwo
    os.system(str)
elif choice==3:
    os.system("shutdown /r /t 0")
elif choice==4:
    print(end="Enter Number of Seconds: ")
    sec = int(input())
    strOne = "shutdown /r /t "
    strTwo = str(sec)
    str = strOne+strTwo
    os.system(str)
elif choice == 5:
    subprocess.call('rundll32.exe user32.dll, LockWorkStation')
elif choice==6:
    exit()
else:
    print("Wrong Choice!")