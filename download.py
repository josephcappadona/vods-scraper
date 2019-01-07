import pytube
from pytube.helpers import safe_filename
from pathlib import Path
from os import makedirs, remove
import pickle
from sys import argv
from pprint import pprint
from vods_args import parse_args, create_handle


def download_match(match, video_dir):
    
    youtube_url = match['youtube_url']
    p1, p2 = match['players']
    c1 = ' '.join(match['characters'][p1])
    c2 = ' '.join(match['characters'][p2])
    event = match['event']
    event_round = match['event_round']
    match_format = match['match_format']
    date = match['date']
    
    new_title = '%s (%s) vs %s (%s) - %s %s (%s) - %s' % (p1, c1, p2, c2, event, event_round, match_format, date)
    
    try:
        yt = pytube.YouTube(youtube_url).streams.first()
        new_filename = safe_filename(new_title) + '.' + yt.mime_type.split('/')[-1]
        video_fp = Path(video_dir + '/' + new_filename)
        
        print('Downloading %s' % new_title)
        if not video_fp.is_file():
            try:
                yt.download(video_dir, filename=new_title)
                return True
            
            except (KeyboardInterrupt, OSError) as e:
                if filepath.is_file():
                    remove(str(filepath))
                raise e
        else:
            print('\tVideo already downloaded. Skipping...')
            
    except (pytube.exceptions.VideoUnavailable, OSError) as e:
        print('\nCould not download video (%s):' % str(type(e)).split("'")[1])
        pprint(match)
        print('')
    
    return False
        
def load_matches(handle, data_dir='output'):
    try:
        filename = '%s.pkl' % handle
        matches = pickle.load(open(data_dir + '/' + filename, 'rb'))
        return matches
        
    except:
        raise ValueError # player's match data not yet retrieved
    
    
if __name__ == '__main__':

    usage = 'Usage:  python download.py [-p PLAYER] [-c CHARACTER] [-t tournament]'
    if len(argv) < 2:
        print(usage)
        quit()

    try:
        players, characters, tournament = parse_args(argv)
    except ValueError:
        print('Arguments not formatted correctly.\n')
        print(usage)
        exit()
    
    data_dir = 'output'
    file_handle = create_handle(players, characters, tournament)
    video_dir = '%s/%s' % (data_dir, file_handle)
    makedirs(video_dir, exist_ok=True)

    matches = load_matches(file_handle, data_dir=data_dir)
    print('\nDownloading VODs for \'%s\'\n' % file_handle)
    try:
        for match in matches:
            download_match(match, video_dir)
    except KeyboardInterrupt:
        print('Keyboard interrupt detected. Stopping script...')

    print('\nFinished')
    print('Videos written to \'%s\'' % video_dir)
    
    
