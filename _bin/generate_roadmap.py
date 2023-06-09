import os
import csv
import jinja2

def setup_jinja():
    # register templates
    multi_loader = jinja2.ChoiceLoader([
        jinja2.FileSystemLoader(searchpath=["./_bin/templates"]),
        jinja2.PrefixLoader({
            'govuk_frontend_jinja': jinja2.PackageLoader('govuk_frontend_jinja'),
            'digital-land-frontend': jinja2.PackageLoader('digital_land_frontend')
        })
    ])
    env = jinja2.Environment(loader=multi_loader)

    # set variables to make available to all templates
    env.globals["assetPath"] = "https://digital-land.github.io/"
    env.globals["baseurl"] = "/data-standards"

    return env

def render(path, template, **kwargs):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, "w") as f:
        f.write(template.render(**kwargs))


def make_id(name):
    return name.lower().replace(' ', '-')


def get_planning_concerns():
    planning_concerns = {}

    # Open the CSV file
    with open('_data/planning-concerns-backlog.csv', 'r') as file:
        reader = csv.DictReader(file)
        
        # Iterate over each row in the CSV
        for row in reader:
            # Access the values in each column using the dictionary keys
            # Create a Python dictionary for each row
            entry = dict(row)
            status = entry['Status']

            planning_concerns.setdefault(status, []).append(entry)


    return planning_concerns


def generate_roadmap():
    env = setup_jinja()
    concerns = get_planning_concerns()
    template = env.get_template("roadmap.html")

    render("./what-we-are-working-on/index.html", template, concerns=concerns)

generate_roadmap()
