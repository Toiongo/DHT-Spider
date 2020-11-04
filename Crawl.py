from Maga import Maga

import libtorrent
import logging
import os
import time


logging.basicConfig(level=logging.INFO)


def main():
    class Crawler(Maga):
        async def magnet_to_torrent(self, magnet_uri, dst):
            params = libtorrent.parse_magnet_uri(magnet_uri)

            session = libtorrent.session({'dht_announce_interval': 3})
            handle = session.add_torrent(params)
            info = handle.status()
            counter = time.time()
            print("Trying magnet link: '" + magnet_uri + "'...")
            while not handle.has_metadata():
                info = handle.status()
                temp = time.time()

                # You can adjust the time program waits to get a torrent file, just change 60 to amount of seconds of your choice.
                # You might also want to remove the peer condition below, to speed things up.
                if temp - counter >= 60 and info.num_peers == 0:
                    print("Couldn't download torrent from link '" + magnet_uri + "' after " + str(int(temp - counter)) + " seconds.\n")
                    return

            torrent_info = handle.get_torrent_info()
            torrent_file = libtorrent.create_torrent(torrent_info)
            torrent_path = os.path.join(dst, ''.join(e for e in torrent_info.name() if e.isalnum() or e in "[] ") + ".torrent")
            torrent_path = str(torrent_path).encode('utf-8').decode()
            with open(torrent_path, "wb") as f:
                f.write(libtorrent.bencode(torrent_file.generate()))
            print("Torrent saved to %s \n" % torrent_path)
            return

        async def handle_get_peers(self, infohash, addr):
            # You might just want to return on this function to save time from potentially dead links
            await self.magnet_to_torrent('magnet:?xt=urn:btih:' + infohash.rstrip(), "./torrents/")

        async def handle_announce_peer(self, infohash, addr, peer_addr):
            await self.magnet_to_torrent('magnet:?xt=urn:btih:' + infohash.rstrip(), "./torrents/")

    try:
        crawler = Crawler()
        crawler.run(6881)
    except KeyboardInterrupt as e:
        crawler.stop()
        sys.exit()

if __name__ == "__main__":
    main()
