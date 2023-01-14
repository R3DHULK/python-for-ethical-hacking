from urllib.request import urlopen
from sys import argv, exit

__author__ = 'AppSec Jay'

def check(url):
    ''' Verify given URL is vulnerable or not '''

    try:
        if "http" not in url: url = "https://" + url

        data = urlopen(url)
        headers = data.info()

        if not ("X-Frame-Options" or "frame-ancestors") in headers: return True

    except: return False


def create_poc(url):
    ''' Create HTML page of given vulnerable URL '''

    code = """
<html>
   <head><title>Clickjack Test Page</title></head>
   <body>
     <p>Website is Vulnerable to Clickjacking!</p>
     <iframe src="https://{}" width="400" height="600"></iframe>
   </body>
</html>
    """.format(url)

    with open(url + ".html", "w") as f:
        f.write(code)
        f.close()


def main():
    ''' Everything comes together '''

    try: sites = open(argv[1], 'r').readlines()
    except: print("[*] Usage: python3 clickjacking_scanner.py <file_name>"); exit(0)

    for site in sites[0:]:
        print("\n[*] Checking " + site)
        status = check(site)

        if status:
            print(" [+] Website is Vulnerable!")
            create_poc(site.split('\n')[0])
            print(" [*] Created a POC and saved to <Domain_Name>.html")

        elif not status: print(" [-] Website is not vulnerable!")
        else: print('Every single thing is crashed, Python got mad, dude wtf you just did?')

if __name__ == '__main__': main()
