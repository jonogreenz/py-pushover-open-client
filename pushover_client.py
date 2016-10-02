import json
import requests

BASE_URL = "https://api.pushover.net/1/"
LOGIN_URL = BASE_URL + "users/login.json"
DEVICE_URL = BASE_URL + "devices.json"
MESSAGES_URL = BASE_URL + "messages.json"
DELETE_URL = BASE_URL + "devices/" + "0000" + "/update_highest_message.json"
RECEIPT_URL = BASE_URL + "receipts/" + "0000" + "/acknowledge.json"


class Message:
	"""Just an easy way to wrap the message objects
	so we dont have to expose a lot of underlying json work
	in both websocket and getting outstanding messages"""
	
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
		pass

class Websocket:
	"""Class to represent the websocket connection to the push server.
	Helps abstract away alot of the data from the client"""
	
	def __init__(self):
		"""TODO: Setup socketio or something to wait for specific frames
		that are sent by the server, and to retrieve messages etc"""
		"""Flask-SocketIO?"""
		pass
		
	def connectClient(self, deviceID, secret):
		"""Connects the client to the webserver"""
		self.connected = False
		pass
		
	def isConnected(self):
		return self.connected
		
	def getMessages(self):
		"""This will be where the new messages will appear to be retrieved"""
		"""Then flush out the messages to be updated"""
		pass

class Request:
	"""This is the class that allows requesting to the Pushover servers"""
	
	def __init__(self, requestType, url, jsonPayload):
		"""Eg. 'post', 'LOGIN_URL', {'json': 555}"""
		"""TODO: Proper error handling.../exceptions,
		Set status to 0 and give error even when its not a server error
		Eg. 404 not found gives back to the caller a status and error they		
		can check """
		r = None
		if(requestType == 'post'):
			r = requests.post(url, jsonPayload)
		elif (requestType == 'get'):
			r = requests.get(url, jsonPayload)
			
		if(r != None):
			self.response = r.json()
			if 400 <= r.status_code < 500 or self.response["status"] == 0:
				#self.errors = self.response["errors"]
				self.response["status"] = 0
	
	def __str__(self):
		return str(self.response)


class Client:
	"""This is the class that represents this specific user and device that
	we are logging in from. All messages we receive are sent to this Client."""
	
	def __init__(self, configFile):
		"""Attempts to load and parse the configuration file"""
		"""TODO: Error handling :) """
		"""TODO: Add possible global timeouts for certain functions to prevent
		spamming of gets/posts"""
		with open(configFile, 'r') as infile:
			jsonConfig = json.load(infile)
		
		self.email = jsonConfig["email"]
		self.password = jsonConfig["password"]
		self.secret = jsonConfig["secret"]
		self.deviceID = jsonConfig["deviceID"]
		self.userID = jsonConfig["userID"]
		
		self.websocket = Websocket()
		
	def writeConfig(self, configFile):
		"""Writes out a config file containing the updated params so that
		in the future you dont need to register the device/get secret/user key"""
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
				
	def getWebSocketMessages(self):
		"""TODO: Do some fancy websocket stuff to listen for
		message requests in real time"""
		
		"""wait for any timeout to be respectful to api"""
		
		
		"""If not connected, connect to wss://client.pushover.net/push over https"""
		"""Login using "login:"+self.deviceID+":"+self.secret+"\n" """
		if(not self.websocket.isConnected()):
			self.websocket.connectClient()
		
		"""Depends on what websocket thing we are using, but get outstanding messages
		from the socket"""
		pass
		
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
			
		