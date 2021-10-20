import os
from typing import List
from urllib.request import urlopen
from itertools import product

import pylast
from PIL import Image
from pylast import Album

IMAGE_EDGE_SIZE = 300


def fetch_albums() -> List[Album]:
    network = pylast.LastFMNetwork(
        api_key=os.getenv("LASTFM_API_KEY"), api_secret=os.getenv("LASTFM_API_SECRET")
    )

    items = network.get_user("jpegaga").get_top_albums(pylast.PERIOD_1MONTH, limit=9)
    return [item.item for item in items]


def generate_collage():
    img = Image.new("RGB", (3 * IMAGE_EDGE_SIZE, 3 * IMAGE_EDGE_SIZE))

    for album, (x, y) in zip(fetch_albums(), product(range(3), range(3))):
        album_img = Image.open(urlopen(album.get_cover_image()))
        img.paste(album_img, (x * IMAGE_EDGE_SIZE, y * IMAGE_EDGE_SIZE))

    return img
