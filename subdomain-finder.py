import requests

domain = input("[+] Input url to get subdomains : ")
print ("[+] Waiting progress ... \n")
print('''
[*] You Engaged Hulk For Finding Subdomains :
       
[*] Trying his best ...
      
      ''')

def main(domain):
	url = "https://sonar.omnisint.io/subdomains/{}".format(domain)
	data = requests.get(url).json()
	print ("[+] Hulk came up with : \n")
	for i in data:
		print(i)
		open('Result.txt','a').write(str(i) + '\n')

if __name__ == '__main__':
	main(domain)
print("  ")
print("\033[1m" + "<== Process Finished ==>" + "\033[0m")
input("Press Enter To Exit")