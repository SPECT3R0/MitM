import argparse
import logging
import asyncio
from modules.core import start_sniffer
from modules import *

# Updated ASCII art for the banner to say "MitM"
BANNER = """
  _______  _______  _______  _______  _______ 
 (  ____ \(  ___  )(  ____ \(  ____ )(  ____ \\
 | (    \\/| (   ) || (    \\/| (    )|| (    \\/
 | |      | |   | || (_____ | (____)|| (_____ 
 | | ____ | |   | ||_______)|  _____)(_____  )
 | | \\_  )| |   | |       ) || (            ) |
 | (___) || (___) |/\\____) || )      /\\____) |
 (_______)(_______)\\_______)|/       \\_______)
     __  __               ______  
    / / / /_  ______     / ____/  
   / /_/ / / / / __ \\   / __/     
  / __  / /_/ / / / /  / /___     
 /_/ /_/\\__,_/_/ /_/  /_____/  MitM
"""

logger = logging.getLogger(__name__)

async def run_cli(config):
    # Set up logging to console for CLI visibility, in addition to file logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    
    print("\033[91m" + BANNER + "\033[0m")  # Red color for the banner
    print("\033[93m[ EchoMitM - Offensive Network Security Framework ]\033[0m")
    print("\033[92m[ Owned by SPECT3R ]\033[0m\n")

    parser = argparse.ArgumentParser(description="EchoMitM - Unleashing Network Chaos")
    parser.add_argument('command', choices=['arp_spoof', 'dns_spoof', 'ssl_strip', 'http_inject', 'analyze', 'stop'], help='Choose your operation')
    parser.add_argument('--content', help='Content for HTTP injection', default="alert('Injected by EchoMitM');")

    args = parser.parse_args()

    handlers = []
    if args.command == 'arp_spoof':
        handlers.append(start_spoofing)
        print("\033[91m[ ARP Spoofing Initiated ]\033[0m")
    elif args.command == 'dns_spoof':
        handlers.append(dns_spoof)
        print("\033[91m[ DNS Spoofing Initiated ]\033[0m")
    elif args.command == 'ssl_strip':
        handlers.append(ssl_strip)
        print("\033[91m[ SSL Stripping Initiated ]\033[0m")
    elif args.command == 'http_inject':
        handlers.append(lambda packet, config: inject_content(packet, config))
        print("\033[91m[ HTTP Injection Initiated ]\033[0m")
    elif args.command == 'analyze':
        analyze_traffic()
        print("\033[94m[ Traffic Analysis Initiated ]\033[0m")
    elif args.command == 'stop':
        handlers.append(stop_spoofing)
        handlers.append(lambda packet, config: False)  
        print("\033[93m[ Stopping All Operations ]\033[0m")

    try:
        await start_sniffer(config, handlers)
    except Exception as e:
        logger.error(f"\033[91m[ Error Encountered ]\033[0m: {e}")

if __name__ == "__main__":
    asyncio.run(run_cli(load_config()))
