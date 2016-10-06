import socket
import sys


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("193.136.138.142",59100)  
messageULQ = 'ULQ\n'
messageUNQ='UNQ '
messageTRQ='TRQ '
lista=[]
varis=[]
inte=0


def comTRS_t():
	
	socke = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	lista=var.split(None)
	size_lista=len(lista)
	amount_words=len(lista)-3
	words=lista[3:]
	words_w_space=" ".join(words)
	
	
	message= messageTRQ + "t " + str(amount_words) + " " + words_w_space +"\n"
	
	
	# Connect the socket to the port where the server is listening
	
	s=("193.136.138.142",59100)
	socke.connect(s)
	  
	try:
		# Send data
	
		socke.sendall(message.encode())

		# Look for the response
		amount_received = 0
		amount_expected = len(message)
    
		while amount_received < amount_expected:
			data = socke.recv(16)
			amount_received += len(data)
			print  (data.decode(),file=sys.stderr)

	finally:
		
		socke.close()

def comTRS_f():
	# Create a TCP socket
	socki = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	lista=var.split(None)
	image=str(lista[3])
	message= messageTRQ + "f " + str(lista[3])  +" 13775 data\n"
	print (message)
	
	s=("193.136.138.142",59100)
	socki.connect(s)
		  
	try:
		socki.sendall(message.encode())
		f = open(image,'rb')
		l = f.read(1024)
		while (l):
			socki.send(l)
			l = f.read(1024)
			
		f.close()
		
		socki.shutdown(socket.SHUT_WR)
		data=socki.recv(1024)
		print  (data.decode(),file=sys.stderr)
		socki.close() 		
	
	finally:
	
		socki.close()	  


def comUDP_TCS_request():
	global lista
	
	# Send data
	message =messageUNQ + "lista[(int(var.split(" ")[1])-1)]"+"\n"
	sent = sock.sendto(message.encode(), server_address)            
                         
                         
	# Receive response

	data, server = sock.recvfrom(4096)
	
	return data

def comUDP_TCS_list():
      
         
	# Send data
	
	sent = sock.sendto(messageULQ.encode(), server_address)            
            
            
	# Receive response
	
	data, server = sock.recvfrom(4096)

	return data

def writeLang(data):
	global lista
	a,b=data.decode().split(" ",1)
	if a=="ULR":
		c,d=b.split(" ",1)
		l=str.split(d)
		lista=l
		i=1
		while i<=int(c):
			print("%d-%s"%(i,l[i-1]))
			i+=1
	return
          
while True:
	var= input()
   
	if var=="exit":
		sock.close()        
		break
    
	elif (var.split(" ")[0]=="request") and (var.split(" ")[1].isdigit()) and((var.split(" ")[2]=="t")or (var.split(" ")[2]=="f")):
		#resp=comUDP_TCS_request()
		if var.split(" ")[2]=="t":
			comTRS_t()
		elif var.split(" ")[2]=="f":
			comTRS_f()
		#if  "EOF" in resp or "ERR" in resp:
		    
			  
                    
                    
                   
	elif var=="list":
		data=comUDP_TCS_list()
		writeLang(data) 
	else:
		print("Erro no comando")
    
