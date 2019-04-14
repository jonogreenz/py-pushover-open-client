# Python Pushover Open Client
py-pushover-open-client aims to provide unofficial Python bindings for [Pushover's Open Client API](https://pushover.net/api/client).

## Usage

### Setup

```
pip3 install py-pushover-open-client 
```

Or simply clone this repository, change into it's root directory and run "pip3 install ."

### How to Use
You can now import the main client using:
```python
from pushover_open_client import Client
```

Please see the examples provided for more detail.

#### Device Registration
The first step is to register a new desktop device with the Pushover servers. This gives us certain device properties, specifically a secret, user key and device key, which can be saved and used by our client to recieve messages.  

To do this, you must setup a configuration file in JSON format containing your Pushover's email and password as below:

```
{
	"email": "myPushoverEmail@example.com",
	"password": "myPushoverPassword",
	"secret": "",
	"deviceID": "",
	"userID": ""
}
```


Then run code that looks like below. Replace "*deviceName*" with a device name between 0 and 25 characters long, "*yourInConfig.cfg*" with the name of your input configuration file, and "*yourOutConfig.cfg*" with the name intended for your output configuration file.  
*Note: These can be the same name if you wish.*

```python
from pushover_open_client import Client

client = Client("yourInConfig.cfg")
client.login()
client.registerDevice("deviceName")
client.writeConfig("yourOutConfig.cfg")
```

Assuming the *deviceName* has not already been taken, your new device will be registered!  

*Note: If you receive an error message saying you could not register the device, try changing the name to be a unique name.*

#### Receiving Messages
Once you have completed registration of the device, you want to continue to use the output configuration file which was written during registration. This will contain the information needed to log in to the servers and to receive messages.

When you initially start a client, you will want to flush out any previously recorded messages. This is also a good way to test that your registration has been successful, as you will receive at least one test message from Pushover.

To do this, start a new session using the written configuration and get any outstanding messages as below:
```python
client = Client("yourOutConfig.cfg")
messageList = client.getOustandingMessages()

#Process/do work with messageList
if(messageList):
	for m in messageList:
		print m.message

	client.deleteMessages(messageList[-1].id)
```

After you have flushed out any previous messages, you can connect to the websocket to receive real time messages! This can be done in one of two methods - via **polling**, or via passing in a **callback function** (recommended). Here are examples of both:

##### **Polling:**
```python
while(True):
	messageList = client.getWebSocketMessages()

	#Prcoess/do work with messageList!
	if(messageList):
		for message in messageList:
		
			#Do work with message here!

			#Make sure to acknowledge messages with priority >= 2
			if(message.priority >= 2):
				client.acknowledgeEmergency(message.receipt)			
			
		#Make sure you delete messages that you recieve!
		client.deleteMessages(messageList[-1].id)
	
	sleep(5) #Wait a few seconds between requests
```

##### **Callback:**
```python
def messageCallback(messageList):
	#Prcoess/do work with messageList!
	if(messageList):
		for message in messageList:
		
			#Do work with message here!
		
			#Make sure to acknowledge messages with priority >= 2
			if(message.priority >= 2):
				client.acknowledgeEmergency(message.receipt)			
			
		#Make sure you delete messages that you recieve!
		client.deleteMessages(messageList[-1].id)

client.getWebSocketMessages(messageCallback)	
```

**_And that's it!_** Please remember to be responsible when accessing Pushover's API!

#### Message Object
Please see [the open client documentation](https://pushover.net/api/client#download) for information regarding what each message contains. Conditional elements are set to None if they do not exist to prevent exceptions.
```
All Messages Include:
id, umid, title, message, app, aid, icon, date, priority

Some Messages Conditionally Include: 
sound, url, url_title, acked, receipt, html
```

## Acknowledgments
Thanks to the developers of:
* websocket-client
* requests

This client is not written or supported by Superblock, the creators of Pushover.

