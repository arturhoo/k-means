# -*- coding: utf-8 -*-
from utils import get_content_from_file, parse_arguments
from random import random, sample, randint
from scipy import spatial
from numpy import array, mean
from optparse import OptionParser
from sys import exit


class Point(object):
    def __init__(self, vector=None):
        self.vector = array(vector)

    def set_associated_vector(self, base_list, instance_list):
        self.vector = array([1 if item in instance_list else 0 for item in base_list])

    def euclidean_distance(self, point):
        return spatial.distance.euclidean(self.vector, point.vector)

    def sqeuclidean_distance(self, point):
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
            d = self.point.sqeuclidean_distance(cluster)
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


def random_centroids(k):
    rand_list = lambda n: [random() for b in range(1, n + 1)]
    return [Point(rand_list(len(list_of_all_tags))) for i in range(k)]


def forgy_initialization(musics, k):
    return [music.point for music in sample(musics, k)]


def random_partition(musics, k):
    total_of_tags = len(musics[0].point.vector)
    centroids = [Point()] * k
    best_matches = [[] for i in range(k)]
    for music in musics:
        best_matches[randint(0, k - 1)].append(music)
    update_centroids(centroids, best_matches, total_of_tags)
    return centroids


def get_centroids_from_file(musics, k, file_name):
    centroids = []
    for line in get_content_from_file(file_name):
        try:
            centroids.append(Point(musics[int(line)].point.vector))
        except IndexError:
            exit('Specified observation ID doesn\'t exist')
    if len(centroids) != k:
        exit('Specified K differs from number of cluster in file')
    return centroids


def jagota_metric(last_matches, centroids, musics):
    jagota = 0.0
    for idx, centroid in enumerate(centroids):
        distance = 0.0
        for music in last_matches[idx]:
            distance += centroid.euclidean_distance(music.point)
        jagota += distance * (1.0 / len(last_matches[idx]))
    return jagota


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


def output(last_matches):
    music_cluster_list = []
    for idx, cluster in enumerate(last_matches):
        for music in cluster:
            music_cluster_list.append((music, idx))
    music_cluster_list.sort()
    for t in music_cluster_list:
        print t[0], t[1]


if __name__ == '__main__':
    usage_text = 'Usage: %prog -i input_file -k num_of_clusters [-c centroids_file]'
    parser = OptionParser(usage=usage_text)
    (options, args) = parse_arguments(parser)
    file_name = options.input
    k = options.k

    tags = get_set_of_tags_from_file(file_name)
    list_of_all_tags = sorted(tags)
    musics = get_musics_from_file(file_name, list_of_all_tags)

    print 'Numbers of tags:', len(list_of_all_tags)

    if options.centroids_file:
        centroids = get_centroids_from_file(musics, k, options.centroids_file)
    else:
        # centroids = random_centroids(k)
        # centroids = forgy_initialization(musics, k)
        centroids = random_partition(musics, k)

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

    print 'Jagota:', jagota_metric(last_matches, centroids, musics)
