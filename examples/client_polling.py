"""
In this example we poll the websocket in order to recieve real time
messages from the provided websocket.

The example assumes the configuration provided already contains a
registered device.
"""
from pushover_open_client import Client
from time import sleep

##Setups with a device configuration
client = Client("example_device.cfg")

#Get any messages sent before the client has started
messageList = client.getOutstandingMessages()

#Do work with outstanding messages

#Make sure you delete messages that you recieve!
if(messageList):
	client.deleteMessages(messageList[-1].id)

#Our polling loop
while(True):
	messageList = client.getWebSocketMessages()
	
	#Prcoess/do work with messageList!
	if(messageList):
		for message in messageList:
		
			#Do work with message here!
		
			#Make sure to acknowledge messages with priority >= 2
			if(message.priority >= 2):
				if(message.acked != 1):
					client.acknowledgeEmergency(message.receipt)			
			
		#Make sure you delete messages that you recieve!
		#Input is the message id of the latest you wish to delete
		client.deleteMessages(messageList[-1].id)
	
	sleep(5) #Wait a few seconds between requests
