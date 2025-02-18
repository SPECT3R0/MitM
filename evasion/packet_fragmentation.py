import logging
from scapy.all import *

logger = logging.getLogger(__name__)

def fragment_packet(packet, config):
    """
    Fragments a packet to bypass some detection mechanisms.
    """
    try:
        if config.get('evasion', {}).get('use_fragmentation', False):
            if packet.haslayer(IP):
                try:
                    # Fragment the packet. Here, we fragment based on a size of 50 bytes for demonstration
                    fragmented = fragment(packet, fragsize=50)
                    for frag in fragmented:
                        send(frag, verbose=False)
                    logger.info("Packet fragmented and sent.")
                    return True  # Return True to indicate the packet was sent fragmented
                except Exception as e:
                    logger.error(f"Fragmentation failed: {e}")
        return False  # Return False if no fragmentation occurred
    except Exception as e:
        logger.error(f"Fragmentation error: {e}")
        return False
