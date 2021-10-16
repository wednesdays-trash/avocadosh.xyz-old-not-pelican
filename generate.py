import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("templates"), autoescape=select_autoescape(["html"])
)


def lastfm_collage():
    return requests.get(
        # https://lastfm-collage.herokuapp.com/collage?username=jpegaga&method=album&period=1month&column=3&row=3&caption=true&scrobble=false
        "https://lastfm-collage.herokuapp.com/collage",
        params=dict(
            username="jpegaga",
            method="album",
            period="1month",
            column="3",
            row="3",
            caption="true",
            scrobble="false"
        ),
    ).content

for template_name in env.list_templates():
    template = env.get_template(template_name)

    with open(f"static/{template_name}", "w") as f:
        f.write(template.render(person="xd"))


with open("./static/img/lastfm-collage.jpg", "wb") as f:
    f.write(lastfm_collage())
