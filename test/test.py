import random
from string import ascii_lowercase

from PIL import Image

from collage import Album, generate_collage


def random_string() -> str:
    letters = random.choices(ascii_lowercase + " ", k=random.randint(5, 50))
    return "".join(letters).strip()


art = Image.open("test/sample-art.jpg").convert("RGBA")

generate_collage(
    Album(title=random_string(), artist=random_string(), cover_art=art)
    for _ in range(9)
).save("./test/output.webp", quality=40)
