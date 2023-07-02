import wexpect
import sys
import time

child = wexpect.spawn('ssh jetson-nano@192.168.43.80')
child.expect("jetson-nano@192.168.43.80's password:")
child.sendline("123456")

child.sendline("sudo reboot")
child.expect("jetson-nano@jetsonnano:~")
child.sendline("123456")

child.sendline("whoami")

child.close()





