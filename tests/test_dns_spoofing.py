import unittest
from unittest.mock import patch, MagicMock
from modules.dns_spoofing import dns_spoof, run_dns_server
from tests import TestBase
from scapy.all import *

class TestDNSSpoofing(TestBase):
    @patch('scapy.all.send')
    def test_dns_spoof(self, mock_send):
        packet = IP()/UDP(sport=1024, dport=53)/DNS(qr=0, qd=DNSQR(qname="example.com"))
        result = dns_spoof(packet, self.config)
        mock_send.assert_called()
        self.assertTrue(result, "DNS spoof should redirect example.com")

    @patch('scapy.all.sniff')
    def test_run_dns_server(self, mock_sniff):
        run_dns_server(self.config)
        mock_sniff.assert_called_with(filter="udp port 53", prn=ANY, iface=self.config['interface'], store=0)

if __name__ == '__main__':
    unittest.main()
