import os
import sys
import boto3
import threading
import botocore
import argparse
from botocore import UNSIGNED
from botocore.config import Config

SAVE_TO = '/lustre/scratch123/tol/teams/grit/geval_pipeline/grit_rawdata/vgp/data'
PREFIX = 'mammals'
TOLID = 'mRhiSin1'
LATIN_NAME = 'Rhinolophus_sinicus'

# INCOMPLETE CLADE DICT
master_dict = {'a': 'amphibians',
               'b': 'birds',
               'd': 'dicotyledons',
               'e': 'echinoderms',
               'f': 'fish',
               'g': 'fungi',
               'h': 'platyhelminths',
               'i': 'insects',
               'l': 'monocotyledons',
               'm': 'mammals',
               'n': 'nematodes',
               'o': 'sponges',
               'p': 'protists',
               'r': 'reptiles',
               's': 'sharks'
               }

# NOT MINE - I HAVE NO IDEA HOW IT WORKS
class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            sys.stdout.write(
                "\r%s --> %s bytes transferred" % (
                    self._filename, self._seen_so_far))
            sys.stdout.flush()


def parseargs():
    """
    argparse function to collect cli arguments
    :return: args
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("tolid",
                        help="TolID")
    parser.add_argument("latin",
                        help="Latin Name")
    parser.add_argument("-dir",
                        "--directory-override",
                        help="A boolean to change vgp directory to the cwd",
                        store=True)
    args = parser.parse_args()
    return args


def get_fl(tolid):
    prefix = tolid[0]
    fullname = master_dict.get(prefix)
    return fullname


def download_all_objects_in_folder(prefix, tolid, latin, override):
    s3_resource = boto3.resource('s3',
                                 config=Config(signature_version=UNSIGNED))
    my_bucket = s3_resource.Bucket('genomeark')
    # It will just pass over directories that don't exist
    folder_list = ['arima', '10x', 'pacbio', 'bionano']
    for i in folder_list:
        # Should be re-written to be more customisable
        if override:
            dir = f'{SAVE_TO}/{prefix}/{latin}/genomic_data/{i}'
        else:
            dir = './'

        objects = my_bucket.objects.filter(Prefix=f'species/{latin}/{tolid}/genomic_data/{i}')
        for obj in objects:
            path, filename = os.path.split(obj.key)
            # VERY SIMPLE FILTER HERE
            if filename.endswith('.pbi'):
                pass
            elif filename.endswith('.bnx'):
                pass
            else:
                print(f'Downloading:: {filename} :: {i}')
                try:
                    os.makedirs(dir)
                except FileExistsError:
                    pass

                print(f'Downloading :: {filename} :: {dir}')
                my_bucket.download_file(obj.key,
                                        f'{dir}/{filename}',
                                        Callback=ProgressPercentage(f'{dir}/{filename}'))


def main():
    args = parseargs()
    latin = args.latin
    tolid = args.tolid
    override = args.dir

    prefix = get_fl(args.tolid)
    download_all_objects_in_folder(prefix, tolid, latin, override)


if __name__ == '__main__':
    main()
