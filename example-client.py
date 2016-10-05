from pushover_open_client import Client


#If first time setup

#client = Client("our.cfg")
#client.login()
#client.registerDevice("nameHere")
#client.writeConfig("mainUser.cfg")

#After first time
#client = Client("mainUser.cfg")
#client.getOustandingMessages()
#client.deleteMessages(highestID)
#client.getWebSocketMessages(workerFunction,False)
#Connect to websocket and listen
#do work here

client = Client("testDevice2.cfg")

"""messages = client.getOutstandingMessages()
highestID = 0
for m in messages:
	highestID = m.id
	print (m.priority)
	print ("")"""
	
client.getWebSocketMessages(None)

	
#client.deleteMessages(highestID)

#isTrue = True
#while(isTrue):
#	messages = client.getWebSocketMessages()
#	isTrue = False()



#Write some sample clients
#TODO:
#Write one for initial logging in
#Write two separate ones for the two different methods of recieving notifications
#Actually make the setup.py work properly :)
#Update license/accreditation to people
#Write a good readme file
#Consider leaving messages as a dictionary rather than changing them