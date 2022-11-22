import socket
import struct
import textwrap
import binascii
import struct
import sys,time

TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

DATA_TAB_1 = '\t   '
DATA_TAB_2 = '\t\t   '
DATA_TAB_3 = '\t\t\t   '
DATA_TAB_4 = '\t\t\t\t   '
print(" usage : python packet-sniffer2.py <ICMP/UDP/TCP>")
try:
	def main():
		conn = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

		filters = (["ICMP", 1, "ICMPv6"],["UDP", 17, "UDP"], ["TCP", 6, "TCP"])
		filter = []

		if len(sys.argv) == 2:
			print("This is the filter: ", sys.argv[1])
			for f in filters:
				if sys .argv[1] == f[0]:
					filter = f



		while True:
			raw_data, addr = conn.recvfrom(65536)
			dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)

			if eth_proto == 'IPV6':
				newPacket, nextProto = ipv6Header(data, filter)
				printPacketsV6(filter, nextProto, newPacket)

			elif eth_proto == 'IPV4':
				printPacketsV4(filter, data, raw_data)



	def printPacketsV4(filter, data, raw_data):
		(version, header_length, ttl, proto, src, target, data) = ipv4_Packet(data)

		# ICMP
		if proto == 1 and (len(filter) == 0 or filter[1] == 1):
			icmp_type, code, checksum, data = icmp_packet(data)
			print ("*******************ICMP***********************")
			print ("\tICMP type: %s" % (icmp_type))
			print ("\tICMP code: %s" % (code))
			print ("\tICMP checksum: %s" % (checksum))

		# TCP
		elif proto == 6 and (len(filter) == 0 or filter[1] == 6):
			print("*******************TCPv4***********************")
			print('Version: {}\nHeader Length: {}\nTTL: {}'.format(version, header_length, ttl))
			print('protocol: {}\nSource: {}\nTarget: {}'.format(proto, src, target))
			src_port, dest_port, sequence, acknowledgment, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin = struct.unpack(
				'! H H L L H H H H H H', raw_data[:24])
			print('*****TCP Segment*****')
			print('Source Port: {}\nDestination Port: {}'.format(src_port, dest_port))
			print('Sequence: {}\nAcknowledgment: {}'.format(sequence, acknowledgment))
			print('*****Flags*****')
			print('URG: {}\nACK: {}\nPSH: {}'.format(flag_urg, flag_ack, flag_psh))
			print('RST: {}\nSYN: {}\nFIN:{}'.format(flag_rst, flag_syn, flag_fin))

			if len(data) > 0:
				# HTTP
				if src_port == 80 or dest_port == 80:
					print('*****HTTP Data*****')
					try:
						http = HTTP(data)
						http_info = str(http.data).split('\n')
						for line in http_info:
							print(str(line))
					except:
						print(format_output_line("",data))
				else:
					print('*****TCP Data*****')
					print(format_output_line("",data))
		# UDP
		elif proto == 17 and (len(filter) == 0 or filter[1] == 17):
			print("*******************UDPv4***********************")
			print('Version: {}\nHeader Length: {}\nTTL: {}'.format(version, header_length, ttl))
			print('protocol: {}\nSource: {}\nTarget: {}'.format(proto, src, target))
			src_port, dest_port, length, data = udp_seg(data)
			print('*****UDP Segment*****')
			print('Source Port: {}\nDestination Port: {}\nLength: {}'.format(src_port, dest_port, length))


	def printPacketsV6(filter, nextProto, newPacket):
		remainingPacket = ""

		if (nextProto == 'ICMPv6' and (len(filter) == 0 or filter[2] == "ICMPv6")):
			remainingPacket = icmpv6Header(newPacket)
		elif (nextProto == 'TCP' and (len(filter) == 0 or filter[2] == "TCP")):
			remainingPacket = tcpHeader(newPacket)
		elif (nextProto == 'UDP' and (len(filter) == 0 or filter[2] == "UDP")):
			remainingPacket = udpHeader(newPacket)

		return remainingPacket


	def tcpHeader(newPacket):
		# 2 unsigned short,2unsigned Int,4 unsigned short. 2byt+2byt+4byt+4byt+2byt+2byt+2byt+2byt==20byts
		packet = struct.unpack("!2H2I4H", newPacket[0:20])
		srcPort = packet[0]
		dstPort = packet[1]
		sqncNum = packet[2]
		acknNum = packet[3]
		dataOffset = packet[4] >> 12
		reserved = (packet[4] >> 6) & 0x003F
		tcpFlags = packet[4] & 0x003F 
		urgFlag = tcpFlags & 0x0020 
		ackFlag = tcpFlags & 0x0010 
		pushFlag = tcpFlags & 0x0008  
		resetFlag = tcpFlags & 0x0004 
		synFlag = tcpFlags & 0x0002 
		finFlag = tcpFlags & 0x0001 
		window = packet[5]
		checkSum = packet[6]
		urgPntr = packet[7]

		print ("*******************TCP***********************")
		print ("\tSource Port: "+str(srcPort) )
		print ("\tDestination Port: "+str(dstPort) )
		print ("\tSequence Number: "+str(sqncNum) )
		print ("\tAck. Number: "+str(acknNum) )
		print ("\tData Offset: "+str(dataOffset) )
		print ("\tReserved: "+str(reserved) )
		print ("\tTCP Flags: "+str(tcpFlags) )

		if(urgFlag == 32):
			print ("\tUrgent Flag: Set")
		if(ackFlag == 16):
			print ("\tAck Flag: Set")
		if(pushFlag == 8):
			print ("\tPush Flag: Set")
		if(resetFlag == 4):
			print ("\tReset Flag: Set")
		if(synFlag == 2):
			print ("\tSyn Flag: Set")
		if(finFlag == True):
			print ("\tFin Flag: Set")

		print ("\tWindow: "+str(window))
		print ("\tChecksum: "+str(checkSum))
		print ("\tUrgent Pointer: "+str(urgPntr))
		print (" ")

		packet = packet[20:]
		return packet


	def udpHeader(newPacket):
		packet = struct.unpack("!4H", newPacket[0:8])
		srcPort = packet[0]
		dstPort = packet[1]
		lenght = packet[2]
		checkSum = packet[3]

		print ("*******************UDP***********************")
		print ("\tSource Port: "+str(srcPort))
		print ("\tDestination Port: "+str(dstPort))
		print ("\tLenght: "+str(lenght))
		print ("\tChecksum: "+str(checkSum))
		print (" ")

		packet = packet[8:]
		return packet


	def icmpv6Header(data):
		ipv6_icmp_type, ipv6_icmp_code, ipv6_icmp_chekcsum = struct.unpack(
			">BBH", data[:4])

		print ("*******************ICMPv6***********************")
		print ("\tICMPv6 type: %s" % (ipv6_icmp_type))
		print ("\tICMPv6 code: %s" % (ipv6_icmp_code))
		print ("\tICMPv6 checksum: %s" % (ipv6_icmp_chekcsum))

		data = data[4:]
		return data


	def nextHeader(ipv6_next_header):
		if (ipv6_next_header == 6):
			ipv6_next_header = 'TCP'
		elif (ipv6_next_header == 17):
			ipv6_next_header = 'UDP'
		elif (ipv6_next_header == 43):
			ipv6_next_header = 'Routing'
		elif (ipv6_next_header == 1):
			ipv6_next_header = 'ICMP'
		elif (ipv6_next_header == 58):
			ipv6_next_header = 'ICMPv6'
		elif (ipv6_next_header == 44):
			ipv6_next_header = 'Fragment'
		elif (ipv6_next_header == 0):
			ipv6_next_header = 'HOPOPT'
		elif (ipv6_next_header == 60):
			ipv6_next_header = 'Destination'
		elif (ipv6_next_header == 51):
			ipv6_next_header = 'Authentication'
		elif (ipv6_next_header == 50):
			ipv6_next_header = 'Encapsuling'

		return ipv6_next_header


	def ipv6Header(data, filter):
		ipv6_first_word, ipv6_payload_legth, ipv6_next_header, ipv6_hoplimit = struct.unpack(
			">IHBB", data[0:8])
		ipv6_src_ip = socket.inet_ntop(socket.AF_INET6, data[8:24])
		ipv6_dst_ip = socket.inet_ntop(socket.AF_INET6, data[24:40])

		bin(ipv6_first_word)
		"{0:b}".format(ipv6_first_word)
		version = ipv6_first_word >> 28
		traffic_class = ipv6_first_word >> 16
		traffic_class = int(traffic_class) & 4095
		flow_label = int(ipv6_first_word) & 65535

		ipv6_next_header = nextHeader(ipv6_next_header)
		data = data[40:]

		return data, ipv6_next_header


	# Unpack Ethernet Frame
	def ethernet_frame(data):
		proto = ""
		IpHeader = struct.unpack("!6s6sH",data[0:14])
		dstMac = binascii.hexlify(IpHeader[0]) 
		srcMac = binascii.hexlify(IpHeader[1]) 
		protoType = IpHeader[2] 
		nextProto = hex(protoType) 

		if (nextProto == '0x800'): 
			proto = 'IPV4'
		elif (nextProto == '0x86dd'): 
			proto = 'IPV6'

		data = data[14:]

		return dstMac, srcMac, proto, data

		# Format MAC Address
	def get_mac_addr(bytes_addr):
		bytes_str = map('{:02x}'.format, bytes_addr)
		mac_addr = ':'.join(bytes_str).upper()
		return mac_addr

	# Unpack IPv4 Packets Recieved
	def ipv4_Packet(data):
		version_header_len = data[0]
		version = version_header_len >> 4
		header_len = (version_header_len & 15) * 4
		ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', data[:20])
		return version, header_len, ttl, proto, ipv4(src), ipv4(target), data[header_len:]

	# Returns Formatted IP Address
	def ipv4(addr):
		return '.'.join(map(str, addr))


	# Unpacks for any ICMP Packet
	def icmp_packet(data):
		icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
		return icmp_type, code, checksum, data[4:]

	# Unpacks for any TCP Packet
	def tcp_seg(data):
		(src_port, dest_port, sequence, acknowledgement, offset_reserved_flag) = struct.unpack('! H H L L H', data[:14])
		offset = (offset_reserved_flag >> 12) * 4
		flag_urg = (offset_reserved_flag & 32) >> 5
		flag_ack = (offset_reserved_flag & 32) >> 4
		flag_psh = (offset_reserved_flag & 32) >> 3
		flag_rst = (offset_reserved_flag & 32) >> 2
		flag_syn = (offset_reserved_flag & 32) >> 1
		flag_fin = (offset_reserved_flag & 32) >> 1

		return src_port, dest_port, sequence, acknowledgement, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[offset:]


	# Unpacks for any UDP Packet
	def udp_seg(data):
		src_port, dest_port, size = struct.unpack('! H H 2x H', data[:8])
		return src_port, dest_port, size, data[8:]

	# Formats the output line
	def format_output_line(prefix, string):
		size=80
		size -= len(prefix)
		if isinstance(string, bytes):
			string = ''.join(r'\x{:02x}'.format(byte) for byte in string)
			if size % 2:
				size-= 1
				return '\n'.join([prefix + line for line in textwrap.wrap(string, size)])


	main()
except KeyboardInterrupt:
	print("\n\033[91m [-] Exiting...")
time.sleep(4)
