#! /bin/env python3
import numpy as np
import sys
import geojson as gj


def feature_collection_by_fname(ref):
    return dict((feat["properties"]["filename"], feat) for feat in ref.features)


def merge_jsons(reference, clusters):
    result = gj.FeatureCollection([])
    ref_features_by_fname = feature_collection_by_fname(reference)
    ref_features_fname_set = set(ref_features_by_fname.keys())

    for i, cluster in enumerate(clusters):
        # Find the common image in the GeoJSONs
        cluster_feats_by_fname = feature_collection_by_fname(cluster)
        img_names = set(feat["properties"]["filename"] for feat in cluster.features)
        common_fname = list(img_names & set(ref_features_fname_set))[0]
        print(common_fname)
        ref = ref_features_by_fname[common_fname]

        # compute the delta coordinates
        cluster_image = cluster_feats_by_fname[common_fname]
        ref_vec = np.array(ref["geometry"]["coordinates"])
        cluster_vec = np.array(cluster_image["geometry"]["coordinates"])
        delta_vec = ref_vec - cluster_vec
        print(f"ref: {ref_vec}\noff:{cluster_vec}")
        print(f"Relative offset for Cluster #{i}: {delta_vec}")

        # Apply the delta_vec to all the features

        for feature in cluster.features:
            new_pos = list(np.array(feature["geometry"]["coordinates"]) - delta_vec)
            point = gj.Point(new_pos)
            feat = gj.Feature(geometry=point, properties=feature["properties"])
            result.features.append(feat)

    return result


def parse_geojson(path: str):
    with open(path, "r") as json_file:
        content = gj.load(json_file)
        return content


def main():
    arguments = sys.argv[1:]

    if len(arguments) < 2:
        raise Exception(
            "Usage: ./code.py [camera_<n>_shots.geojson]+  reference_shots.geojson"
        )

    clusters = arguments[:-1]
    references = arguments[-1]

    cluster_gjsons = [parse_geojson(path) for path in clusters]
    ref_gjson = parse_geojson(references)

    result = merge_jsons(ref_gjson, cluster_gjsons)
    with open("output.geojson", "w") as out:
        gj.dump(result, out)


if __name__ == "__main__":
    main()
