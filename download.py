import pytube
from pytube.helpers import safe_filename
from pathlib import Path
from os import makedirs, remove
import pickle
from sys import argv
from pprint import pprint


def download_player_match(player, match, output_base_dir='./output', overwrite=False):
    
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

        output_dir = output_base_dir + '/' + player
        makedirs(output_dir, exist_ok=True)
        filepath = Path(output_dir + '/' + new_filename)
        
        print('Downloading %s' % new_title)
        if not filepath.is_file() or overwrite:
            try:
                yt.download(output_dir, filename=new_title)
            except (KeyboardInterrupt, OSError) as e:
                if filepath.is_file():
                    remove(str(filepath))
                raise e
        else:
            print('\tVideo already downloaded')
            
    except (pytube.exceptions.VideoUnavailable, OSError) as e:
        print('\nCould not download video (%s):' % str(type(e)).split("'")[1])
        pprint(match)
        
def load_player(player, data_dir='./output'):
    try:
        filename = '%s.pkl' % player
        matches = pickle.load(open(data_dir + '/' + filename, 'rb'))
        return matches
        
    except:
        raise ValueError # player's match data not yet retrieved
    
    
if __name__ == '__main__':
    if len(argv) < 3:
        print('Usage:  python download.py [-p PLAYER | -f players.txt]')
        quit()
    else:
        players = []
        if argv[1] == '-p':
            players.append(argv[2])
            
        elif argv[1] == '-f':
            with open(argv[2], 'rt') as player_file:
                for player in player_file.read().split('\n'):
                    if player:
                        players.append(player)
                        
        overwrite = False
        if len(argv) > 3 and argv[3] == '-o':
            overwrite = True
            
        for player in players:
            print('\nDownloading VODs for %s\n' % player)

            matches = load_player(player)[:]
            for match in matches: download_player_match(player, match, overwrite=overwrite)
                
            print('\nFinished')
            print('Videos written to %s' % ('./output/%s/' % player))
            
            