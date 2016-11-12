from __future__ import print_function
input = raw_input
import socket, threading, os, datetime, multiprocessing, time, sys, subprocess

cpus = multiprocessing.cpu_count()

banner = """
            ___        _      _             _____ _____ ____  
           / _ \ _   _(_)_ __| | ___   _   |  ___|_   _|  _ \ 
          | | | | | | | | '__| |/ / | | |  | |_    | | | |_) |
          | |_| | |_| | | |  |   <| |_| |  |  _|   | | |  __/ 
           \___/\___,_|_|_|  |_|\_____, |  |_|     |_| |_|    
                                   |___/         

         """            

def long_print(color, *args):
	global now
	now = datetime.datetime.now()
	if color == 'yellow':
		print ("[\033[1;94m{}\033[00m] \033[1;33m{}{}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), str(args)))
	elif color == 'green':
		print ("[\033[1;94m{}\033[00m] \033[1;32m{}{}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), str(args)))
	elif color == 'red':
		print ("[\033[1;94m{}\033[00m] \033[1;31m{}{}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), str(args)))

def shell_handler(name, sock, addr):
	global now
	now = datetime.datetime.now()
	cmd = 's'
	print ("[\033[1;94m{}\033[00m] \033[0;33m{} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"),'Serving Limited Shell To', str(addr[0])))
	while len(cmd) > 0:
		cmd = sock.recv(9999)
		banned = [';', '|', '&', '&&', '..']
		if str(banned) in cmd:
			sock.send("Must Stay in this Directory!")
			print ("[\033[1;94m{}\033[00m] \033[1;31m{} {} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), str(addr[0]), 'Detected Malicous Command: ', cmd))
		scmd = ['/bin/sh', '-c', cmd]
		rcmd = subprocess.Popen(scmd, stdout=subprocess.PIPE)
		sock.send(rcmd.communicate()[0])
		print ("[\033[1;94m{}\033[00m] \033[0;33m{} {} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), str(addr[0]), 'Called:', cmd))

def upload_handler(name, sock, addr):
   global now
   now = datetime.datetime.now()
   filename = sock.recv(1024)
   filesize = sock.recv(1024)
   print ("[\033[1;94m{}\033[00m] \033[0;33m{}\033[00m \033[1;32m{} {} {} {} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"),'PUT', filename, filesize, 'Bytes',  'from', str(addr[0])))
   f = open("new" + filename, 'wb')
   data = sock.recv(1024)
   totalrecv = len(data)
   f.write(data)
   while totalrecv < filesize:
      data = sock.recv(1024)
      totalrecv += len(data)
      f.write(data)
      
   print("done")	
   sock.close()

def download_handler(name, sock, addr):
	global now
	now = datetime.datetime.now()
	try:
		filename = sock.recv(1024)
		if os.path.isfile(filename):
			sock.send("EXISTS " + str(os.path.getsize(filename)))
			print ("[\033[1;94m{}\033[00m] \033[1;32m{} {}\033[00m\033[0;33m {}\033[00m \033[1;32m{} {} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), str(addr[0]), filename, 'EXISTS', 'and is', str(os.path.getsize(filename)), 'Bytes'))
			userResponse = sock.recv(1024)
			if userResponse[:2] == 'OK':
				print ("[\033[1;94m{}\033[00m] \033[0;33m{}\033[00m \033[1;32m{} {} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"),'GET', filename, 'for', str(addr[0])))
				with open(filename, 'rb') as f:
					bytesToSend = f.read(1024)
					sock.send(bytesToSend)
					while bytesToSend != "":
						bytesToSend = f.read(1024)
						sock.send(bytesToSend)
	except Exception:
		pass
	else:
		sock.send("ERR ")
		print ("[\033[1;94m{}\033[00m] \033[1;31m{} {} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), str(addr[0]), filename, 'does not exist'))
	sock.close()

def Main():
    host = '127.0.0.1'
    port = 554


    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,port))

    s.listen(50)
    conns = [1,2,3,4,5]
    now = datetime.datetime.now()
    
    print(banner)
    print ("[\033[1;94m{}\033[00m] \033[1;35m{}{}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), 'Running in: ', os.getcwd()))
    for i in range(1, 51):
	    if i < 50:
	    	print ("[\033[1;94m{}\033[00m] \033[1;33m{} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), 'Open For Connection', i))
	        c, addr = s.accept()
	        passwd = c.recv(1024)
	  
	        try:
	           print ("[\033[1;94m{}\033[00m] \033[1;35m{} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), 'Authenticating With', addr[0]))
	           if passwd == 'pass':
	           	  pass
	              
	           else:
	           	  c.close()
	           	  print ("[\033[1;94m{}\033[00m] \033[1;31m{}{}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), str(addr[0]), ' Failed Authentication'))
	           	  print ("[\033[1;94m{}\033[00m] \033[1;31m{} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), 'Shutting Down', str(addr[0])))
	           	  c.close()

	           print ("[\033[1;94m{}\033[00m] \033[1;32m{}{}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), 'Got Connection from: ', socket.gethostbyaddr(str(addr)[0])))
	        except socket.gaierror:
	           print ("[\033[1;94m{}\033[00m] \033[1;32m{}{}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), 'Got Connection from: ', str(addr[0])))
	        
	        try:
		        mode = c.recv(1024)
		        if mode == 'd':
			       try:
			           t = threading.Thread(target=download_handler, args=("download_handler", c, addr))
			           t.start()
			       except Exception as e:
			           print(type(e))
			           print(e)
				   
		        elif mode == 'u':
			       try:
			           t = threading.Thread(target=upload_handler, args=("upload_handler", c, addr))
			           t.start()
			       except Exception as e:
			           print(type(e))
			           print(e)
			       
		        elif mode == 's':
			       try:
			           t = threading.Thread(target=shell_handler, args=("shell_handler", c, addr))
			           t.start()
			       except Exception as e:
			           print(type(e))
			           print(e)

			       
		        else:
		        	print(mode)
			        print("UNKNOWN OPTION")
			        exit()
	        except Exception:
	        	pass
  
         
    s.close()

if __name__ == '__main__':
	Main()
	"""
	jobs = []
	for i in range (cpus):
		p = multiprocessing.Process(target=Main())
		jobs.append(p)
		p.start()"""