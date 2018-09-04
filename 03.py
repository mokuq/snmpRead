'''
Description	OID
sn	.1.3.6.1.4.1.253.8.53.3.2.1.3.1
bwTotal	.1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.34
colTotal	.1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.33
bwA3	.1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.44
colA3	.1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.43

oids = {'sn': ".1.3.6.1.4.1.253.8.53.3.2.1.3.1",
		'bwTotal': ".1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.34", 
		'colTotal': ".1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.33", 
		'bwA3': ".1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.44",
		'colA3': ".1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.43"
		}
'''

from os import path # os needed for folder and file address
from csv import writer, reader # modul for csv
import sys #modul for reading command line arguments
from pysnmp.entity.rfc3413.oneliner import cmdgen # snmp requests

# current directory
script_dir = path.dirname(path.abspath(__file__))

# list of oid: sn, bwTotal, colTotal, bwA3, colA3 
oids = (".1.3.6.1.4.1.253.8.53.3.2.1.3.1", 
		".1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.34", 
		".1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.33", 
		".1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.44",
		".1.3.6.1.4.1.253.8.53.13.2.1.6.1.20.43")

# from pysnmp
cmdGen = cmdgen.CommandGenerator()

# creating a list of data from snmp requests
def dataList(hostname):
	# session = Session(hostname=hostname, community='public', version=2)
	# creating a list of values
	lst = list()
	# trevelind thrue oids
	for key	in oids:
		#getting value of concrete oid
		errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
		    cmdgen.CommunityData('public'),
		    cmdgen.UdpTransportTarget((hostname, 161)),
		    key
		)
		try:
			value = varBinds[0][1]
			# if value is absend, than we add None
			lst.append(str(value))
		except IndexError:
				lst.append(None)	

	lst.insert(1, hostname)
	return lst	

# receiving list of IP:
try: 
	f = open(sys.argv[1]) 
except (IndexError, FileNotFoundError):
	try:
		f = open(script_dir + "/" + 'rawdata.txt', newline='') 
	except FileNotFoundError:
		print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
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
clicks.insert(0, ('sn ip bw bwA3 col  colA3').split() )


for hostname in f:
	if 	hostname:
		lst = dataList (hostname[0])
		clicks.append(lst)


filename = script_dir + "/" + 'serialized_data.csv'

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
    input("Press enter to continue")
except SyntaxError:
    pass