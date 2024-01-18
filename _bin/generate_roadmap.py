import os
import csv
import jinja2
import frontmatter
import json
import jsonpickle

from operator import itemgetter
from jinja_filters import slugify_filter
from utils import pythonic_keys
from planningconsiderations import get_planning_considerations
from pathlib import Path


def debug_filter(thing):
    return f"<script>console.log({json.dumps(json.loads(jsonpickle.encode(thing)), indent=2)});</script>"


def markdown_filter(text):
    from markdown import markdown

    if text is not None and isinstance(text, str):
        return markdown(text)


def setup_jinja():
    # register templates
    multi_loader = jinja2.ChoiceLoader(
        [
            jinja2.FileSystemLoader(searchpath=["./_bin/templates"]),
            jinja2.PrefixLoader(
                {
                    "govuk_frontend_jinja": jinja2.PackageLoader(
                        "govuk_frontend_jinja"
                    ),
                    "digital-land-frontend": jinja2.PackageLoader(
                        "digital_land_frontend"
                    ),
                }
            ),
        ]
    )
    env = jinja2.Environment(loader=multi_loader)

    # set variables to make available to all templates
    env.globals["baseurl"] = "/data-standards"
    env.globals["assetPath"] = env.globals["baseurl"] + "/assets"
    env.globals[
        "issuesURL"
    ] = "https://github.com/digital-land/data-standards-backlog/issues/"
    env.globals[
        "discussionsURL"
    ] = "https://github.com/digital-land/data-standards-backlog/discussions/"
    env.filters["slugify"] = slugify_filter
    env.filters["markdown_filter"] = markdown_filter
    env.filters["debug"] = debug_filter

    return env


def render(path, template, **kwargs):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, "w") as f:
        f.write(template.render(**kwargs))


def make_id(name):
    return name.lower().replace(" ", "-")


def generate_roadmap():
    env = setup_jinja()
    concerns = get_planning_considerations()
    count = sum([len(concerns[bucket]) for bucket in concerns.keys()])
    all_concerns = sorted(
        [concern for bucket in concerns.keys() for concern in concerns[bucket]],
        key=itemgetter("Concern"),
    )

    current_work_template = env.get_template("what-we-are-working-on.html")
    backlog_template = env.get_template("backlog.html")
    planning_consideration_template = env.get_template("planning-consideration.html")

    render(
        "./what-we-are-working-on/index.html", current_work_template, concerns=concerns
    )
    render(
        "./what-we-are-working-on/planning-consideration/index.html",
        backlog_template,
        concerns=all_concerns,
        count=count,
    )
    parent_dir = Path(__file__).parent.parent
    planning_considerations = Path(parent_dir, "planning-considerations")
    for concern in all_concerns:
        concern = pythonic_keys(concern)
        slug = slugify_filter(concern["concern"])
        markdown_file = Path(planning_considerations, f"{slug}.md")

        if markdown_file.exists():
            with open(markdown_file, "r") as f:
                concern_markdown = frontmatter.load(f)
                concern["markdown"] = concern_markdown.content
                concern.update(concern_markdown.metadata)

        render(
            f"./what-we-are-working-on/planning-consideration/{slug}/index.html",
            planning_consideration_template,
            consideration=concern,
        )


generate_roadmap()
