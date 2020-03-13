from torrent.trackers.udp import UDPTracker

with UDPTracker("udp://tracker.leechers-paradise.org:6969") as tracker:
    tracker._header()
