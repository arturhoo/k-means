# -*- coding: utf-8 -*-
from sys import exit, exc_info


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


if __name__ == '__main__':
    tags = get_set_of_tags_from_file('data/lfm.dat')
    print len(tags)
