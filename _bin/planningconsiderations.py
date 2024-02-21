import csv
from operator import itemgetter


# returns considerations grouped by status
def get_planning_considerations():
    planning_considerations = {}

    # Open the CSV file
    with open("_data/planning-concerns-backlog.csv", "r") as file:
        reader = csv.DictReader(file)

        # Iterate over each row in the CSV
        for row in reader:
            # Access the values in each column using the dictionary keys
            # Create a Python dictionary for each row
            entry = dict(row)
            status = entry["Stage"]

            if entry["Concern"] != "":
                planning_considerations.setdefault(status, []).append(entry)

    return planning_considerations


def breakdown_by_stage():
    considerations = get_planning_considerations()
    all_considerations = sorted(
        [
            concern
            for bucket in considerations.keys()
            for concern in considerations[bucket]
        ],
        key=itemgetter("Concern"),
    )
    stages = {}
    for c in all_considerations:
        stage = c["Stage"]
        stages.setdefault(stage, []).append(c)

    return stages


def print_stage_count():
    stages = breakdown_by_stage()
    for s in stages.keys():
        print(s, ": ", len(stages[s]))


if __name__ == "__main__":
    print_stage_count()
