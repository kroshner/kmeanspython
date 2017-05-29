import distance


def create_centroid_with_verification(objects, grouped_by):
    euclidean_center = distance.calculate_euclidean_center(grouped_by, objects)
    item = distance.get_closest_to_item_from_objects(euclidean_center, objects)["item"]
    return {
        "centroid": item,
        "was_real_centroid": item["is_centroid"] is True,
        "id": item["data"][19],
        "real_cluster_class_name": grouped_by
    }
