import os
import smtplib
import keyring
import json


def SendMailAlert(smtpData,hostData):
	server = smtpData['serverName']
	port = smtpData['port']
	sender = smtpData['sender']	
	password = keyring.get_password(server,sender)
	receivers = hostData['receivers']
	fromPerson = smtpData['fromName']
	engagement = hostData['engagement']
	subject = hostname+' is Down for '+engagement+' !!!' #+ "Test mail, Please ignore"
	toPerson = ';'.join(receivers)
	
	message = "From:"+fromPerson+"\nTo:"+toPerson+"\nMIME-Version: 1.0\nContent-type: text/html\nSubject: "+subject+"\n\n\nHi Team,<br/><br/>"+hostname+" is Down for "+engagement+"<br/><br/>Please check the issue<br/><br/><br/><br/><b>P.S</b><br/>This is a System Generated Mail."
	
	smtpObj = smtplib.SMTP(server,port)
	smtpObj.starttls()
	smtpObj.login(sender,password)
	smtpObj.sendmail(sender, receivers, message) 

	

with open('D:\Python\Configuration.json') as file:
		jsonData = json.load(file)
		

		
hostDetails = jsonData['hostDetails']
smtpData = jsonData['smtpDetails']



for hostData in hostDetails:
	hostname = hostData['hostName']
	response = os.system('ping "'+hostname+'"')
	
	if response == 0:
		print(hostname , " is up and running.")
	else:
		print(hostname, " is Down !!!")
		SendMailAlert(smtpData,hostData)
	



	
