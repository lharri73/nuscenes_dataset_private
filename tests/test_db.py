################################################################################
## Date Created  : Fri Jun 14 2019                                            ##
## Authors       : Landon Harris, Ramin Nabati                                ##
## Last Modified : Sat Jun 15 2019                                            ##
## Copyright (c) 2019                                                         ##
################################################################################

from context import pynuscenes
import os
import pickle
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--data_location', type=str, default='../data/datasets/nuscenes')
parser.add_argument('--versions')

FLAGS = parser.parse_args()

def test_nuscenes_db():
    logger = logging.getLogger('pynuscenes')
    root = FLAGS.data_location
    nusc = None
    passed = True
    for nuscenes_version in pynuscenes.utils.constants.NUSCENES_SPLITS.keys():
        num_samples = 0
        for split in pynuscenes.utils.constants.NUSCENES_SPLITS[nuscenes_version]:
            nuscenes_db = pynuscenes.NuscenesDB(root, nusc_version=nuscenes_version, split=split, nusc=nusc)
            nuscenes_db.generate_db()
            num_samples += len(nuscenes_db.db['frames'])

        if len(nuscenes_db.nusc.sample) != num_samples:
            logger.critical('Length of nuscenes samples does not match samples in db for {}'.format(nuscenes_version))
            logger.critical('length should be {}, but got {}'.format(len(nuscenes_db.nusc.sample), num_samples))
            passed = False
        else:
            passed = True
    if passed:    
        logger.info('Passed!')
    else:
        logger.error('Test failed...see output above')
    logger.info('Waiting to remove nuscenes from memory...')

if __name__ == "__main__":
    test_nuscenes_db()