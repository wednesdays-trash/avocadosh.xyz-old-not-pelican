import sys

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape

from collage import generate_collage, fetch_albums

load_dotenv()

env = Environment(
    loader=FileSystemLoader("templates"), autoescape=select_autoescape(["html"])
)


if __name__ == "__main__":
    if not "--no-collage" in sys.argv:
        generate_collage(fetch_albums()).save("./static/img/lastfm-collage.jpg", quality=85)

    for template_name in env.list_templates():
        if template_name == "layout.html.jinja2":
            continue

        template = env.get_template(template_name)

        with open(f"static/{template_name.replace('.jinja2', '')}", "w") as f:
            f.write(template.render())
