"""
Implementation of the UDP Tracker protocol for BitTorrent

Specifications at https://www.bittorrent.org/beps/bep_0015.html

Author: Simon Bordeyne @Dogeek
Github: https://github.com/Dogeek
"""

import socket
from urllib.parse import urlparse
import random
import time

from torrent.utils import get_logger

def retry(func):
    start_time = time.time()
    n = 0
    while n < 9:
        if (time.time() - start_time) > 15 * 2**n:
            start_time = time.time()
            n += 1
            yield func


class UDPTracker:
    def __init__(self, address):
        self.logger = get_logger('torrent.trackers.udp.' + str(id(self)))
        parsed_address = urlparse(address)
        self.address, self.port = parsed_address.netloc.split(':')
        self.port = int(self.port)
        self.socket = socket.socket(
            socket.AddressFamily.AF_INET, # IPv4 protocol
            socket.SocketKind.SOCK_DGRAM,  # UDP protocol
        )
        self._transaction_id = None
        self._protocol_id = 0x41727101980.to_bytes(64, 'big')
        self.logger.info(f'Instanciated class UDPTracker on {address}')


    @property
    def transaction_id(self):
        if self._transaction_id is None:
            self._transaction_id = random.randint(0, 2_147_483_647) # Random Int32
        return self._transaction_id

    def __enter__(self):
        self.socket.connect((self.address, self.port))
        self.logger.info('Connected to socket...')
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.logger.info('Closing socket...')
        self.socket.close()

    def _header(self):
        self.logger.info('Sending header')
        header = self._protocol_id + \
                 0x0.to_bytes(32, 'big') + \
                 self.transaction_id.to_bytes(32, 'big')
        self.logger.info(f'Header created : {header}')
        assert len(header) // 8 == 16, "Header is not 16 bytes long"
        self.socket.send(header)
        self.logger.info('Header sent.')
        response = self.socket.recv(128)
        self.logger.info(f'Response received: {response}')
