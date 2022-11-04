import pikepdf
import sys
import os
# read the pdf file
os.system("clear")
print(''' 
  ___ ___  ___   _____  _____ ___   _____ ___   ___  _    
 | _ \   \| __| | __\ \/ /_ _| __| |_   _/ _ \ / _ \| |  v. 1. O 
 |  _/ |) | _|  | _| >  < | || _|    | || (_) | (_) | |__ 
 |_| |___/|_|   |___/_/\_\___|_|     |_| \___/ \___/|____|
          c 0 d e   f       0         
                        r        m    R3DHULK     ''')  
print("")                                                     
pdf = pikepdf.Pdf.open(input("Enter PDF Name : "))
print("")
docinfo = pdf.docinfo
for key, value in docinfo.items():
    print( key, ":", value)
    print("")
input("Enter To Close Window")
os.system("clear")
