import socket
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


logo = '''
         ____       _     _     ___  
        (  __)     ( )  ((())) (   ) 
        | | _  ___ | _)  | |   | O  |
        ( )_))( o_)( )   ( )   ( __/ 
        /____\ \(  /_\   /_\   /_\  
        
         code from R3DHULK

 ******************************************
 *                                        *
 *   coded simple python script           *
 *             to know about url's ip     *
 *           and validity                 *
 *                                        *
 ******************************************
'''

print (logo)


hostname = socket.gethostname()
myip = socket.gethostbyname(hostname)

print ( " You are working on " + hostname)
print (" Your IP is " + myip)

url = URLValidator()


try:

    url = input ("Enter Url to get it's IP : ")

    print("It is a valid URL")
    print("The IP for this " + url + " is ", socket.gethostbyname(url))

except ValidationError as exception:

    print("It is not a valid URL")
input("Enter To Exit")