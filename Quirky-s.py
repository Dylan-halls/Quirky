from __future__ import print_function
from Crypto.Cipher import AES
input = raw_input
import socket, threading, os, datetime, multiprocessing
import time, sys, subprocess, base64, ConfigParser

try:
	cpus = multiprocessing.cpu_count()
	cfg = ConfigParser.RawConfigParser()
	conffile = 'Quirky.cfg'
	cfg.read(conffile)

	banner = """
	            ___        _      _             _____ _____ ____  
	           / _ \ _   _(_)_ __| | ___   _   |  ___|_   _|  _ \ 
	          | | | | | | | | '__| |/ / | | |  | |_    | | | |_) |
	          | |_| | |_| | | |  |   <| |_| |  |  _|   | | |  __/ 
	           \___/\___,_|_|_|  |_|\_____, |  |_|     |_| |_|    
	                                   |___/         

	         """  

	PADDING = '{'
	BLOCK_SIZE = 32
	pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
	EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
	DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)          

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
			#[word for word in wordlist if any(letter in word for letter in 'aqk')]
			
			if cfg.get('Shell_Handler', 'stay_in_dir') == 'yes':
				
				if ';' in cmd:
					sock.send("Must Stay in this Directory!")
					print ("[\033[1;94m{}\033[00m] \033[1;31m{} {} {} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), 'Detected Malicous Command From', addr[0].strip(), '->', cmd))
				
				elif ':' in cmd:
					sock.send("Must Stay in this Directory!")
					print ("[\033[1;94m{}\033[00m] \033[1;31m{} {} {} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), 'Detected Malicous Command From', addr[0].strip(),'->', cmd))

				elif '|' in cmd:
					sock.send("Must Stay in this Directory!")
					print ("[\033[1;94m{}\033[00m] \033[1;31m{} {} {} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), 'Detected Malicous Command From', addr[0].strip(), '->', cmd))

				elif '&' in cmd:
					sock.send("Must Stay in this Directory!")
					print ("[\033[1;94m{}\033[00m] \033[1;31m{} {} {} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), 'Detected Malicous Command From', addr[0].strip(), '->', cmd))

				elif 'wget' in cmd:
					sock.send("At least have the decenty to use Quirky in a Quirky Shell!")
					print ("[\033[1;94m{}\033[00m] \033[1;31m{} {} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), 'Aha', addr[0].strip(), 'tryed to use wget'))

				else:
					she = cfg.get('Shell_Handler', 'shell')
					scmd = [she,'-c', cmd]
					rcmd = subprocess.Popen(scmd, stdout=subprocess.PIPE)
					sock.send(rcmd.communicate()[0])
					print ("[\033[1;94m{}\033[00m] \033[0;33m{} {} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), str(addr[0]), 'Called:', cmd))

			else:
				she = cfg.get('Shell_Handler', 'shell')
				scmd = [she,'-c', cmd]
				rcmd = subprocess.Popen(scmd, stdout=subprocess.PIPE)
				sock.send(rcmd.communicate()[0])
				print ("[\033[1;94m{}\033[00m] \033[0;33m{} {} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), str(addr[0]), 'Called:', cmd))
			
	def upload_handler(name, sock, addr):
	   global now
	   now = datetime.datetime.now()
	   filename = sock.recv(1024)
	   filesize = sock.recv(1024)
	   print ("[\033[1;94m{}\033[00m] \033[0;33m{}\033[00m \033[1;32m{} {} {} {} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"),'PUT', filename, filesize, 'Bytes',  'from', str(addr[0])))
	   f = open(filename, 'wb')
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

	def Main(EncodeAES, DecodeAES, pad, PADDING):
	    host = cfg.get('Server-Options', 'Bind_IP')
	    sport = cfg.get('Server-Options', 'Bind_Port')
	    port = int(sport)

	    s = socket.socket()
	    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	    s.bind((host,port))

	    s.listen(50)
	    conns = [1,2,3,4,5]
	    now = datetime.datetime.now()
	    
	    if cfg.get('Banner', 'show') == 'yes':
	    	if cfg.get('Banner', 'color') == 'yes':
	    		print('\033[1;34m{}\033[00m'.format(banner))
	    	else:
	    		print(banner)
	    else: pass
	    print ("[\033[1;94m{}\033[00m] \033[1;35m{}{} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), 'Running on ', host, port))
	    print ("[\033[1;94m{}\033[00m] \033[1;35m{}{}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), 'Running in: ', os.getcwd()))
	    for i in range(1, 51):
		    if i < 50:
		    	print ("[\033[1;94m{}\033[00m] \033[1;33m{} {}\033[00m".format(now.strftime("%Y-%m-%d %H:%M"), 'Open For Connection', i))
		        c, addr = s.accept()
		        key = cfg.get('Encryption', 'key')
		        c.send(key)
		        cipher = AES.new(key)
		        time.sleep(1)
		        e_passwd = c.recv(1024)
		        passwd = DecodeAES(cipher, e_passwd)
		  
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
except KeyboardInterrupt:
	pass

if __name__ == '__main__':
	try:
		jobs = []
		for i in range (cpus):
			p = multiprocessing.Process(target=Main(EncodeAES, DecodeAES, pad, PADDING))
			jobs.append(p)
			p.start()
	except KeyboardInterrupt:
		pass