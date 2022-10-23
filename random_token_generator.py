import secrets
print('''
    ********************************************************  
    *  [?] Simple Random String Generator Tool [?]         *
    *                                                      *
    *  You Can Save Them In My Advanced Notepad Software   *
    *  Check Out : https://github.com/R3DHULK/hulk-office  *
    *                                                      *
    ********************************************************
    ''')
val = int (input("How many no. of string you want to generate : "))
print("Your token is :", secrets.token_hex(val))
input("Enter To Close")