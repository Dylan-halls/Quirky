from __future__ import print_function
from Crypto.Cipher import AES
input = raw_input
import socket, sys, getpass, pwd, os, stat, time, base64

try:
	host = sys.argv[1]
	fil = sys.argv[2]
	mode = sys.argv[3]
except Exception, e:
	print("Usage:")
	print("\tQuirky-c <ip> <filename> [--option]\n")
	print("\t--download          Download file from server")
	print("\t--upload            Upload file to server")
	print("\t--shell             Request a limited shell from the server\n\t                    (run without filename)\n")
	exit(-1)

port = 554
s = socket.socket()
print("[\033[1;94m+\033[00m] Opening Socket")

try:
   s.connect((host, port))
   BLOCK_SIZE = 16
   key = os.urandom(BLOCK_SIZE)

   PADDING = '{'
   pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
   cipher = AES.new(key)
   EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
   DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
except socket.error:
   print("[\033[1;31m!\033[00m] Connection was Refused... is the server running?")
   exit()

s.send(key)
i_passwd = getpass.getpass("[\033[1;94m+\033[00m] Password: ")
e_passwd = EncodeAES(cipher, i_passwd)
s.send(e_passwd)
time.sleep(1)

if mode == '--download':
   s.send("d")
   time.sleep(0.10)
elif mode == '--upload':
   s.send("u")
   time.sleep(0.10)
elif mode == '--shell':
   time.sleep(0.10)
   s.send("s")

def shell(host):
	time.sleep(1)
	cmd = ''
	print("[\033[1;94m+\033[00m] Serving Shell")
	user = getpass.getuser()
	while cmd != 'q':
		cmd = input("\033[1;31m{}{}{}\033[00m \033[1;94m{}\033[00m".format(user, '@', host, '~$ '))
		s.send(cmd)
		print(s.recv(9999))

def upload():
	s.send(fil)
	time.sleep(1)
	s.send(str(os.path.getsize(fil)))
	filesize = long(os.path.getsize(fil))
	with open(fil, 'rb') as f:
		bytesToSend = f.read(1024)
		bytecount = len(bytesToSend)
		s.send(bytesToSend)
		while bytesToSend != "":
			bytesToSend = f.read(1024)
			bytecount += len(bytesToSend)
			s.send(bytesToSend)
			sys.stdout.write("\r[\033[1;94m+\033[00m] {0:2f}".format((bytecount/float(filesize))*100)+"%")
			sys.stdout.flush()
		print("\n[\033[1;94m+\033[00m] Upload Complete")
	s.close()

def download():
	print("[\033[1;94m+\033[00m] Connecting to {}:{}".format(host,port))

	filename = fil
	if filename != 'q':
		s.send(filename)
		data = s.recv(1024)                            #(" + str(filesize)+" Bytes)
		if data[:6] == 'EXISTS':
			filesize = long(data[6:])
			message = input("[\033[1;94m+\033[00m] Download "+ filename+ " (" + str(filesize)+" Bytes) [y/n]: ").lower()
			if message == 'y':
				s.send("OK")
				f = open("new" + filename, 'wb')
				data = s.recv(1024)
				totalrecv = len(data)
				f.write(data)
				while totalrecv < filesize:
					data = s.recv(1024)
					totalrecv += len(data)
					f.write(data)
					sys.stdout.write("\r[\033[1;94m+\033[00m] {0:2f}".format((totalrecv/float(filesize))*100)+"%")
					sys.stdout.flush()

				print("\n[\033[1;94m+\033[00m] Download Complete")
		else:
			print("[\033[1;31m!\033[00m] File Does not Exist!!")

	s.close()

if __name__ == '__main__':
    
    if str(sys.argv[3]) == '--download':
        download()
    elif str(sys.argv[3]) == '--upload':
        upload()
    elif str(sys.argv[3]) == '--shell':
        shell(host)
    
	