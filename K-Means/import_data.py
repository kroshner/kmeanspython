import csv


# user;gender;age;how_tall_in_meters;weight;body_mass_index;x1;y1;z1;x2;y2;z2;x3;y3;z3;x4;y4;z4;class
def get_data():
    with open('./data/dataset-har-PUC-Rio-ugulino.csv', 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        iris_data = map(_map_iris_item, list(reader))
        return iris_data


def _map_iris_item(item):
    return {
        "is_centroid": False,
        "current_class": None,
        "data": item
    }
