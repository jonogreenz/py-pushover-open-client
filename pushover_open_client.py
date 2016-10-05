import json
import threading
import requests
import websocket

WEBSOCKET_URL = "wss://client.pushover.net/push"
BASE_URL = "https://api.pushover.net/1/"
LOGIN_URL = BASE_URL + "users/login.json"
DEVICE_URL = BASE_URL + "devices.json"
MESSAGES_URL = BASE_URL + "messages.json"
DELETE_URL = BASE_URL + "devices/" + "0000" + "/update_highest_message.json"
RECEIPT_URL = BASE_URL + "receipts/" + "0000" + "/acknowledge.json"

class Message:
	"""Just an easy way to wrap the message objects
	so we dont have to expose a lot of underlying json work
	in both websocket and outstanding messages"""
	
	def __init__(self, messageJson):
		"""Sets all the parts of the message so that can be used easily"""
		"""Always exist"""
		self.id = messageJson["id"]
		self.umid = messageJson["umid"]
		self.title = messageJson["title"]
		self.message = messageJson["message"]
		self.app = messageJson["app"]
		self.aid = messageJson["aid"]
		self.icon = messageJson["icon"]
		self.date = messageJson["date"]
		self.priority = messageJson["priority"]
		"""Conditionals"""
		if("sound" in messageJson):
			self.sound = messageJson["sound"]
		if("url" in messageJson):
			self.url = messageJson["url"]
		if("url_title" in messageJson):
			self.url_title = messageJson["url_title"]
		if("acked" in messageJson):
			self.acked = messageJson["acked"]
		if("receipt" in messageJson):
			self.receipt = messageJson["receipt"]
		if("html" in messageJson):
			self.html = messageJson["html"]

class Request:
	"""This is the class that allows requesting to the Pushover servers"""
	
	def __init__(self, requestType, url, jsonPayload):
		"""Eg. 'post', 'LOGIN_URL', {'name': value}"""
		r = None
		self.response = {'status': 0} #Initial response, in case exception is raised
		try:
			if(requestType == 'post'):
				r = requests.post(url, jsonPayload)
			elif (requestType == 'get'):
				r = requests.get(url, jsonPayload)
				
			if(r != None):
				self.response = r.json()
				if 400 <= r.status_code < 500 or self.response["status"] == 0:
					#TODO: Print errors - self.response["errors"]
					self.response["status"] = 0
		except requests.exceptions.RequestException as e:
			#Some exception has been raised, set status as 0 before returning
			print (e)
			self.response["status"] = 0
	
	def __str__(self):
		return str(self.response)

class WSClient:
	"""Class to represent the websocket connection to the push server.
	Helps abstract away alot of the data from the client
	This uses websocket-client to maintain a connection.
	Further information can be found at https://pushover.net/api/client"""
	
	"""TODO: Use the keep-alive packet to determine that the connection
	is still being kept alive and well?"""
	"""TODO: Ensure we can keyboard interrupt websocket
	to stop execution"""
	
	def __init__(self, inClient):
		self.connected = False
		self.ws = None
		self.client = inClient
		self.mainMutex = threading.Lock()
		self.mainThread = None
		self.callback = None
		self.trace = False
		self.unseenMessages = []
		
	"""External functions for use by the client"""
	def isConnected(self):
		"""Checks if we're connected to the websocket"""
		#self.mainMutex.acquire()
		isCon = self.connected
		#self.mainMutex.release()
		return isCon
		
	def getMessages(self):
		"""Allows messages to be retrieved by the user. Messages
		are passed here when no callback method is supplied to the
		websocket"""
		#self.mainMutex.acquire()
		returnMessages = self.unseenMessages
		self.unseenMessages = []
		#self.mainMutex.release()
		return returnMessages
		
	def disconnect(self):
		"""Disconnects the client from the websocket"""
		if(isConnected()):
			self.ws.close()
			self.mainThread.join()
		else:
			print ("Attemping to disconnect but not connected.")
	
	def connect(self, callback, traceRoute):
		"""Connects the client to the websocket"""
		if(not self.isConnected()):
			if(traceRoute):
				#Enables tracing of connection
				self.trace = True
				websocket.enableTrace(True)
			#Set callback for received messages to go to
			self.callback = callback
			#Have to put this in here, otherwise respawned dies for some reason
			self.ws = websocket.WebSocketApp(WEBSOCKET_URL,
								on_message = self.onRecieve,
								on_error = self.onError,
								on_close = self.onClose)
			self.ws.on_open = self.onOpen
			#Start the actual connection
			self.mainThread = threading.Thread(target = self.ws.run_forever, args=())
			self.mainThread.start()
		else:
			print ("Attempting to connect but already connected.")
		
	"""Internal functions/callbacks"""
	def respawnConnection(self):
		"""Respawns connection to websocket after drop request by Pushover"""
		#Wait for last websocket thread to finish
		self.mainThread.join()
		#Spawn new websocket
		self.connect(self.callback, self.trace)
	
	def onOpen(self, ws):
		"""After connecting, 'logs into' the websocket"""
		print ("Websocket connection opened.")
		self.connected = True
		self.ws.send("login:"+self.client.deviceID+":"+self.client.secret+"\n")
	
	def onRecieve(self, ws, message):
		"""Handles pushover's frames which tell us if messages have
		arrived, or whether to reconnect"""
		
		str = message.decode('utf-8')
		if(str == '#'):
			#Keep alive packet, nothing to be done
			pass
		elif(str == "!"):
			#A new message! Flush the messages. Assumes previous have been deleted
			messages = self.client.getOutstandingMessages()
			#If we've been supplied a callback, send the messages to it
			#otherwise give to getMessages for people to retrieve
			if(self.callback == None):
				#Check message isn't already in the unseen list
				for i in messages: #Sorry for the very un-pythonic way
					inSeen = False
					for j in unseenMessages:
						if(i.id == j.id):
							inSeen = True
					if(not inSeen):
						self.unseenMessages.append(i)
			else:
				self.callback(messages)
		elif(str == "R"):
			#A reload request, time to drop connection and recon
			self.ws.close()
			#We must spawn a new thread in order to reconnect after this thread dies
			aThread = threading.Thread(target = self.respawnConnection, args=())
			aThread.start()
		elif(str == "E"):
			#A permanent error occurred (such as settings wrong details)
			#Terminate connection and request the user fix
			self.ws.close()
			print ("Exception, an error has occurred with websocket! Please"
					"check the details you have provided in configuration.")
		
	def onError(self, ws, error):
		"""When websocket recieves an error it ends up here"""
		print (error)
		
	def onClose(self, ws):
		"""After closing websocket"""
		print ("Websocket connection closed.")
		self.connected = False	

class Client:
	"""This is the class that represents this specific user and device that
	we are logging in from. All messages we receive are sent to this Client."""
	
	def __init__(self, configFile):
		"""Attempts to load and parse the configuration file"""
		"""TODO: Error handling and proper exceptions """
		"""TODO: Add possible global timeouts for certain functions to prevent
		spamming of gets/posts"""
		with open(configFile, 'r') as infile:
			jsonConfig = json.load(infile)
		
		self.email = jsonConfig["email"]
		self.password = jsonConfig["password"]
		self.secret = jsonConfig["secret"]
		self.deviceID = jsonConfig["deviceID"]
		self.userID = jsonConfig["userID"]
		
		self.websocket = WSClient(self)
		
	def writeConfig(self, configFile):
		"""Writes out a config file containing the updated params so that
		in the future you don't need to register the device/get secret/user key"""
		with open(configFile, 'w') as outfile:
			json.dump({
				'email': self.email,
				'password': self.password,
				'secret': self.secret,
				'deviceID': self.deviceID,
				'userID': self.userID
				}, outfile, indent=4)
		
	def login(self):
		"""Logs in to an account using supplied information in configuration"""
		payload = {"email": self.email, "password": self.password}
		request = Request('post', LOGIN_URL, payload)
		if(request.response["status"] != 0):
			self.secret = request.response["secret"]
			self.userID = request.response["id"]
		else:
			print ("Could not login. Please check your details are correct.")
			
	def registerDevice(self, deviceName):
		"""Registers the client as active using supplied information in either
		configuration or after login"""
		if(self.secret):
			payload = {"secret": self.secret, "os": "O", "name": deviceName}
			request = Request('post', DEVICE_URL, payload)
			if(request.response["status"] != 0):
				self.deviceID = request.response["id"]
				#return getOutstandingMessages()
			else:
				print ("Could not register device. Check device name is unique and try "
						"again later.")
		else:
			print ("Exception, secret is needed for device registration!")
		
	def getOutstandingMessages(self):
		"""Returns json of outstanding messages after login
		and device registration"""
		if(self.deviceID and self.secret):
			payload = {"secret": self.secret, "device_id": self.deviceID}
			request = Request('get', MESSAGES_URL, payload)
			if(request.response["status"] != 0):
				#foreach message
				messageList = []
				for message in request.response["messages"]:
					#create a message class and add to list
					thisMessage = Message(message)
					messageList.append(thisMessage)
				#return the list
				return messageList
			else:
				print ("Could not retrieve outstanding messages. Try again later.")
		else:
			print ("Exception, deviceID and secret is needed for retrieving messages!")
		
	def deleteMessages(self, highestID):
		"""Deletes all of the messages from pushover's server up to
		the highest messageID which is to be supplied by the user"""
		if(highestID > 0):
			if(self.deviceID or self.secret):
				delStrURL = DELETE_URL.replace("0000", self.deviceID)
				payload = {"secret": self.secret, "message": highestID}
				request = Request('post', delStrURL, payload)
				if(request.response["status"] != 0):
					#print ("Deletion successful")
					pass
				else:
					print ("Could not delete messages. Try again later.")
			else:
				print ("Exception, deviceID and secret is needed for deleting messages!")
				
	def getWebSocketMessages(self, messageCallback = None, traceRoute = False):
		"""Connects to PushOver's websocket to receive real-time notifications.
		Can be used in two ways:
			- Can be polled periodically by a calling function
			- Can be passed in a callback function which will execute every 
			  time a message is received (recommended)
		"""
		if(messageCallback == None):
			#Assuming that the user is going to do something with the messages
			#outside of this function, and will repeatedly poll this function
			if(not self.websocket.isConnected()):
				self.websocket.connect(None, traceRoute)
			return self.websocket.getMessages()
		else:
			#Assume this function is a one off call
			#Give the callback to websocket to do its thing. 
			#This bypasses getting the messages separately. Thats it
			if(not self.websocket.isConnected()):
				self.websocket.connect(messageCallback, traceRoute)
		
	def acknowledgeEmergency(self, receiptID):
		"""Uses the receiptID which is supplied by the user to acknowledge emergency 
		priority messages"""
		if(self.secret):
			ackStrURL = RECEIPT_URL.replace("0000", receiptID)
			payload = {"secret": self.secret}
			request = Request('post', ackStrURL, payload)
			if(request.response["status"] != 0):
				#print ("Acknowledged successful")
				pass
			else:
				print ("Could not acknowledge emergency priority message. "
						"Try again later.")
		else:
			print ("Exception, secret is needed for deleting messages!")