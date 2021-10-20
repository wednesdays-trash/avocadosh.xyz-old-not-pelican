from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape

from collage import generate_collage

load_dotenv()

env = Environment(
    loader=FileSystemLoader("templates"), autoescape=select_autoescape(["html"])
)


if __name__ == "__main__":
    generate_collage().save("./static/img/lastfm-collage.png")

    for template_name in env.list_templates():
        template = env.get_template(template_name)

        with open(f"static/{template_name}", "w") as f:
            f.write(template.render())
