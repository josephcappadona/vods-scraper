from sys import argv
from os import makedirs, remove
from pickle import load
from pprint import pprint
from pathlib import Path
from vods_args import parse_args, create_handle
from pytube import YouTube
from pytube.helpers import safe_filename
from pytube.exceptions import VideoUnavailable

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
        print('\n\t\tDownloading %s' % new_title)
        yt = YouTube(youtube_url).streams.first()
        new_filename = safe_filename(new_title) + '.' + yt.mime_type.split('/')[-1]
        video_fp = Path(video_dir + '/' + new_filename)
        
        if not video_fp.is_file():
            try:
                yt.download(video_dir, filename=new_title)
                return True
            
            except (KeyboardInterrupt, OSError) as e:
                if filepath.is_file():
                    remove(str(filepath))
                raise e
        else:
            print('\t\t\tVideo already downloaded. Skipping...')
            
    except (VideoUnavailable, OSError) as e:
        print('\t\t\tCould not download video (%s):' % str(type(e)).split("'")[1])
        pprint(match)
        print('')
    
    return False
        
def load_matches(handle, data_dir='output'):
    try:
        filename = '%s.pkl' % handle
        filepath = data_dir + '/' + filename
        print('\nLoading matches from \'%s\'' % filepath)
        matches = load(open(filepath, 'rb'))
        return matches
        
    except:
        raise ValueError # player's match data not yet retrieved
    
    
if __name__ == '__main__':

    usage = 'Usage:  python download.py [-p PLAYER] [-c CHARACTER] [-t tournament] [-l LIMIT]'
    if len(argv) < 2:
        print(usage)
        quit()

    try:
        players, characters, tournament, limit = parse_args(argv)
    except ValueError:
        print('Arguments not formatted correctly.\n')
        print(usage)
        exit()
    
    data_dir = 'output'
    file_handle = create_handle(players, characters, tournament, limit)
    video_dir = '%s/%s/' % (data_dir, file_handle)
    makedirs(video_dir, exist_ok=True)

    matches = load_matches(file_handle, data_dir=data_dir)
    print('\n\tDownloading VODs for \'%s\'' % file_handle)
    try:
        for match in matches:
            download_match(match, video_dir)
    except KeyboardInterrupt:
        print('Keyboard interrupt detected. Stopping script...')

    print('\nFinished')
    print('Videos written to \'%s\'' % video_dir)
    
    
