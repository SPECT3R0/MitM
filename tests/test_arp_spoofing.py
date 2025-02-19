import unittest
from unittest.mock import patch, MagicMock
from modules.arp_spoofing import arp_spoof, start_spoofing, stop_spoofing
from tests import TestBase
from scapy.all import *

class TestARPSpoofing(TestBase):
    @patch('scapy.all.send')
    def test_arp_spoof(self, mock_send):
        # Mock send to avoid actual network interaction
        result = arp_spoof(self.target_ip, self.gateway_ip, self.config['interface'])
        mock_send.assert_called()
        self.assertTrue(result, "ARP spoof should return True on success")

    @patch('modules.arp_spoofing.arp_spoof')
    def test_start_spoofing(self, mock_arp_spoof):
        mock_arp_spoof.return_value = True
        result = start_spoofing(self.config)
        self.assertTrue(result, "start_spoofing should succeed with valid config")

    @patch('scapy.all.send')
    def test_stop_spoofing(self, mock_send):
        result = stop_spoofing(self.config)
        mock_send.assert_called()
        self.assertTrue(result, "stop_spoofing should return True")

if __name__ == '__main__':
    unittest.main()
