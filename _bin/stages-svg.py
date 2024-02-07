from lxml import etree
from datetime import datetime

from planningconsiderations import breakdown_by_stage


class SVG:
    def __init__(self, filename):
        self.original_filename = filename
        self.load()

    def load(self):
        # self.tree = etree.parse(self.original_filename)
        # self.root = self.tree.getroot()
        with open(self.original_filename) as fid:
            self.svg_file = etree.parse(fid, parser=etree.XMLParser(huge_tree=True))
        self.root = self.svg_file.getroot()

    def save(self, filename):
        self.tree = etree.ElementTree(self.root)
        self.tree.write(filename, pretty_print=True)


def get_element_by_id(element, id):
    return element.xpath(f".//*[@id='{id}']")[0]


def find_elements_by_class(element, class_name):
    # to limit search to current element need to put '.' at beginning
    return element.xpath(
        f".//*[contains(concat(' ', normalize-space(@class), ' '), '{class_name}')]"
    )


# config
svg_file_path = "assets/images/latest-stage-count-diagram.svg"
max_bar_height = 460
y_start = 174
label_y_offset = 36
label_font_size = 36
min_bar_height = 48
distributable_space = max_bar_height - min_bar_height
stages = [
    "screening",
    "researching",
    "codesigning",
    "test-and-iterate",
    "go-no-go",
    "prepared-for-platform",
    "on-the-platform",
    "archived",
]
stage_grid_mapping = {
    "Backlog": "backlog",
    "Screen": "screening",
    "Research": "researching",
    "Co-design": "codesigning",
    "Test and iterate": "test-and-iterate",
    "Ready for go/no-go": "go-no-go",
    "Prepared for platform": "prepared-for-platform",
    "On the platform": "on-the-platform",
    "Archived": "archived",
}


def calc_y_pos(height):
    offset = max_bar_height - height
    return y_start + offset


def set_bar_height(bar, height):
    set_attribute(bar, "height", str(height))
    offset = max_bar_height - height
    y_pos = y_start + offset
    set_attribute(bar, "y", str(y_pos))


def position_label(label, bar_y_pos):
    y_pos = label_y_offset + bar_y_pos
    set_attribute(label, "y", str(y_pos))


def set_attribute(element, attr, value):
    element.set(attr, value)


def get_bar_and_label(stage_element):
    bars = find_elements_by_class(stage_element, "bar")
    bar = bars[0]
    label = find_elements_by_class(stage_element, "label")[0]

    return bar, label


def update_stage(svg, stage, max_count, min_height=min_bar_height):
    stage_element = get_element_by_id(svg.root, stage[0])
    bar, label = get_bar_and_label(stage_element)

    bar_part_height = distributable_space / (max_count - 1)

    if stage[1] == 0:
        bar_height = 5
        bar_y_pos = calc_y_pos(min_height)
        set_attribute(label, "class", "st6 st4 st9 label")
    else:
        bar_height = min_height
        if stage[1] > 1:
            bar_height = round(((stage[1] - 1) * bar_part_height) + min_height)
        bar_y_pos = calc_y_pos(bar_height)

    set_bar_height(bar, bar_height)
    position_label(label, bar_y_pos)
    label.text = str(stage[1])


def get_stage_counts():
    count_dict = breakdown_by_stage()
    counts = {}
    for name in stage_grid_mapping:
        counts[stage_grid_mapping[name]] = 0
        if name in count_dict.keys():
            counts[stage_grid_mapping[name]] = len(count_dict[name])
    return counts


def generate_svg():
    svg = SVG(svg_file_path)

    stage_counts = get_stage_counts()

    # update backlog
    backlog_element = get_element_by_id(svg.root, "backlog")
    bar, label = get_bar_and_label(backlog_element)
    label.text = str(stage_counts["backlog"])
    del stage_counts["backlog"]

    max_count = max(stage_counts.values())

    for stage in stages:
        update_stage(svg, (stage, stage_counts[stage]), max_count)

    today = datetime.today().strftime("%Y-%m-%d")
    svg.save(f"assets/images/stage-counts/{today}.svg")


if __name__ == "__main__":
    generate_svg()
