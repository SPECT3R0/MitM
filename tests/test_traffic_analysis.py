import unittest
from unittest.mock import patch
from modules.traffic_analysis import log_traffic, analyze_traffic, setup_db
from tests import TestBase
import sqlite3

class TestTrafficAnalysis(TestBase):
    def setUp(self):
        super().setUp()
        setup_db()

    @patch('modules.traffic_analysis.conn')
    def test_log_traffic(self, mock_conn):
        packet = IP(src="1.1.1.1", dst="2.2.2.2")/TCP()
        result = log_traffic(packet, self.config)
        self.assertTrue(result, "Traffic logging should succeed")

    def test_analyze_traffic(self):
        # Insert test data
        c = sqlite3.connect('traffic.db').cursor()
        c.execute("INSERT INTO traffic (src, dst, protocol) VALUES ('1.1.1.1', '2.2.2.2', 6)")
        analyze_traffic()

if __name__ == '__main__':
    unittest.main()
