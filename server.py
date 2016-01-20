from twisted.internet.protocol import Protocol, Factory
from twisted.internet import task
from twisted.internet import reactor

import time
import datetime

def sendDataToClients():
	for client in factory.clients:
		msg = "I saw a cat at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		client.message(msg)
		print "Sending Data To: ", client
				
class SocketServer(Protocol):

	def message(self, message):
		self.transport.write(message + '\n')	
	
	def connectionMade(self):
		#self.transport.write("""connected""")
		self.factory.clients.append(self)
		print "clients are ", self.factory.clients
	
	def connectionLost(self, reason):
	    self.factory.clients.remove(self)
	    print "Closing Connection ", self
	
	def dataReceived(self, data):
	    #print "data is ", data
		a = data.split(':')
		if len(a) > 1:
			command = a[0]
			content = a[1]
			msg = ""
			
			if command == "helo":
				self.name = content
				msg = "hello" + self.name
				for c in self.factory.clients:
					c.message(msg)
				
			if command == "msg":
				msg = self.name + ": " + content
				for c in self.factory.clients:
					c.message(msg)
					
			if command == "begin":
				dataTask.start(1.0)
				
			if command == "end":
				dataTask.stop

#main					
factory = Factory()
factory.protocol = SocketServer
factory.clients = []
dataTask = task.LoopingCall(sendDataToClients)
reactor.listenTCP(85, factory)
print "Simple TCP Server Starting..."
reactor.run()



