import random
import string

print('''
    ********************************************************  
    *  [?] Simple Random Password Generator Tool [?]       *
    *                                                      *
    *  You Can Save Them In My Advanced Notepad Software   *
    *  Check Out : https://github.com/R3DHULK/hulk-office  *
    *                                                      *
    ********************************************************
    ''')
def get_string(letters_count, digits_count):
    letters = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
    digits = ''.join((random.choice(string.digits) for i in range(digits_count)))

    # Convert resultant string to list and shuffle it to mix letters and digits
    sample_list = list(letters + digits)
    random.shuffle(sample_list)
    # convert list to string
    final_string = ''.join(sample_list)
    print('Random string with', letters_count, 'letters', 'and', digits_count, 'digits', 'is:', final_string)
print("Enter how many Letters and Numbers you wish to combine below 👇")
get_string(int(input("How many letters? : ")), int(input("How to many number? : ")))
input("Enter To Close")