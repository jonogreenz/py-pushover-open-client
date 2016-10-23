"""
In this example we pass a callback function the websocket to recieve real 
time messages. The callback will be passed messages in real time.

The example assumes the configuration provided already contains a
registered device.
"""
from pushover_open_client import Client

def messageCallback(messageList):
	#Prcoess/do work with messageList!
	if(messageList):
		for message in messageList:
		
			#Do work with message here!
		
			#Make sure to acknowledge messages with priority >= 2
			if(message.priority >= 2):
				if(message.acked != 1):
					client.acknowledgeEmergency(message.receipt)			
			
		#Make sure you delete messages that you recieve!
		client.deleteMessages(messageList[-1].id)

##Setups with a device configuration
client = Client("example_device.cfg")

#Get any messages sent before the client has started
messageList = client.getOutstandingMessages()

#Do work with outstanding messages

#Make sure you delete messages that you recieve!
if(messageList):
	client.deleteMessages(messageList[-1].id)

#Pass our function as a parameter, this will run 'forever'
client.getWebSocketMessages(messageCallback)

#Can optionally continue doing other work here without the need
#to poll the websocket