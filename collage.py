import os
from itertools import product
from typing import List, Tuple
from urllib.request import urlopen

import pylast
from PIL import Image, ImageFont, ImageDraw
from pylast import Album

IMAGE_EDGE_SIZE = 300
TEXT_BG_BOTTOM_PADDING = 5
FONT_SIZE = 15


def fetch_albums() -> List[Album]:
    network = pylast.LastFMNetwork(
        api_key=os.getenv("LASTFM_API_KEY"), api_secret=os.getenv("LASTFM_API_SECRET")
    )

    items = network.get_user("jpegaga").get_top_albums(pylast.PERIOD_1MONTH, limit=9)
    return [item.item for item in items]


def fetch_cover(album: Album) -> Image.Image:
    return Image.open(urlopen(album.get_cover_image())).convert("RGBA")


def text_overlay(text: str, base_size: Tuple[int, int]) -> Image.Image:
    fnt = ImageFont.truetype(os.getenv("COLLAGE_TTF"), FONT_SIZE)
    height = fnt.getsize_multiline(text)[1] + TEXT_BG_BOTTOM_PADDING

    rect = Image.new("RGBA", base_size, (255, 255, 255, 0))

    draw = ImageDraw.Draw(rect)
    draw.rectangle((0, 0, base_size[0], height), fill=(0, 0, 0, 128))
    draw.text((0, 0), text, font=fnt)

    return rect


def art_with_text(album: Album):
    artist = album.artist.name if album.artist and album.artist.name else ""
    text = f"{album.title or ''}\n{artist}"

    album_img = fetch_cover(album)
    text_img = text_overlay(text, album_img.size)

    return Image.alpha_composite(album_img, text_img)


def generate_collage():
    img = Image.new("RGBA", (3 * IMAGE_EDGE_SIZE, 3 * IMAGE_EDGE_SIZE))

    print("Fetching albums...")
    # place covers in (0, 300), (0, 600), (0, 900), (300, 0) ...
    for album, (x, y) in zip(fetch_albums(), product(range(3), range(3))):
        print(album, x, y)
        album_img = art_with_text(album)
        img.paste(album_img, (x * IMAGE_EDGE_SIZE, y * IMAGE_EDGE_SIZE))

    return img











