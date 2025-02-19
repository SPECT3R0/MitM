import unittest
from unittest.mock import patch, MagicMock
from modules.http_injection import inject_content, start_injection
from tests import TestBase
from scapy.all import *

class TestHTTPInjection(TestBase):
    @patch('scapy.all.send')
    def test_inject_content(self, mock_send):
        packet = IP()/TCP(dport=80)/Raw(load="HTTP/1.1 200 OK\r\n\r\n<html><body></body></html>")
        result = inject_content(packet, self.config)
        mock_send.assert_called()
        self.assertTrue(result, "HTTP injection should modify content")

    @patch('scapy.all.sniff')
    def test_start_injection(self, mock_sniff):
        start_injection(self.config)
        mock_sniff.assert_called_with(prn=ANY, iface=self.config['interface'], store=0)

if __name__ == '__main__':
    unittest.main()
