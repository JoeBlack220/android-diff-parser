from os import listdir
from os.path import isfile, join
import random
import os
import shutil
from shutil import copyfile

inputDir = "../res/split/android-5.0.0_r1_android-5.1.0_r1/all/"
outputDir = "../res/split/android-5.0.0_r1_android-5.1.0_r1/sample/"


def getFiles(dir):
    files = [f for f in listdir(dir) if isfile(join(dir, f))]
    return files


def cleanDir(dir):
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def sample(inputDir, outputDir, num, seed):
    files = getFiles(inputDir)
    rand = random.Random(seed)
    rand.shuffle(files)
    num = len(files) if num >= len(files) else num
    samples = files[:num]
    print(samples)

    for sample in samples:
        copyfile(join(inputDir, sample), join(outputDir, sample))
    print(samples)


cleanDir(outputDir)
sample(inputDir, outputDir, 160, 2020)
