#!/usr/bin/env python

import config
import subprocess
import time
from IPy import IP

print config.IFACE

iface_name = None
iface_addr = None
iface_netmask = None

def get_iface_addr(name):
	global iface_addr
	global iface_name
	
	if(name != iface_name):
		global iface_netmask
		iface_name = name
		info = subprocess.check_output(("./iface_addr.sh %s" % name).split(' ')).splitlines()
		iface_addr = info[0]
		iface_netmask = info[1]
		
	return iface_addr

def get_iface_mask(name):
	global iface_netmask
	global iface_name
	
	if(name != iface_name):
		global iface_addr
		iface_name = name
		info = subprocess.check_output(("./iface_addr.sh %s" % name).split(' ')).splitlines()
		iface_addr = info[0]
		iface_netmask = info[1]
		
	return iface_netmask

ip = get_iface_addr(config.IFACE)
mask = get_iface_mask(config.IFACE)

me = IP("%s" % ip)
net = me.make_net("%s" % mask)

print "Scanning network %s" % net

def scan(net):
	results = []
	# Scan the subnet for who's up
	scan_cmd = "nmap -sn 192.168.1.0/24 -oG -".split(' ')
	scan_results = subprocess.check_output(scan_cmd).splitlines()[1:-1]
	scan_results = map(lambda x: x.split('\t'), scan_results)
	for line in scan_results:
		host = IP(line[0].split(':')[1].split(' ')[1])
		status = line[1].split(':')[1].split(' ')[1]
		results.append([host, status])
	return results

def guess_os(target):
	ip = target[0]
	
	os_cmd = ("nmap -Pn -O %s" % ip).split(' ')
	guess_output = subprocess.check_output(os_cmd).splitlines()
	
	guess = "Unknown"
	
	for line in guess_output:
		idx = line.find("Running: ")
		if(idx != -1):
			guess = line[9:]			
			break
	return guess

def host_info(net):
	found = scan(net)	
	
	for machine in found:
		os = guess_os(machine)
		try:
			machine[2] = os
		except:
			machine.append(os)
	
	return found

hosts = host_info(net)

print(hosts)

print "sleeping..."
time.sleep(15)
print "awake!"

hosts2 = host_info(net)

diff = set(hosts).symmetric_difference(set(hosts2))

print(diff)
