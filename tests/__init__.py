import logging
import unittest
from config import load_config
import subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='tests.log')
logger = logging.getLogger(__name__)

class TestBase(unittest.TestCase):
    def setUp(self):
        self.config = load_config() or {}
        if not self.config:
            logger.error("Failed to load configuration for tests.")
            self.skipTest("Configuration loading failed.")
        
        # Dynamically fetch IPs
        try:
            self.target_ip = subprocess.check_output(['dig', '+short', 'myip.opendns.com', '@resolver1.opendns.com']).decode().strip()
            self.gateway_ip = subprocess.check_output(['ip', 'route', 'show', 'default', '|', 'awk', "'{print $3}'"]).decode().strip() or '8.8.8.8'  # Fallback to Google's DNS
            self.spoof_ip = f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
            self.config['targets'] = [{'ip': self.target_ip, 'gateway': self.gateway_ip}]
            self.config['dns_spoof'] = [{'domain': 'example.com', 'to_ip': self.spoof_ip}]
            self.config['interface'] = self.config.get('interface', 'eth0')
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to fetch dynamic IPs: {e}")
            self.skipTest("Dynamic IP fetching failed.")

    def tearDown(self):
        logger.info(f"Completed tests for {self.__class__.__name__}")
