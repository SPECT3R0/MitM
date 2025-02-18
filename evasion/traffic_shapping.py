import logging
import random
import time
from scapy.all import *

logger = logging.getLogger(__name__)

def shape_traffic(packet, config):
    """
    Shapes the traffic by introducing random delays and possibly adjusting packet sizes.
    """
    try:
        if config.get('evasion', {}).get('traffic_shaping', False):
            # Introduce a random delay to mimic normal network behavior
            delay = random.uniform(0.01, 0.1)  # Random delay between 10ms and 100ms
            time.sleep(delay)
            
            # Optionally, adjust packet size but ensure it doesn't break the packet
            if packet.haslayer(IP):
                original_len = packet[IP].len
                new_len = max(64, min(original_len + random.randint(-10, 10), 1500))  # Between MTU limits
                if new_len != original_len:
                    # Create a new packet with adjusted size, ensuring all layers are preserved
                    new_packet = packet.copy()
                    new_packet[IP].len = new_len
                    # Adjust payload or padding if necessary, this is a simplified example
                    if new_len > original_len:
                        padding = b'\x00' * (new_len - original_len)
                        new_packet[IP].payload.add_payload(Raw(load=padding))
                    else:
                        new_packet[IP].payload.load = new_packet[IP].payload.load[:new_len - original_len]
                    return new_packet
        return packet
    except Exception as e:
        logger.error(f"Traffic shaping error: {e}")
        return packet  # Return the original packet in case of any error
