import os
import re
import copy
import csv

from pprint import pprint

titles_dirs = [
    'f:/a/',
    'h:/a/',
    ]

TITLE = {
    'title': '',
    'year': 0,
    'eps': 0,
    }

FILETYPES = ('.mkv', '.avi', '.ogm')

LOCATION_KEYS = ('OST', 'M', 'N', 'G', 'A', 'psp')
LOCATION = {
    'location': '',
    'OST': False,
    'M': False,
    'N': False,
    'G': False,
    'A': False,
    'psp': False,
    'titles': []
    }

TITLENAME_REGEX = re.compile('(.*?) {0,1}[\[\(]([0-9]{4})[\]\)]')


def count_eps(title_dir):
    count = 0

    isfile = lambda item: os.path.isfile(os.path.join(title_dir, item))
    isdir = lambda item: os.path.isdir(os.path.join(title_dir, item))
    
    items = os.listdir(title_dir)
    files = list(filter(isfile, items))
    dirs = list(filter(isdir, items))
    
    media_files = list(filter(lambda item: item.endswith(FILETYPES), files))

    if len(dirs) > 0 and len(media_files) == 0:
        return count_eps(os.path.join(title_dir, dirs[0]))

    return len(media_files)
        

def process_location(location):
    loc = copy.deepcopy(LOCATION)
    loc['location'] = os.path.basename(location)

    # try:
    #     safe_items = os.listdir(location)
    # except OSError:
    #     pass
    
    for item in os.listdir(location):
        if os.path.isdir(os.path.join(location, item)):
            if item in LOCATION_KEYS:
                loc[item] = True
            else:
                # titlename maybe?
                if TITLENAME_REGEX.match(item):
                    title = copy.deepcopy(TITLE)
                    title['title'], title['year'] = TITLENAME_REGEX.findall(item)[0]
                    title['year'] = int(title['year'])
                    title['eps'] = count_eps(os.path.join(location, item))
                    loc['titles'].append(title)
    return loc


def write_csv(lst, filename):
    with open(filename, 'w') as csv_fh:
        writer = csv.writer(csv_fh, delimiter=';', lineterminator='\n')
        for t in lst:
            writer.writerow(t)


def process_dir(titles_dir):
    titles = []
    locations = []
    media = []
    
    for item in os.listdir(titles_dir):
        loc = process_location(os.path.join(titles_dir, item))
        for t in loc['titles']:
            titles.append((t['title'], t['year'], t['eps']))
            locations.append((t['title'], os.path.basename(os.path.normpath(titles_dir)), item))
        media.append((item,
                      int(loc['OST']),
                      int(loc['M']),
                      int(loc['N']),
                      int(loc['G']),
                      int(loc['A'])
                      ))

    return titles, locations, media

if __name__ == '__main__':
    c = 0
    for title_dir in titles_dirs:
        titles, locations, media = process_dir(title_dir)
##        pprint(titles)
##        pprint(locations)
##        pprint(media)
        c += 1
        name = str(c)
        write_csv(titles, 'e:/' + name + 'titles.csv')
        write_csv(locations, 'e:/' + name + 'locations.csv')
        write_csv(media, 'e:/' + name + 'media.csv')
    









