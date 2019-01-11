from sys import argv
from os import makedirs
from pickle import dump
from vods_args import parse_args, create_handle
from vods_scraping import get_page_matches
from vods_url import get_page_url


def get_matches(players, characters, tournament, limit):
    matches = []
    page = 0
    if not limit: limit = 10**10

    while True:
        page_url = get_page_url(players, characters, tournament, page)
        page_matches = get_page_matches(page_url, limit=(limit-len(matches)))
        if page_matches:
            matches += page_matches

            if limit and len(matches) >= limit:
                matches = matches[:limit]
                break
        else:
            break
        page += 1

    return matches


if __name__ == '__main__':

    usage = 'Usage:  python get_vods.py [-p PLAYERS] [-c CHARACTERS] [-t TOURNAMENT] [-l LIMIT]'
    if len(argv) < 2:
        print(usage)
        quit()

    try:
        players, characters, tournament, limit = parse_args(argv)
    except ValueError:
        print('Arguments not formatted correctly.\n')
        print(usage)
        exit()
    
    makedirs('output', exist_ok=True)
    file_handle = create_handle(players, characters, tournament, limit)
    outfile_path = 'output/%s.pkl' % file_handle

    print('\n\nGetting VODs for \'%s\'\n\n' % file_handle)
    matches = get_matches(players, characters, tournament, limit)
    print('\nFinished')

    dump(matches, open(outfile_path, 'wb+'))
    print('Match info written to \'%s\'\n\n' % outfile_path)
        
        
