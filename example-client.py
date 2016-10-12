from pushover_open_client import Client
from time import sleep

client = Client("testDevice2.cfg")

"""messages = client.getOutstandingMessages()
highestID = 0
for m in messages:
	highestID = m.id
	print (m.priority)
	print ("")"""
	
while(True):
    messageList = client.getWebSocketMessages()

    #Prcoess/do work with messageList!
    if(messageList):
        for message in messageList:

            #Do work with message here!
            print(message.message)

            #Make sure to acknowledge messages with priority >= 2
            if(message.priority >= 2):
                client.acknowledgeEmergency(message.receipt)            

        #Make sure you delete messages that you recieve!
        client.deleteMessages(messageList[-1].id)

    sleep(5) #Wait a few seconds between requests

	
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