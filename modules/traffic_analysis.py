from scapy.all import *
import sqlite3
import logging

logger = logging.getLogger(__name__)

conn = sqlite3.connect('traffic.db')
c = conn.cursor()

async def log_traffic(packet, config):
    if packet.haslayer(IP):
        try:
            c.execute("INSERT INTO traffic (src, dst, protocol) VALUES (?, ?, ?)", 
                      (packet[IP].src, packet[IP].dst, packet[IP].proto))
            conn.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
    return False

def analyze_traffic():
    try:
        c.execute("SELECT src, COUNT(*) FROM traffic GROUP BY src")
        for row in c.fetchall():
            logger.info(f"IP {row[0]} sent {row[1]} packets")
    except sqlite3.Error as e:
        logger.error(f"Error analyzing traffic: {e}")

def setup_db():
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS traffic 
                     (id INTEGER PRIMARY KEY, src TEXT, dst TEXT, protocol INTEGER)''')
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Database setup failed: {e}")

setup_db()
