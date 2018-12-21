#!/usr/bin/python

import pty, sys, threading, socket
from subprocess import Popen, PIPE, STDOUT
from time import sleep
from os import fork, waitpid, execv, read, write

global vars

class newthread(threading.Thread): # Use this to create a new thread for each host. Probably with a for loop.
	def __init__(self, host, type):
		threading.Thread.__init__(self)
		self.host = host
		self.type = type
		print("[+] Running %s setup for %s..." % type, host)
		self.run()
		
	def run(self):
		try:
			setup(self.host, self.type) # TODO: write setup()
			print("[+] %s setup complete." % self.host)
		except:
			print("[-] %s setup failed for reason %s" % self.host, error)

class ssh(): # Shamelessly stolen from stackoverflow and modified slightly to support threading
    def __init__(self, host, execute='echo "done" > /root/testing.txt', askpass=True, user='assessor', password=b'SuperSecurePassword'):
        self.execute = execute
        self.host = host
        self.user = user
        self.password = password
        self.askpass = askpass
        self.run()

    def run(self):
        command = [
                '/usr/bin/ssh',
                self.user+'@'+self.host,
                '-o', 'NumberOfPasswordPrompts=1',
                self.execute,
        ]

        # PID = 0 for child, and the PID of the child for the parent    
        pid, child_fd = pty.fork()

        if not pid: # Child process
            # Replace child process with our SSH process
            execv(command[0], command)

        ## if we havn't setup pub-key authentication
        ## we can loop for a password promt and "insert" the password.
        while self.askpass:
            try:
                output = read(child_fd, 1024).strip()
            except:
                break
            lower = output.lower()
            # Write the password
            if b'password:' in lower:
                write(child_fd, self.password + b'\n')
                break
            elif b'are you sure you want to continue connecting' in lower:
                # Adding key to known_hosts
                write(child_fd, b'yes\n')
            elif b'company privacy warning' in lower:
                pass # This is an understood message
            else:
                print('Error:',output)

        waitpid(pid, 0)

functions
def main(): # Here's where the magic happens
	tmpscheme = [ i+'.' for i in getip().split('.')[:3]]
	tmpscheme.extend(('0', '/24'))
	scheme = ''.join(tmpscheme)
	gethostnames(scheme)
	
def getip(): # abuse sockets to find our IP
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		s.connect(('10.255.255.255', 1))
		IP = s.getsockname()[0]
	except:
		IP = '127.0.0.1'
	finally:
		s.close()
	return IP

def gethostnames(scheme): # Using the schema for IPs, find all active hosts

def ntp(host): # Set NTP

def docker(host): # Install docker containers

def elastic(host): # Configure elastic.yml

def moloch(host): # Fix moloch


if __name__ == '__main__':
	main()
