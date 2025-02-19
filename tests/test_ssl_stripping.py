import unittest
from unittest.mock import patch, MagicMock
from modules.ssl_stripping import ssl_strip, start_stripping
from tests import TestBase
from scapy.all import *

class TestSSLStripping(TestBase):
    @patch('scapy.all.send')
    def test_ssl_strip(self, mock_send):
        packet = IP()/TCP(dport=443)/Raw(load="GET / HTTP/1.1")
        result = ssl_strip(packet, self.config)
        mock_send.assert_called()
        self.assertTrue(result, "SSL strip should downgrade HTTPS to HTTP")

    @patch('scapy.all.sniff')
    def test_start_stripping(self, mock_sniff):
        start_stripping(self.config)
        mock_sniff.assert_called_with(filter="tcp port 443", prn=ANY, iface=self.config['interface'], store=0)

if __name__ == '__main__':
    unittest.main()
