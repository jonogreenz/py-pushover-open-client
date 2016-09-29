import ConfigParser
import requests

BASE_URL = "https://api.pushover.net/1/"
LOGIN_URL = BASE_URL + "users/login.json"
DEVICE_URL = BASE_URL + "devices.json"
MESSAGES_URL = BASE_URL + "messages.json"
DELETE_URL = BASE_URL + "devices/" + "0000" + "/update_highest_message.json"
RECEIPT_URL = BASE_URL + "receipts/" + "0000" + "/acknowledge.json"

class Message:
	"""Just an easy way to wrap the message objects so we dont have to expose
	a lot of underlying json work in both websocket and getting outstanding messages"""
	
	def __init__(self, messageJson):
		"""TODO: Self.all_the_things set"""
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
		else if (requestType == 'get'):
			r = requests.get(url, jsonPayload)
			
		if(r != None):
			self.response = request.json()
			if 400 <= request.status_code < 500 or self.response["status"] == 0:
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
		"""TODO: Add possible global timeouts for certain functions to prevent spamming of gets/posts"""
		config = ConfigParser.RawConfigParser()
		config.read(configFile)
		self.email = config.get('Device', 'email')
		self.password = config.get('Device', 'password')
		self.secret = config.get('Device', 'secret')
		self.deviceID = config.get('Device', 'deviceID')
		self.userID = None
		
	def login(self):
		"""Logs in to an account using supplied information in configuration"""
		payload = {"email": self.email, "password": self.password}
		request = Request('post', LOGIN_URL, payload)
		if(request.response["status"] != 0):
			self.secret = request.response["secret"]
			self.userID = request.response["id"]
			
	def registerDevice(self, deviceName):
		"""Registers the client as active using supplied information in either
		configuration or after login"""
		if(self.secret != None):
			payload = {"secret": self.secret, "os": "O", "name": deviceName}
			request = Request('post', DEVICE_URL, payload)
			if(request.response["status"] != 0):
				self.deviceID = request.response["id"]
				#return getOutstandingMessages()
		else:
			print "Exception, secret is needed for device registration!"
			
	def writeConfig(self):
		"""TODO: Writes out a config file containing the updated params so that we
		don't need to do login or registration next time?"""
		pass
		
	def getOutstandingMessages(self):
		"""Returns json of outstanding messages after login and device registration"""
		if(self.deviceID != None and self.secret != None):
			payload = {"secret": self.secret, "device_id": self.deviceID}
			request = Request('get', MESSAGES_URL, payload)
			if(request.response["status"] != 0):
				#foreach message
				#create a message class and add to list
				#return the list
				pass
		
	def deleteMessages(self, highestID):
		"""Deletes all of the messages from pushover's server up to the highest messageID
		which is to be supplied by the user"""
		if(self.deviceID != None and self.secret != None):
			delStrURL = DELETE_URL.replace("0000", self.deviceID)
			payload = {"secret": self.secret, "message": highestID}
			request = Request('post', delStrURL, payload)
			if(request.response["status"] != 0):
				print "Deletion successful**** "
				
	def webSocketMessages(self):
		"""TODO: Do some fancy websocket stuff to listen for message requests in real time"""
		pass
		
	def acknowledgeEmergency(self, receiptID):
		"""Uses the receiptID which is supplied by the user to acknowledge emergency 
		priority messages"""
		if(self.secret != None):
			ackStrURL = RECEIPT_URL.replace("0000", receiptID)
			payload = {"secret": self.secret}
			request = Request('post', ackStrURL, payload)
			if(request.response["status"] != 0):
				print "Acknowledged successful**** "
			
		