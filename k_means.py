# -*- coding: utf-8 -*-
from utils import get_content_from_file
from random import random, sample, randint
from scipy import spatial
from numpy import array, mean


class Point(object):
    def __init__(self, vector=None):
        self.vector = array(vector)

    def set_associated_vector(self, base_list, instance_list):
        self.vector = array([1 if item in instance_list else 0 for item in base_list])

    def euclidean_distance(self, point):
        return spatial.distance.sqeuclidean(self.vector, point.vector)


class Music(object):
    def __init__(self, mid, list_of_tags, list_of_all_tags):
        self.mid = mid
        self.list_of_tags = list_of_tags
        self.set_point(list_of_all_tags)

    def __repr__(self):
        return self.mid

    def set_point(self, list_of_all_tags):
        self.point = Point()
        self.point.set_associated_vector(list_of_all_tags, self.list_of_tags)

    def find_closest_centroid(self, centroids):
        best_match = -1
        best_match_distance = float("inf")
        for i, cluster in enumerate(centroids):
            d = self.point.euclidean_distance(cluster)
            if d < best_match_distance:
                best_match = i
                best_match_distance = d

        return best_match, best_match_distance


def get_set_of_tags_from_file(file_name):
    content = get_content_from_file(file_name)
    tags = set()
    for line in content:
        tags_from_line = line.strip().split()[1:]
        tags = tags.union(set(tags_from_line))
    return tags


def get_musics_from_file(file_name, list_of_all_tags):
    musics = []
    for line in get_content_from_file(file_name):
        list_from_line = line.strip().split()
        music = Music(list_from_line[0], list_from_line[1:], list_of_all_tags)
        musics.append(music)
    return musics


def update_centroids(centroids, best_matches, total_of_tags=None):
    '''calculate the new means to be the centroid of the observations in the
    cluster
    '''
    if total_of_tags is None:
        total_of_tags = len(centroids[0].vector)
    for i in range(len(centroids)):
        averages = [0.0] * total_of_tags
        if len(best_matches[i]) > 0:
            list_of_points = [music.point.vector for music in best_matches[i]]
            averages = mean(list_of_points, axis=0)
        centroids[i] = Point(averages)


if __name__ == '__main__':
    file_name = 'data/lfm_short.dat'
    k = 8

    tags = get_set_of_tags_from_file(file_name)
    list_of_all_tags = sorted(tags)
    musics = get_musics_from_file(file_name, list_of_all_tags)

    print 'Numbers of tags:', len(list_of_all_tags)

    rand_list = lambda n: [random() for b in range(1, n + 1)]
    centroids = [Point(rand_list(len(list_of_all_tags))) for i in range(k)]

    last_matches = None
    iteration = 1
    while True:
        print 'Iteration', iteration
        total_squared_distace = 0.0
        best_matches = [[] for i in range(k)]

        # find which centroid is the closest for each music
        for music in musics:
            best_match, best_match_distance = \
                music.find_closest_centroid(centroids)
            best_matches[best_match].append(music)
            total_squared_distace += best_match_distance

        for i, match in enumerate(best_matches):
            print i, len(match)
        print 'Total distance:', total_squared_distace
        print '-----'

        # if the results are the same as last time, this is complete
        if best_matches == last_matches:
            break
        last_matches = best_matches

        # move the centroids to the average of their members
        print 'Moving the centroids'
        update_centroids(centroids, best_matches)

        iteration += 1
