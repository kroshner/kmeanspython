import sys
from threading import Thread
import Queue
import time
import centroids
import import_data
import distance
import clusters
number_of_centroids = 5
iteration = 0
start_time = time.time()


def main(argv):
    initial_dataset = import_data.get_data()
    processing_dataset = import_data.get_data()

    processing_dataset = centroids.randomize_centroids(processing_dataset, number_of_centroids)

    verification_results = do_clustering(processing_dataset)

    while True:
        if is_clustering_successful(verification_results):
            output_success_rates(processing_dataset, initial_dataset)
            break
        elif is_too_many_attempts():
            print("TOO MANY ATTEMPTS")
            break
        else:
            centroids_ids = list(map(lambda x: x["id"], verification_results))
            processing_dataset = centroids.setup_centroids_new(processing_dataset, verification_results)
            verification_results = do_clustering(processing_dataset)
    print("FINAL, ITERATIONS COUNT: ", iteration)
    print("TIME DURATION %s seconds" % (time.time() - start_time))


def do_clustering(dataset_with_setup):
    global iteration
    iteration += 1
    print("Current iteration: " + str(iteration) + ". PASSED %s seconds" % (time.time() - start_time))
    initial_centroids = centroids.filter_centroids(dataset_with_setup)
    initial_non_centroids = centroids.filter_non_centroids(dataset_with_setup)
    for non_centroid in initial_non_centroids:
        new_current_class = distance.get_closest_to_item_from_objects(non_centroid, initial_centroids)["item"]["current_class"]
        non_centroid["current_class"] = new_current_class
    grouped_clusters = centroids.group_by_class(dataset_with_setup)
    verification_results = []
    for cluster in grouped_clusters:
        verification_results.append(clusters.create_centroid_with_verification(cluster["items"], cluster["grouped_by"]))
    return verification_results


def do_clustering_threaded(dataset_with_setup):
    global iteration
    iteration += 1
    print("Current iteration: " + str(iteration) + ". PASSED %s seconds" % (time.time() - start_time))
    initial_centroids = centroids.filter_centroids(dataset_with_setup)
    initial_non_centroids = centroids.filter_non_centroids(dataset_with_setup)
    for non_centroid in initial_non_centroids:
        new_current_class = distance.get_closest_to_item_from_objects(non_centroid, initial_centroids)["item"]["current_class"]
        non_centroid["current_class"] = new_current_class
    grouped_clusters = centroids.group_by_class(dataset_with_setup)

    queue = Queue.Queue()
    threads_list = []
    for cluster in grouped_clusters:
        t = Thread(
            target=lambda q, arg1, arg2: q.put(clusters.create_centroid_with_verification(arg1, arg2)),
            args=(queue, cluster["items"], cluster["grouped_by"])
        )
        t.start()
    threads_list.append(t)

    for t in threads_list:
        t.join()

    results = []
    while not queue.empty():
        result = queue.get()
        results.append(result)

    return results


def is_clustering_successful(verification_results):
    return len(filter(lambda x: x["was_real_centroid"] is True, verification_results)) == number_of_centroids


def is_too_many_attempts():
    return iteration > 1000


def output_success_rates(results, initial_dataset):
    print("SUCCESS")
    total_items_results_count = len(results)
    total_items_initial_count = len(initial_dataset)
    print("NUMBER OF ITEMS IS " + "EQUAL! THAT'S GOOD" if total_items_initial_count == total_items_results_count else "NOT EQUAL! THAT'S BAD")
    grouped_results = centroids.group_by_class(results)
    grouped_initial_data = centroids.group_by_data_class(initial_dataset)
    for initial_item_group in grouped_initial_data:
        initial_item_group_key = initial_item_group["grouped_by"]
        initial_item_group_count = len(initial_item_group["items"])
        results_item_group = filter(lambda x: x["grouped_by"] == initial_item_group_key, grouped_results)
        results_item_group_count = len((results_item_group[0])["items"]) if any(results_item_group) else 0
        print(str(initial_item_group_count) + " items in ___" + initial_item_group_key + "___ initial cluster, " + str(results_item_group_count) + " in resulting set")


if __name__ == "__main__":
    main(sys.argv)
