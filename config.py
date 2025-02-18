import yaml
import logging
import subprocess
import random

logger = logging.getLogger(__name__)

def load_config():
    try:
        with open('config.yaml', 'r') as stream:
            config = yaml.safe_load(stream)
        
        # Dynamic IP acquisition for testing
        config['targets'][0]['ip'] = subprocess.check_output(['dig', '+short', 'myip.opendns.com', '@resolver1.opendns.com']).decode().strip()
        config['targets'][0]['gateway'] = '8.8.8.8'  # Fallback to Google's DNS for gateway if not dynamically available
        config['dns_spoof'][0]['to_ip'] = f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}" if config['evasion']['dynamic_payload'] else config['targets'][0]['ip']
        
        return config
    except yaml.YAMLError as exc:
        logger.error(f"Error in configuration file: {exc}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to fetch dynamic IP addresses: {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading config: {e}")
    return None
