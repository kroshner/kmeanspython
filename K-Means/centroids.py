from itertools import groupby
from random import randint
import copy


def filter_centroids(objects):
    return filter(lambda x: x["is_centroid"] is True, objects)


def filter_non_centroids(objects):
    return filter(lambda x: x["is_centroid"] is False, objects)


def group_by_class(objects):
    result = []
    sorted_objects = sorted(objects, key=lambda x: x["current_class"])
    for k, g in groupby(sorted_objects, lambda x: x["current_class"]):
        result.append({
            "grouped_by": k,
            "items": list(g)
        })
    print("group_by_class method: len is:" + str(len(result)))
    for item in result:
        print("grouped_by_key: " + item["grouped_by"] + ". count: " + str(len(item["items"])))
    return result


def group_by_data_class(objects):
    result = []
    sorted_objects = sorted(objects, key=lambda x: x["data"][18])
    for k, g in groupby(sorted_objects, lambda x: x["data"][18]):
        result.append({
            "grouped_by": k,
            "items": list(g)
        })
    return result


def randomize_centroids(objects, number_of_centroids):
    random_centroids_indexes = _get_array_random_centroids_indexes(objects, number_of_centroids)
    return _mark_items_as_centroids(objects, random_centroids_indexes)


def setup_centroids(objects, ids):
    # result = copy.deepcopy(objects)
    result = _reinit_objects(objects)
    filtered_items = filter(lambda x: x["data"][19] in ids, result)
    map(_map_item_via_id, filtered_items)
    return result


def setup_centroids_new(objects, verification_results):
    # result = copy.deepcopy(objects)
    objects = _reinit_objects(objects)
    for verification_result in verification_results:
        centroid_id = verification_result["id"]
        cluster_class_name = verification_result["real_cluster_class_name"]
        centroid = filter(lambda x: x["data"][19] == centroid_id, objects)
        if len(centroid) == 1:
            _map_item_via_id(centroid[0], cluster_class_name)
        else:
            print("BULLSHIT")
    return objects


def _reinit_objects(objects):
    for item in objects:
        item["current_class"] = None
        item["is_centroid"] = False
    return objects


def _get_array_random_centroids_indexes(objects, number_of_centroids):
    centroids_indexes = []
    centroids_cluster_keys = []
    for i in range(0, number_of_centroids, 1):
        current_array_random_index = _get_array_random_index(objects)
        current_array_random_cluster_key = objects[current_array_random_index]["data"][18]
        while (current_array_random_index in centroids_indexes) or (current_array_random_cluster_key in centroids_cluster_keys):
            current_array_random_index = _get_array_random_index(objects)
            current_array_random_cluster_key = objects[current_array_random_index]["data"][18]
        centroids_indexes.append(current_array_random_index)
        centroids_cluster_keys.append(current_array_random_cluster_key)
    return centroids_indexes


def _get_array_random_index(objects):
    array_first_index = 0
    array_last_index = len(objects) - 1
    array_random_index = randint(array_first_index, array_last_index)
    return array_random_index


def _mark_items_as_centroids(objects, centroids_indexes):
    for index in centroids_indexes:
        objects[index]["is_centroid"] = True
        objects[index]["current_class"] = objects[index]["data"][18]
    return objects


def _map_item_via_id(item, cluster_class):
    item["is_centroid"] = True
    item["current_class"] = cluster_class
    return item
