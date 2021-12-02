import os
from itertools import product
from typing import Iterable, List
from urllib.request import urlopen
from dataclasses import dataclass

import pylast
from PIL import Image, ImageDraw, ImageFont

IMAGE_EDGE_SIZE = 300
TEXT_BG_BOTTOM_PADDING = 5
FONT_SIZE = 15


@dataclass
class Album:
    title: str
    artist: str
    cover_art: Image.Image


def fetch_albums() -> List[Album]:
    """
    Fetch my 9 most listened albums from the past month
    Expects LASTFM_API_KEY and LASTFM_API_SECRET env vars

    This is the module's interface with the outer world; the rest of it is free of side effects
    """
    api_key = os.getenv("LASTFM_API_KEY")
    api_secret = os.getenv("LASTFM_API_SECRET")
    network = pylast.LastFMNetwork(api_key, api_secret)
    # despite only needing 9 albums for the collage, we'll fetch a bit more so we can discard
    # albums with no album art and just draw the next album instead
    items = network.get_user("jpegaga").get_top_albums(pylast.PERIOD_1MONTH, limit=15)

    # yield all items with a non-None album art
    for item in items:
        alb: pylast.Album = item.item

        print(f'Fetching "{alb.title}" by {alb.artist}')

        if (
            alb.info["image"][0] is None
            or alb.artist is None
            or alb.artist.name is None
            or alb.title is None
        ):
            continue

        yield Album(
            title=alb.title,
            artist=alb.artist.name,
            cover_art=Image.open(urlopen(alb.get_cover_image())).convert("RGBA"),
        )


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


def generate_collage(albums: Iterable[Album]):
    result_img = Image.new("RGBA", (3 * IMAGE_EDGE_SIZE, 3 * IMAGE_EDGE_SIZE))

    print("Fetching albums...")

    # place covers in (0, 300), (0, 600), (0, 900), (300, 0) ...
    for album, (x, y) in zip(albums, product(range(3), range(3))):
        base_cover = album.cover_art
        label = f"{album.title}\n{album.artist}"
        img = Image.alpha_composite(base_cover, overlay(label))

        result_img.paste(img, (x * IMAGE_EDGE_SIZE, y * IMAGE_EDGE_SIZE))

    # from dust we came and to dust we will return
    return result_img.convert("RGB")
