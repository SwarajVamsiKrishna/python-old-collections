import wmi
import json
import re
from SendSMTPMail import SendSMTPMail


def GetLocalDrives():
	driveList = []
	for disk in server.Win32_LogicalDisk():
		if disk.DriveType == 3:
			driveList.append(str(disk.Name))
	return driveList
			
def GetTotalDiskSpace(drive):
	drive = drive
	try:
		for disk in server.Win32_LogicalDisk(Name=drive):
			total = int(disk.Size) /2**30
			total = round(total,2)
		return total
	except UnboundLocalError:
		return 'Drive Not Found'

def GetFreeDiskSpace(drive):
	drive = drive
	try:
		for disk in server.Win32_LogicalDisk(Name=drive):			
			free = int(disk.FreeSpace) / 2**30
			free = round(free,2)
		return free
	except UnboundLocalError:
		return 'Drive Not Found'

def GetUsedDiskSpace(drive):
	drive = drive
	total = GetTotalDiskSpace(drive)
	free = GetFreeDiskSpace(drive)
	used = (total - free)
	used = round(used,2)
	return used

def GetPercentDiskUsage(drive):
	drive = drive
	total = GetTotalDiskSpace(drive)
	used = GetUsedDiskSpace(drive)
	per_used = (used * 100) / total
	per_used = round(per_used,2)
	return per_used 

def GetCpuList():
	'''
	Attempt to get a list containing the names of the CPUs in
	the system. This should be one name per physical CPU but
	it seems that hyper threading seems to make it show 2x the
	actual number.
	'''
	cpulist = []
	cpudict = {}
	for cpu in server.Win32_Processor():
		name = str(cpu.Name)
		deviceid = str(cpu.DeviceID)
		cpudict = {deviceid:name}
		cpulist.append(cpudict)
	return cpulist

def GetNumCpu():
	'''
	Call GetCpuList and then return the number of items in the list.
	'''
	cpus = GetCpuList()
	return len(cpus)

def GetServiceStatus(caption):
	caption = caption
	st='There is no service running with name : '+caption
	for svc in server.Win32_Service(Caption=caption):
		st = svc.State
	return str(st)

def GetNodeName():
	'''
	This is for when you are looking at a clustered env and
	want to know who the active node is.
	'''
	for os in server.Win32_OperatingSystem():
		activeNode = os.CSName
	return str(activeNode)



with open ('Config.json','r') as jsonString:
		jsonObject = json.load(jsonString)
		

hosts = jsonObject['Server List']
title = jsonObject['Title']
SMTPInfo = jsonObject['SMTPInfo']



htmlTitle = "<h1>"+title+"<h1>"
wholeHtmlBody = ''

for host in hosts:
	
	hostHtml = '<h2 align=left>'+host
	htmlHead = hostHtml+'<table style="font-family: \'Trebuchet MS\', Arial, Helvetica, sans-serif;border-collapse: collapse;width: 80%;" border=1 ><thead><tr><th style= "padding-top: 8; padding-bottom: 8;text-align: left; background:#66a0ff;color:white;border: 1px solid #ddd; padding: 4px;">S.No</th><th style= "padding-top: 8; padding-bottom: 8;text-align: left; background:#66a0ff;color:white;border: 1px solid #ddd; padding: 4px;">Drive</th><th style= "padding-top: 8; padding-bottom: 8;text-align: left; background:#66a0ff;color:white;border: 1px solid #ddd; padding: 4px;">Capacity</th><th style= "padding-top: 8; padding-bottom: 8;text-align: left; background:#66a0ff;color:white;border: 1px solid #ddd; padding: 4px;">Used Space</th><th style= "padding-top: 8; padding-bottom: 8;text-align: left; background:#66a0ff;color:white;border: 1px solid #ddd; padding: 4px;">Free Space</th><th style= "padding-top: 8; padding-bottom: 8;text-align: left; background:#66a0ff;color:white;border: 1px solid #ddd; padding: 4px;">Usage %</th></tr></thead>'
	
	innerBody = ''
	
	row = 1
	try :
		server = wmi.WMI(host)
		drives = (GetLocalDrives())
		for drive in drives:
				
			driveLetter = drive.replace(':','')
			capacity = str(GetTotalDiskSpace(drive))
			usedSpace = str(GetUsedDiskSpace(drive))
			freeSpace = str(GetFreeDiskSpace(drive))
			usedPercen = str(GetPercentDiskUsage(drive))
					
			innerBody = innerBody + '<tr><td style = "border: 1px solid #ddd; padding: 4px;">'+str(row)+'</td><td style = "border: 1px solid #ddd; padding: 4px;">'+driveLetter+'</td><td style = "border: 1px solid #ddd; padding: 4px;">'+capacity+'</td><td style = "border: 1px solid #ddd; padding: 4px;">'+usedSpace+'</td><td style = "border: 1px solid #ddd; padding: 4px;">'+freeSpace+'</td><td style = "border: 1px solid #ddd; padding: 4px;">'+usedPercen+'</td></tr>'
			row = row + 1
			
		hostBody = htmlHead + '<tbody>'+innerBody+'</tbody>' + '</table>'
		wholeHtmlBody = wholeHtmlBody + hostBody
	except Exception as e:
			error = str(e)
			rs = re.search("'(.*)'",error)
			if rs is None:
				error = '<table  border=1><thead><tr><th style=\'background:red ; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif; border-collapse: collapse;width:80%;\'>Unable to Access the Server</th></tr></thead></table>'
			else:
				error = '<table style=\'background:red\' border=1><thead><tr><th style=\'background:red ; font-family: "Trebuchet MS", Arial, Helvetica, sans-serif; border-collapse: collapse;width:80%;\'>'+rs.group(1)+'</tr></thead></table>'
			wholeHtmlBody = wholeHtmlBody + hostHtml + error			
			
mailbody = htmlTitle + wholeHtmlBody
mailbody = '<html><body>'+mailbody+'</body></html>'

SMTPInfo['body']=mailbody

# print (mailbody)

with open('test.html','w') as test:
	test.write(mailbody)
	
	

SendSMTPMail(SMTPInfo)
