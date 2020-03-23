import os
import time
import datetime
import json
import urllib
import urlparse
import dateutil.parser
from argparse import ArgumentParser
from shutil import copyfile

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="file",
                    help="media.json file", metavar="FILE")
json_path = parser.parse_args().file

archive_path = os.path.dirname(json_path)

with open(json_path) as f:
    data = json.load(f)

stories = data['stories']
length = len(stories)

download_dir = 'stories'
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

index = 1

for story in stories:
    print("Processing {0}/{1}".format(index, length))

    current_file_path = os.path.join(archive_path, story['path'])

    file_name = story['path'].split('/')[-1]
    time_stamp = story['taken_at']

    new_file_path = os.path.join(download_dir, file_name)

    if os.path.exists(new_file_path):
        print('File already exists')
    else:
        copyfile(current_file_path, new_file_path)

    date = dateutil.parser.parse(time_stamp)
    utime = time.mktime(date.timetuple())
    os.utime(new_file_path, (utime, utime))

    index = index + 1
