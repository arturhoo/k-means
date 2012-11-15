# -*- coding: utf-8 -*-
from utils import get_content_from_file
from random import random


class Point(object):
    # maybe leave the constructor empty and create a method for building the
    # vector from base and instace lists
    def __init__(self, base_list=None, instance_list=None):
        if base_list is not None and instance_list is not None:
            self.vector = [1 if item in instance_list
                           else 0
                           for item in base_list]
        else:
            self.vector = []

    def euclidean_distance(self, point):
        squares = [(x - y) ** 2 for x, y in zip(self.vector, point.vector)]
        return sum(squares)


class Music(object):
    def __init__(self, id, list_of_tags):
        self.id = id
        self.list_of_tags = list_of_tags
        self.point = None

    def set_point(self, list_of_all_tags):
        self.point = Point(list_of_all_tags, self.list_of_tags)


def get_set_of_tags_from_file(file_name):
    content = get_content_from_file(file_name)
    tags = set()
    for line in content:
        tags_from_line = line.strip().split()[1:]
        tags = tags.union(set(tags_from_line))
    return tags


def calculate_total_squared_distance(clusters, best_matches, musics):
    total_squared_distace = 0.0
    for i, match in enumerate(best_matches):
        for matched_music in match:
            cluster_point = Point()
            cluster_point.vector = clusters[i]
            d = matched_music.point.euclidean_distance(cluster_point)
            total_squared_distace += d
    print 'Total distance:', total_squared_distace


if __name__ == '__main__':
    file_name = 'data/lfm_short.dat'
    k = 5
    musics = []
    tags = get_set_of_tags_from_file(file_name)
    list_of_all_tags = sorted(tags)

    print 'Numbers of tags:', len(list_of_all_tags)

    for line in get_content_from_file(file_name):
        list_from_line = line.strip().split()
        music = Music(list_from_line[0], list_from_line[1:])
        music.set_point(list_of_all_tags)
        musics.append(music)

    rand_bin_list = lambda n: [random() for b in range(1, n + 1)]
    clusters = [rand_bin_list(len(list_of_all_tags)) for i in range(k)]

    last_matches = None
    for t in range(100):
        print 'Iteration', t
        total_squared_distace = 0.0
        best_matches = [[] for i in range(k)]

        # find which centroid is the closest for each music
        for music in musics:
            best_match = -1
            best_match_distance = float("inf")
            for i, cluster in enumerate(clusters):
                cluster_point = Point()
                cluster_point.vector = cluster
                d = music.point.euclidean_distance(cluster_point)
                if d < best_match_distance:
                    best_match = i
                    best_match_distance = d
            best_matches[best_match].append(music)
            total_squared_distace += best_match_distance

        # if the results are the same as last time, this is complete
        if best_matches == last_matches:
            break
        last_matches = best_matches

        # move the centroids to the average of their members
        print 'Moving the centroids'
        for i in range(k):
            averages = [0.0] * len(list_of_all_tags)
            if len(best_matches[i]) > 0:
                list_of_points = [music.point.vector for music in best_matches[i]]
                sum_of_points = [sum(value) for value in zip(*list_of_points)]
                averages = [float(ssum) / float(len(list_of_points)) for ssum in sum_of_points]
            clusters[i] = averages

        for i, match in enumerate(best_matches):
            print i, len(match)
        print 'Total distance:', total_squared_distace
