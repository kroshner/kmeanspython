import math


def get_closest_to_item_from_objects(item, objects):
    distances = []
    for object_item in objects:
        distances.append({
            "distance": calculate_euclidean_distance(item["data"], object_item["data"]),
            "item": object_item
        })
    sorted_items = sorted(distances, key=lambda x: x["distance"])
    return sorted_items[0]


def calculate_euclidean_distance(object1, object2):
    accumulator = 0.0
    for x in range(2, 18):
        accumulator += math.pow(float(object2[x]) - float(object1[x]), 2)
    return math.sqrt(accumulator)


def calculate_euclidean_center(class_name, objects):
    new_centroid = {
        "is_centroid": True,
        "current_class": class_name,
        "data": list(["", "", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, ""])
    }
    for item in objects:
        for x in range(2, 18):
            new_centroid["data"][x] += float(item["data"][x])
    for x in range(2, 18):
        new_centroid["data"][x] /= len(objects)
    return new_centroid
