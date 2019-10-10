from intervaltree import IntervalTree, Interval
from  ipaddress import ip_interface
import pprint
import csv

class Firewall:
	def __init__(self, path):
		self.rules = {}
		with open(path, mode='r', encoding='utf-8-sig') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				direction, protocol, port, ip_address = self._parse_row(
					row[0], row[1], row[2], row[3])
				self._create_rule(direction, protocol, port, ip_address)
	
	def _parse_row(self, direction_str, protocol_str, port_str, ip_address_str):
		direction = direction_str
		protocol = protocol_str
		port = port_str
		if '-' in port:
			port = (int(port.split('-')[0]), int(port.split('-')[1]))
		else:
			port = (int(port))
		ip_address = ip_address_str
		if '-' in ip_address:
			ip_address = (ip_address.split('-')[0], ip_address.split('-')[1])
		else:
			ip_address = (ip_address)
		return  direction, protocol, port, ip_address
			

	def _create_rule(self, direction, protocol, port, ip_address):
		if direction in self.rules:
			if protocol in self.rules[direction]:
				if ip_address in self.rules[direction][protocol]:
					if isinstance(port, int):
						self.rules[direction][protocol][ip_address].add(Interval(port, port+1))
					else:
						self.rules[direction][protocol][ip_address].add(Interval(port[0],port[1]+1))
					self.rules[direction][protocol][ip_address].merge_overlaps()
				else:
					interval_tree = self._create_interval_tree(port)
					self.rules[direction][protocol][ip_address] = interval_tree
			else:
				interval_tree = self._create_interval_tree(port)
				self.rules[direction][protocol] = {ip_address: interval_tree}
		else:
			interval_tree = self._create_interval_tree(port)
			self.rules[direction] = {protocol: {ip_address: interval_tree}}
			
	def _create_interval_tree(self, int_or_tuple):
		tree = IntervalTree()
		if isinstance(int_or_tuple, int):
			tree.add(Interval(int_or_tuple, int_or_tuple+1)) # non inclusive on upper
		else:
			tree.add(Interval(int_or_tuple[0], int_or_tuple[1]))
		return tree

	def accept_packet(self, direction, protocol, port, ip_address):
		if direction not in self.rules:
			return False
		if protocol not in self.rules[direction]:
			return False
		if ip_address in self.rules[direction][protocol]:
			if self.rules[direction][protocol][ip_address].overlaps(port):
				return True
		else:
			for ip in self.rules[direction][protocol]:
				if isinstance(ip, tuple):
					min_ip = ip_interface(ip[0])
					max_ip = ip_interface(ip[1])
					cur_ip = ip_interface(ip_address)
					if cur_ip >= min_ip and cur_ip <= max_ip:
						if self.rules[direction][protocol][ip].overlaps(port):
							return True
		return False

if __name__ == "__main__":
	filepath = 'db.csv'
	fw = Firewall(filepath)
	
	print("\n\nSimple Pass / No Pass Firewall Implementation\n\n")
	pp = pprint.PrettyPrinter(indent=4)
	print("Rules ingested from {}: ".format(filepath))
	pp.pprint(fw.rules)
	print("\n\n")

	# Test cases
	tc1 = ['outbound', 'tcp', 10000, '192.168.10.11']
	tc2 = ['outbound', 'tcp', 200000, '192.168.10.11']
	tc3 = ['outbound', 'tcp', 200001, '192.168.10.11']
	tc4 = ['inbound', 'udp', 53, '192.168.1.1']
	tc5 = ['inbound', 'udp', 53, '192.168.2.5']
	tc6 = ['inbound', 'udp', 53, '192.168.2.6']
	if fw.accept_packet(tc1[0], tc1[1], tc1[2], tc1[3]):
		print("Test case 1 passed: {}".format(tc1))
	if fw.accept_packet(tc2[0], tc2[1], tc2[2], tc2[3]):
		print("Test case 2 passed: {}".format(tc2))
	if not fw.accept_packet(tc3[0], tc3[1], tc3[2], tc3[3]):
		print("Test case 3 passed: {}".format(tc3))
	if fw.accept_packet(tc4[0], tc4[1], tc4[2], tc4[3]):
		print("Test case 4 passed: {}".format(tc4))
	if fw.accept_packet(tc5[0], tc5[1], tc5[2], tc5[3]):
		print("Test case 5 passed: {}".format(tc5))
	if not fw.accept_packet(tc6[0], tc6[1], tc6[2], tc6[3]):
		print("Test case 6 passed: {}".format(tc6))
	
