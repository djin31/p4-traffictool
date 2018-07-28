from scapy.all import *

##class definitions
class Ethernet(Packet):
	name = 'ethernet'
	fields_desc = [
		XBitField('dstAddr', 0, 48),
		XBitField('srcAddr', 0, 48),
		XShortField('etherType', 0),
	]
class Ipv4(Packet):
	name = 'ipv4'
	fields_desc = [
		XBitField('version', 0, 4),
		XBitField('ihl', 0, 4),
		XByteField('diffserv', 0),
		XShortField('totalLen', 0),
		XShortField('identification', 0),
		XBitField('flags', 0, 3),
		XBitField('fragOffset', 0, 13),
		XByteField('ttl', 0),
		XByteField('protocol', 0),
		XShortField('hdrChecksum', 0),
		XLongField('srcAddr', 0),
		XLongField('dstAddr', 0),
	]
	#update hdrChecksum over [[u'ipv4', u'version'], [u'ipv4', u'ihl'], [u'ipv4', u'diffserv'], [u'ipv4', u'totalLen'], [u'ipv4', u'identification'], [u'ipv4', u'flags'], [u'ipv4', u'fragOffset'], [u'ipv4', u'ttl'], [u'ipv4', u'protocol'], [u'ipv4', u'srcAddr'], [u'ipv4', u'dstAddr']] using csum16 in post_build method

class Q_meta(Packet):
	name = 'q_meta'
	fields_desc = [
		XShortField('flow_id', 0),
		XShortField('_pad0', 0),
		XBitField('ingress_global_tstamp', 0, 48),
		XShortField('_pad1', 0),
		XBitField('egress_global_tstamp', 0, 48),
		XBitField('_spare_pad_bits', 0, 15),
		XBitField('markbit', 0, 1),
		XBitField('_pad2', 0, 13),
		XBitField('enq_qdepth', 0, 19),
		XBitField('_pad3', 0, 13),
		XBitField('deq_qdepth', 0, 19),
	]
class Snapshot(Packet):
	name = 'snapshot'
	fields_desc = [
		XShortField('ingress_global_tstamp_hi_16', 0),
		XLongField('ingress_global_tstamp_lo_32', 0),
		XLongField('egress_global_tstamp_lo_32', 0),
		XLongField('enq_qdepth', 0),
		XLongField('deq_qdepth', 0),
		XShortField('_pad0', 0),
		XBitField('orig_egress_global_tstamp', 0, 48),
		XShortField('_pad1', 0),
		XBitField('new_egress_global_tstamp', 0, 48),
		XLongField('new_enq_tstamp', 0),
	]
class Udp(Packet):
	name = 'udp'
	fields_desc = [
		XShortField('srcPort', 0),
		XShortField('dstPort', 0),
		XShortField('hdr_length', 0),
		XShortField('checksum', 0),
	]

##bindings
bind_layers(Ethernet, Ipv4, etherType = 0x0800)
bind_layers(Ipv4, Udp, protocol = 0x11)
bind_layers(Udp, Q_meta, dstPort = 0x1e61)
bind_layers(Udp, Snapshot, dstPort = 0x22b8)

##packet_list
possible_packets_ = [
	(Ethernet()),
	(Ethernet()/Ipv4()),
	(Ethernet()/Ipv4()/Udp()),
	(Ethernet()/Ipv4()/Udp()/Q_meta()),
	(Ethernet()/Ipv4()/Udp()/Snapshot())
]