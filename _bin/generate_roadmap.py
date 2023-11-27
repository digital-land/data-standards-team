import os
import csv
import jinja2

from operator import itemgetter
from jinja_filters import slugify_filter
from utils import pythonic_keys


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

    return env


def render(path, template, **kwargs):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, "w") as f:
        f.write(template.render(**kwargs))


def make_id(name):
    return name.lower().replace(" ", "-")


def get_planning_concerns():
    planning_concerns = {}

    # Open the CSV file
    with open("_data/planning-concerns-backlog.csv", "r") as file:
        reader = csv.DictReader(file)

        # Iterate over each row in the CSV
        for row in reader:
            # Access the values in each column using the dictionary keys
            # Create a Python dictionary for each row
            entry = dict(row)
            status = entry["Status"]

            planning_concerns.setdefault(status, []).append(entry)

    return planning_concerns


def generate_roadmap():
    env = setup_jinja()
    concerns = get_planning_concerns()
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
    for concern in all_concerns:
        concern = pythonic_keys(concern)
        render(
            f"./what-we-are-working-on/planning-consideration/{slugify_filter(concern['concern'])}/index.html",
            planning_consideration_template,
            consideration=concern,
        )


generate_roadmap()
