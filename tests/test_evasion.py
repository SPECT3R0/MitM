import unittest
from unittest.mock import patch
from evasion.traffic_shaping import shape_traffic
from evasion.encryption_c2 import encrypt_command_control
from evasion.packet_fragmentation import fragment_packet
from evasion.decoy_traffic import generate_decoy
from tests import TestBase
from scapy.all import *

class TestEvasion(TestBase):
    def setUp(self):
        super().setUp()
        self.packet = IP()/TCP()/Raw(load=b"test")

    @patch('time.sleep')
    def test_traffic_shaping(self, mock_sleep):
        shaped_packet = shape_traffic(self.packet, self.config)
        self.assertEqual(shaped_packet.summary(), self.packet.summary(), "Traffic shaping should not corrupt packet")
        mock_sleep.assert_called()

    @patch('scapy.all.send')
    def test_encryption(self, mock_send):
        encrypted_packet = encrypt_command_control(self.packet, self.config)
        self.assertNotEqual(encrypted_packet[TCP].payload.load, self.packet[TCP].payload.load, "Packet should be encrypted")

    @patch('scapy.all.send')
    def test_fragmentation(self, mock_send):
        result = fragment_packet(self.packet, self.config)
        self.assertTrue(result, "Fragmentation should succeed")
        mock_send.assert_called()

    def test_decoy(self):
        generate_decoy(self.config)  # No direct assertion, but ensure no crash
        # You might want to check logs or simulate network impact

if __name__ == '__main__':
    unittest.main()
