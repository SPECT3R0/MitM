
import argparse
import logging
import asyncio
from modules.core import start_sniffer
from modules import *

# Updated ASCII art for the banner to say "MitM"
BANNER = """
███╗   ███╗ ██╗████████╗███╗   ███╗
████╗ ████║ ██║╚══██╔══╝████╗ ████║
██╔████╔██║ ██║   ██║   ██╔████╔██║
██║╚██╔╝██║ ██║   ██║   ██║╚██╔╝██║
██║ ╚═╝ ██║ ██║   ██║   ██║ ╚═╝ ██║
╚═╝     ╚═╝ ╚═╝   ╚═╝   ╚═╝     ╚═╝

-------- Author: SPECT3R --------
"""

logger = logging.getLogger(__name__)

def colorize(text, red, green, blue):
    """Convert text to RGB color."""
    return f"\033[38;2;{red};{green};{blue}m{text}\033[0m"

async def run_cli(config):
    # Set up logging to console for CLI visibility, in addition to file logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    
    # RGB coloring for the banner (Dark Purple for a spooky effect)
    print(colorize(BANNER, 80, 0, 80))
    print(colorize("[ EchoMitM - Offensive Network Security Framework ]", 170, 0, 0))  # Dark Red for impact
    print(colorize("[ Haunted by SPECT3R ]\n", 128, 0, 128))  # Dark Purple for ghostly effect

    parser = argparse.ArgumentParser(description="EchoMitM - Unleashing Digital Phantoms")
    parser.add_argument('command', choices=['arp_spoof', 'dns_spoof', 'ssl_strip', 'http_inject', 'analyze', 'stop'], help='Choose your haunting operation')
    parser.add_argument('--content', help='Content for HTTP injection', default="alert('Haunted by EchoMitM');")

    args = parser.parse_args()

    handlers = []
    if args.command == 'arp_spoof':
        handlers.append(start_spoofing)
        print(colorize("[ ARP Spoofing - Spirits Unleashed ]", 170, 0, 0))  # Dark Red
    elif args.command == 'dns_spoof':
        handlers.append(dns_spoof)
        print(colorize("[ DNS Spoofing - Phantom Domains ]", 170, 0, 0))  # Dark Red
    elif args.command == 'ssl_strip':
        handlers.append(ssl_strip)
        print(colorize("[ SSL Stripping - Eerie Eavesdropping ]", 170, 0, 0))  # Dark Red
    elif args.command == 'http_inject':
        handlers.append(lambda packet, config: inject_content(packet, config))
        print(colorize("[ HTTP Injection - Malevolent Whispers ]", 170, 0, 0))  # Dark Red
    elif args.command == 'analyze':
        analyze_traffic()
        print(colorize("[ Traffic Analysis - Spectral Surveillance ]", 0, 0, 170))  # Dark Blue
    elif args.command == 'stop':
        handlers.append(stop_spoofing)
        handlers.append(lambda packet, config: False)  
        print(colorize("[ Stopping All Operations - The Haunting Ceases ]", 128, 128, 0))  # Dark Yellow

    try:
        await start_sniffer(config, handlers)
    except Exception as e:
        logger.error(colorize(f"[ Error Encountered - A Ghastly Glitch ]: {e}", 170, 0, 0))  # Dark Red

if __name__ == "__main__":
    asyncio.run(run_cli(load_config()))
