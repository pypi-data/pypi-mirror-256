from cryptography.fernet import Fernet
from threading import Thread
import pickle as json
import socket

__session__ = {}
__run__ = True

EncryptionMode = b'Tq_hBOzVozSYvyX8cvvqGZrmzkgaGssB99-azrqCleg='

class Container:

	def __getiteme__(self,parm):
		return __session__.get(parm)
		
	def __setiteme__(self,parm,value):
		__session__[parm] = value
		
	def __enter__(self):
		return self
		
	def __exit__(self,x,z,y):
		print('__exit__ function :- ',x,z,y)
		
	def get(self,parm):
		return __session__.get(parm)
		
	def all(self):
		return [x for x in __session__.values()]
		
	def count(self):
		return len(__session__.values())
		
	def pop(self,parm):
		return __session__.pop(parm)
	
class Encryption:

	def __init__(self,key=EncryptionMode):
		from cryptography.fernet import Fernet
		self.__Key = Fernet(key)

	def encrypt(self,data:bytes):
		try:
			return self.__Key.encrypt(data)
		except:
			raise KeyError(f'bad key {self.__code}')

	def decrypt(self,data:bytes):
		try:
			return self.__Key.decrypt(data)
		except:
			raise KeyError(f'bad key {self.__code}')

class Bridge:

	def __init__(self,server,code=EncryptionMode):
		self.__server = server
		self.__end_of_bytes = b'<end_of_bytes>'
		self.__enc = Encryption(key=code)
		self.data = b''

	def Link(addr):
		soc = socket.socket()
		soc.connect(addr)
		return Bridge(soc)

	def Check(data):
		try:
			json.dumps(data)
			return True
		except:
			raise KeyError("can't puck this type of data")

	def SendBuffer(self,string):
		try:
			if Bridge.Check(string):
				Buffer = self.__enc.encrypt(json.dumps(string))
				self.__server.send(Buffer+self.__end_of_bytes)
			else:
				raise KeyError('SendSBuffer accepts only (bool , tuple , str , list , set , dict , int , bytes)')
		except TypeError:
			raise KeyError('SendBuffer accepts only (bool , tuple , str , list , set , dict , int , bytes)')
		except ConnectionResetError:
			raise ConnectionResetError('desconnected')

	def RecvBuffer(self,re=1024,max_value=-1):
		try:
			while self.__end_of_bytes not in self.data:
				self.data += self.__server.recv(re)
				if len(self.data) >= max_value and max_value != -1:
					raise Error.BufferDataError(f'the data bigger than {max_value}')
			later_bit = self.data[self.data.find(self.__end_of_bytes)+len(self.__end_of_bytes):]
			pyl = json.loads(self.__enc.decrypt(self.data[:self.data.find(self.__end_of_bytes)]))
			self.data = later_bit
			return pyl
		except ConnectionResetError:
			raise ConnectionResetError('desconnected')
			
	def TimeOut(self,out):
		self.__server.settimeout(out)

	def Close(self):
		self.__server.close()
	
class Error:

	class ServerInitializeError:

		def __init__(self,er):
			self.er = er
			
class Server:

	def __init__(self,addr):
		self.addr = addr
		self.ip , self.port = addr
		self.loop = 0

	def __tunnel__(ser,session):
		global sessions
		while True:
			try:
				client , addr = ser.accept()
				session[addr] = Bridge(client)
			except OSError:
				break

	def init(self):
		self.ser = socket.socket()
		self.ser.bind(self.addr)
		self.ser.listen()
		
	def listen(self):
		if hasattr(self,'ser'):
			Thread(target=Server.__tunnel__,args=(self.ser,__session__)).start()
			return Container()
		else:
			raise Error.ServerInitializeError('the init function must be called')

	def listen_on(self,func):
		if hasattr(self,'ser'):
			Thread(target=func,args=(self.ser,__session__)).start()
		else:
			raise Error.ServerInitializeError('the init function must be called')
			
	def stop(self):
		global __run__
		__run__ = False
		self.ser.close()