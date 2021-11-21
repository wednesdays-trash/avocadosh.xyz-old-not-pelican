import os
from itertools import product
from typing import List
from urllib.request import urlopen

import pylast
from PIL import Image, ImageDraw, ImageFont
from pylast import Album

IMAGE_EDGE_SIZE = 300
TEXT_BG_BOTTOM_PADDING = 5
FONT_SIZE = 15


def fetch_albums() -> List[Album]:
    """
    Fetch my 9 most listened albums from the past month
    Expects LASTFM_API_KEY and LASTFM_API_SECRET env vars
    """
    api_key = os.getenv("LASTFM_API_KEY")
    api_secret = os.getenv("LASTFM_API_SECRET")
    network = pylast.LastFMNetwork(api_key, api_secret)
    # despite only needing 9 albums for the collage, we'll fetch a bit more so we can discard
    # albums with no album art and just draw the next album instead
    items = network.get_user("jpegaga").get_top_albums(pylast.PERIOD_1MONTH, limit=15)

    # yield all items with a non-None album art
    for item in items:
        if item.item.info["image"][0] is None:
            continue
        yield item.item


def fetch_cover(album: Album) -> Image.Image:
    "Download the album's cover image and return a Pillow Image of it"
    return Image.open(urlopen(album.get_cover_image())).convert("RGBA")


def overlay_text(album: Album) -> str:
    "Returns the string to be written on the album overlay"
    artist = album.artist.name if album.artist and album.artist.name else ""
    return f"{album.title or ''}\n{artist}"


def overlay(text: str) -> Image.Image:
    """
    An image of some text in a cool font on top of a black rectangle stretching across the whole
    image horizontally
    Font location should be defined via COLLAGE_TTF env var
    """
    fnt = ImageFont.truetype(os.getenv("COLLAGE_TTF"), FONT_SIZE)
    height = fnt.getsize_multiline(text)[1] + TEXT_BG_BOTTOM_PADDING

    rect = Image.new("RGBA", (IMAGE_EDGE_SIZE, IMAGE_EDGE_SIZE), (255, 255, 255, 0))

    draw = ImageDraw.Draw(rect)
    draw.rectangle((0, 0, IMAGE_EDGE_SIZE, height), fill=(0, 0, 0, 180))
    draw.text((0, 0), text, font=fnt)

    return rect


def generate_collage():
    result_img = Image.new("RGBA", (3 * IMAGE_EDGE_SIZE, 3 * IMAGE_EDGE_SIZE))

    print("Fetching albums...")

    # place covers in (0, 300), (0, 600), (0, 900), (300, 0) ...
    for album, (x, y) in zip(fetch_albums(), product(range(3), range(3))):
        print(album)

        base_cover = fetch_cover(album)
        album_label = overlay_text(album)
        img = Image.alpha_composite(base_cover, overlay(album_label))

        result_img.paste(img, (x * IMAGE_EDGE_SIZE, y * IMAGE_EDGE_SIZE))

    # from dust we came and to dust we will return
    return result_img.convert("RGB")
