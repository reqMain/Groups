import time
import sys
import re,os
import urllib.request,urllib.parse,threading
from datetime import datetime

try:
	from googlesearch import search
except ImportError:
	print("[!] \"google\" Module is unavailable. ")
	print("    Please Install it by using:")
	print("\n    python3 -m pip install google")
	exit()

SAVE = "Result_%s.txt" % datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
availabledom = ["pastebin",
		"throwbin",
		"pastr",
		"pasteio",
		"paste2",
		"paste"]
site_urls = ["https://whatsgrouplink.com/",
	     "https://whatsappgroups.app/job-alerts-whatsapp-group-links/",
	     "https://whatsappgroups.app/whatsapp-group-links/",
	     "https://whatsappgroups.app/pubg-whatsapp-group-links-india/",
	     "https://whatsappgroups.app/funny-jokes-whatsapp-group-links/",
	     "https://allinonetrickz.com/new-whatsapp-groups-invite-links/"]

def linkcheck(url):
	print("\nTrying URL:", url, end='\r')
	try:
		r = urllib.request.urlopen(url)
	except:
		return ('','')
	if(r.getcode() != 404):
		r = r.read().decode("utf-8")
		p = r.find("</h2>")
		name=r[r.rfind("\">", 0, p) + 2:p]
		if name.strip() == '':
			return ('','')
		return (name,url)
	return ('','')
def pad(s):
	if not "invite" in s:
		p = s.find(".com")
		s = s[:p + 4] + "/invite" + s[p + 4:]
	return s
def scrape(txt):
	if type(txt) == type(b''):
		txt = txt.decode("utf-8")
	match = []
	match2 = re.findall(r"(https:\/\/chat\.whatsapp\.com\/(invite\/)?[a-zA-Z0-9]{22})", txt)
	match = [item[0] for item in match2]
	match = list(set(match))
	for lmt in match:
		lmt = pad(lmt)
		nm, url = linkcheck(lmt)
		if nm != '':
			print("[i] Group Name: " + (nm + ' ' * (65-len(nm))))
			print("[i] Group Link: ", url)
			f = open(SAVE, "ab")
			f.write(str.encode(nm + " : " + url + '\n'))
			f.close()


def start(index):
	print("[*] Initializing...")
	if index >= len(availabledom):
		return
	query = "intext:chat.whatsapp.com inurl:" + availabledom[index]
	print("[*] Finding Results from Google ...")
	for url in search(query, tld="com", num=10, stop=None, pause=2):
		txt = urllib.request.urlopen(url).read().decode("utf8")
		scrape(txt)

def scrap_from_link(index):
	print("[*] Initializing...")
	if index >= len(site_urls):
		return
	r = urllib.request.urlopen(site_urls[index]).read().decode()
	scrape(r)

def get_terminal_size(fallback=(80, 24)):
	for i in range(0, 3):
		try:
			columns, rows = os.get_terminal_size(i)
		except OSError:
			continue
		break
	else:
		columns, rows = fallback
	return columns, rows

def main():
	global SAVE
	terminal_size = get_terminal_size()
	
	if terminal_size[0] < 80:
		print("""
   

 __   __   __        __           
/ _` |__) /  \ |  | |__) |    \ / 
\__> |  \ \__/ \__/ |    |___  |  
                                     
   
   
		""")
	else:
		print("""
     
  ________  ____  __  _____  ____  __
 / ___/ _ \/ __ \/ / / / _ \/ /\ \/ /
/ (_ / , _/ /_/ / /_/ / ___/ /__\  / 
\___/_/|_|\____/\____/_/  /____//_/  
                                     
									 
   
	""")

	if len(sys.argv) >= 2:
		if 'u' in sys.argv[1] or '-u' in sys.argv[1]:
			print("[*] Updating, Please Wait...", end='\r')
			try:
				txt = urllib.request.urlopen("https://github.com/Lucia361/grouply/raw/master/grouply.py").read()
				f = open(sys.argv[0], "wb")
				f.write(txt)
				f.close()
				print("[$] Update Successful.")
				print("[i] Run " + sys.argv[0] + " Again..")
			except:
				print("[!] Update Failed !!!     ")
			exit()
	
	threads = []
	print("""
   1> Extract From Google
   2> Extract From Group Sharing Sites [BEST]
   3> Check From File
   4> Update Grouply
	""")
	
	try:
		inp = int(input("[#] Enter Selection: "))
	except:
		print("\t[!] Invalid Selection..")
		exit()
	
	if inp != 4:
		newSave = str(input("[#] Enter Saving File (Default is Result.txt): "))
		SAVE = "Result.txt" if newSave == '' else newSave
	
		f = open(SAVE, 'w')
		f.write("WhatsApp Group Links Extracted by Grouply \nGet it at https://github.com/Lucia361/grouply\r\n")
		f.close()
	
	if inp == 1:	
		for i in range(0, int(input("[#] Enter Threads Number(1-" + str(len(availabledom)) + "):- "))):
			thread = threading.Thread(target=start, args=(i,))
			thread.start()
			threads.append(thread)

		for i in threads:
			i.join()
	elif inp == 2:
		for i in range(0, int(input("[#] Enter Threads Number(1-" + str(len(site_urls)) + "):- "))):
			thread = threading.Thread(target=scrap_from_link, args=(i,))
			thread.start()
			threads.append(thread)

		for i in threads:
			i.join()
	elif inp == 3:
		path = input("[#] Enter Whatsapp Links File Path: ").strip()
		if not os.path.isfile(path):
			print("\t[!] No such file found...")
			exit()
		thn = int(input("[#] Enter Thread Numbers: "))
		op = open(path, "rb").read().decode("utf-8")
		op = op.count('\n') // thn
		with open(path, "rb") as strm:
			for i in range(thn - 1):
				head = [next(strm) for x in range(op)]
				thread = threading.Thread(target=scrape, args=(b'\n'.join(head),))
				thread.start()
				threads.append(thread)
			thread = threading.Thread(target=scrape, args=(strm.read(),))
			thread.start()
			threads.append(thread)
		for i in threads:
			i.join()
	elif inp == 4:
		print("[*] Updating, Please Wait...", end='\r')
		try: 
			txt = urllib.request.urlopen("https://github.com/Lucia361/grouply/raw/master/grouply.py").read()
			f = open(sys.argv[0], "wb")
			f.write(txt)
			f.close()
			print("[$] Grouply updated successfully")
			print("[i] Run " + sys.argv[0] + " Again...")
		except:
			print("[!] Update Failed !!!     ")
		exit()
	else:
		print("[!] Invalid Selection...")

if __name__ == "__main__":
	main()
