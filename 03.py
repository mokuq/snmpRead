from os import path # os needed for folder and file address
from csv import writer, reader # modul for csv
import sys #modul for reading command line arguments
from pysnmp.entity.rfc3413.oneliner import cmdgen # snmp requests
import pysnmp# exception while hostname is bad IPv4/UDP transport address pysnmp.error.PySnmpError
import datetime # date and time in a name of outpu file

print ('This program is collecting data from printers via SNMP.')
print ('Creator: Viktor Ilienko')

# current directory
script_dir = path.dirname(path.abspath(__file__))

# list of oid: sn,  bwTotal, bwA3, colTotal,  colA3, pagesTotal 
# Xerox 
oidsXerox = (".1.3.6.1.2.1.43.5.1.1.17.1", 
		".1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.34", 
		".1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.44",
		".1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.33", 
		".1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.43",
		".1.3.6.1.2.1.43.10.2.1.4.1.1")

# HP
oidsHP = (".1.3.6.1.2.1.43.5.1.1.17.1", 
		".1.3.6.1.4.1.11.2.3.9.4.2.1.4.1.2.6.0",
		".1.3.6.1.4.1.11.2.3.9.4.2.1.1.16.1.1.11.27.0",
		".1.3.6.1.4.1.11.2.3.9.4.2.1.4.1.2.7.0", 
		".1.3.6.1.4.1.11.2.3.9.4.2.1.1.16.3.1.1.27.0",
		".1.3.6.1.2.1.43.10.2.1.4.1.1")

# from pysnmp
cmdGen = cmdgen.CommandGenerator()

# creating a list of data from snmp requests
def dataList(hostname):
	# session = Session(hostname=hostname, community='public', version=2)
	# creating a list of values
	lst = list()

	# checking is it Xerox or HP
	try:
		errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
		    cmdgen.CommunityData('public'),
		    cmdgen.UdpTransportTarget((hostname, 161)),
		    ".1.3.6.1.2.1.25.3.2.1.3.1"
		)
		# if value is absend, than we add None, otherwise adding value
		try:
			model = str(varBinds[0][1]).replace(";","")
		except IndexError:
			model = " "
	except pysnmp.error.PySnmpError:
		model = " "

	lst.append(model)

	if model[0].lower() == "h":
		oids = oidsHP
	else:
		oids = oidsXerox

	# trevelind thru oids
	for key	in oids:
		#getting value of concrete oid
		try:
			errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
			    cmdgen.CommunityData('public'),
			    cmdgen.UdpTransportTarget((hostname, 161)),
			    key
			)
			# if value is absend, than we add None, otherwise adding value
			try:
				value = varBinds[0][1]
				lst.append(str(value))
			except IndexError:
				lst.append(None)
		except pysnmp.error.PySnmpError:
			return None 
	# adding host's IP 
	if len(lst)!=0:
		lst.insert(2, hostname)
	return lst	


# receiving list of IP:
try: 
	f = open(sys.argv[1]) 
except (IndexError, FileNotFoundError):
	try:
		f = open(script_dir + "/" + 'iplist.txt', newline='')
		print ("Opening rawdata.txt and traveling thru IP addresses, please, wait...") 
	except FileNotFoundError:
		print("Enter/Paste IP addresses. Ctrl-Z to save it.")
		contents = []
		while True:
			try:
				line = input()
			except EOFError:
				break
			contents.append(line)
		f = contents
finally:
	f = reader(f)	

clicks = []
clicks.insert(0, ('model sn ip bw bwA3 col  colA3 pagesTotal').split() )


for hostname in f:
	try: 
		print ("Discovering data from", hostname[0])
		# checking typo in IP addresses
		if hostname[0][0].isalpha() or not ("." in hostname[0]):
			print ("Typo in IP address. Please, write IP in standard format: xxx.xxx.xxx.xxx")
			print ("This IP was passed")
			continue
		lst = dataList (hostname[0])
		# if received None than lst is not adding
		clicks.append(lst)
	except IndexError:
		pass

filename = script_dir + "\\" + 'Counters_' + datetime.datetime.now().strftime("%S-%M-%H-%d-%m-%Y")+'.csv'

with open(filename, 'w', newline='') as writeFile:
	writer = writer(writeFile)
	for line in clicks:
		writer.writerow(line)
try:
	f.close()
except (NameError, AttributeError):
	pass

# waiting for hiting enter
try:
	print (f"You can find data from discovered printers in a file {filename}")
	input("Press enter to close the program")
except SyntaxError:
    pass
