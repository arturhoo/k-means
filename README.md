# k-Means Algorithm

Artur Oliveira Rodrigues ; artur [at] dcc.ufmg.br

The documentation (in Portuguese) is located in the `doc` directory, and the
reference file is `doc/tp2.pdf`.


## Implementation

The algorithm was implemented in Python and its code can be found at
`k_means.py`. Additional code is also located in the file `utils.py`.

The way the k-Means algorithm was implemeted allows the tuning of multiple
parameters, as follows:

    positional arguments:
      -i, --input           observations file
      -k, --num_of_clusters number of clusters

    optional arguments:
      -c, --centroids_file  file contaning user-specified initial centroids
      -d, --debug           display debug information
      -h, --help            show this help message and exit

Here is a sample parameters configuration:

    $ python k_means.py -i data/lfm.dat -k 3

and here is the sample output (simplified for clarity):

    0 2
    1 2
    2 0
    3 2
    4 2
    (...)
    4995 1
    4996 1
    4997 1
    4998 1
    4999 1
