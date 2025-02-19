import unittest
from unittest.mock import patch, MagicMock
from modules.core import handle_packet, start_sniffer
from tests import TestBase

class TestCore(TestBase):
    @patch('modules.core.handle_packet')
    def test_start_sniffer(self, mock_handle):
        mock_handle.return_value = True
        result = start_sniffer(self.config, [lambda x, y: True])
        self.assertIsNone(result, "start_sniffer should not return anything")

    @patch('evasion.traffic_shaping.shape_traffic')
    @patch('evasion.encryption_c2.encrypt_command_control')
    @patch('evasion.packet_fragmentation.fragment_packet')
    @patch('evasion.decoy_traffic.generate_decoy')
    def test_handle_packet(self, mock_decoy, mock_fragment, mock_encrypt, mock_shape):
        mock_shape.return_value = MagicMock()
        mock_encrypt.return_value = MagicMock()
        mock_fragment.return_value = False
        mock_decoy.return_value = None

        result = handle_packet(MagicMock(), self.config, [lambda x, y: False])
        self.assertFalse(result, "Handle packet should return False if no handler processes it")

if __name__ == '__main__':
    unittest.main()
