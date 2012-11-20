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


def parse_arguments(parser):
    '''parse the arguments provided in the command line'''
    parser.add_option('-i', '--input', type='string', help='input file',
                      dest='input')
    parser.add_option('-k', '--k', type='int', help='number of clusters',
                      dest='k')
    parser.add_option('-c', '--centroids', type='string',
                      help='centroids file', dest='centroids_file')
    parser.add_option('-d', '--debug', action='store_true',
                      help='debug info', dest='debug')
    (options, args) = parser.parse_args()
    if not options.input:
        parser.error('Input filename not given')
    if not options.k:
        parser.error('Number of clusters K not given')
    return(options, args)
