# -*- coding: utf-8 -*-
from sys import exit, exc_info


class Music(object):
    """docstring for Music"""
    def __init__(self, id, list_of_tags):
        self.list_of_tags = list_of_tags

    def set_associated_point(self, list_of_all_tags):
        self.associated_point = [1 if tag in self.list_of_tags
                                 else 0
                                 for tag in list_of_all_tags]


def get_content_from_file(file_name):
    try:
        with open(file_name) as f:
            content = f.readlines()
            f.close()
    except IOError as e:
        print 'I/O error({0}): {1}'.format(e.errno, e.strerror)
        exit()
    except:
        print 'Unexpected error: ', exc_info()[0]
        exit()
    return content


def get_set_of_tags_from_file(file_name):
    content = get_content_from_file(file_name)
    tags = set()
    for line in content:
        tags_from_line = line.strip().split()[1:]
        tags = tags.union(set(tags_from_line))
    return tags


def get_associated_point(list_of_tags, observation):
    return [1 if tag in observation else 0 for tag in list_of_tags]


if __name__ == '__main__':
    file_name = 'data/lfm.dat'
    musics = []
    tags = get_set_of_tags_from_file(file_name)
    list_of_all_tags = sorted(tags)
    for line in get_content_from_file(file_name):
        list_from_line = line.strip().split()
        music = Music(list_from_line[0], list_from_line[1:])
        music.set_associated_point(list_of_all_tags)
        musics.append(music)
