from Maga import Maga

import libtorrent
import logging
import os
import time


logging.basicConfig(level=logging.INFO)


def magnet_to_torrent(magnet_uri, dst):
    params = libtorrent.parse_magnet_uri(magnet_uri)

    session = libtorrent.session({'dht_announce_interval': 3})
    handle = session.add_torrent(params)
    info = handle.status()
    counter = time.time()
    print("Trying magnet link: '" + magnet_uri + "'...")
    while not handle.has_metadata():
        info = handle.status()

        if info.num_peers > 0:
            counter = time.time()

        temp = time.time()
        print("\rRemaining time: '{}|60' /=/ Number of peers: {}".format(int(temp - counter), str(info.num_peers)), end="")
        time.sleep(0.01)
        if temp - counter >= 60 and info.num_peers == 0:
            print("\nCouldn't find peers for '" + magnet_uri + "' after " + str(int(temp - counter)) + " seconds.")
            return

    torrent_info = handle.get_torrent_info()
    torrent_file = libtorrent.create_torrent(torrent_info)
    torrent_path = os.path.join(dst, torrent_info.name() + ".torrent")
    with open(torrent_path, "wb") as f:
        f.write(libtorrent.bencode(torrent_file.generate()))
    print("\nTorrent saved to %s" % torrent_path)
    return


class Crawler(Maga):
    async def handle_get_peers(self, infohash, addr):
        magnet_to_torrent('magnet:?xt=urn:btih:' + infohash.rstrip(), "./torrents/")

    async def handle_announce_peer(self, infohash, addr, peer_addr):
        magnet_to_torrent('magnet:?xt=urn:btih:' + infohash.rstrip(), "./torrents/")


crawler = Crawler()
crawler.run(6881)
