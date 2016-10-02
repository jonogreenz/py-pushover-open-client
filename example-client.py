from pushover_client import Client


#If first time setup

#client = Client("our.cfg")
#client.login()
#client.registerDevice("nameHere")
#client.writeConfig("mainUser.cfg")

#After first time
#client = Client("mainUser.cfg")
#client.getOustandingMessages()
#Connect to websocket and listen
#do work here

client = Client("newUser.cfg")

messages = client.getOutstandingMessages()
highestID = 0
for m in messages:
	highestID = m.id
	print (m.id)
	print ("")
	
client.deleteMessages(highestID)

isTrue = True
while(isTrue):
	messages = client.getWebSocketMessages()
	isTrue = False()