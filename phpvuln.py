import requests

print ('''\033[93m
    **********************************************
    *      Simple PHP Vulnerability Scanner      *
    *  github page : https://github.com/r3dhulk  *
    **********************************************
       ''')

def scan_vulnerabilities(url):
    response = requests.get(url)
    if response.status_code == 200:
        if 'X-Powered-By: PHP' in response.headers:
            print('\033[92m [INFO] Target is using PHP')
            # Add vulnerability checks here
        else:
            print('\033[92m [ERROR] Target is not using PHP')
    else:
        print('\033[92m [ERROR] Could not connect to target')

scan_vulnerabilities(input("\033[92m [+] Enter Url (i.e. https://example.com) : "))
