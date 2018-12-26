import pytube
from pytube.helpers import safe_filename
from pathlib import Path
from os import makedirs, remove
import pickle
from sys import argv
from pprint import pprint


def download_player_match(player, match, output_base_dir='./output'):
    
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
        if not filepath.is_file():
            try:
                yt.download(output_dir, filename=new_title)
                return True
            
            except (KeyboardInterrupt, OSError) as e:
                if filepath.is_file():
                    remove(str(filepath))
                raise e
        else:
            print('\tVideo already downloaded')
            
    except (pytube.exceptions.VideoUnavailable, OSError) as e:
        print('\nCould not download video (%s):' % str(type(e)).split("'")[1])
        pprint(match)
        print('')
    
    return False
        
def load_player(player, data_dir='./output'):
    try:
        filename = '%s.pkl' % player
        matches = pickle.load(open(data_dir + '/' + filename, 'rb'))
        return matches
        
    except:
        raise ValueError # player's match data not yet retrieved
    
    
if __name__ == '__main__':
    if len(argv) < 3:
        print('Usage:  python download.py [-p PLAYER | -P players.txt] [-c CHARACTER | -C characters.txt] [-t tournament] [-l limit]')
        quit()
    else:
        parsed_args = enumerate(zip(argv[1:-1:2], argv[2::2]))
        
        players = set()
        valid_characters = set()
        valid_tournaments = set()
        limit = 10**10
        for i, (prefix, suffix) in parsed_args:
            ind = 2 + i*2
            
            if prefix == '-p':
                players.add(suffix)
                
            elif prefix == '-P':
                with open(suffix, 'rt') as player_file:
                    for player in player_file.read().split('\n'):
                        if player:
                            players.add(player)
                
            elif prefix == '-c':
                valid_characters.add(suffix)
                    
            elif prefix == '-C':
                with open(suffix, 'rt') as character_file:
                    for character in character_file.read().split('\n'):
                        if character:
                            valid_characters.add(character)
            
            elif prefix == '-t':
                valid_tournaments = tournaments.add(suffix)
                
            elif prefix == '-T':
                with open(suffix, 'rt') as tournament_file:
                    for tournament in tournament_file.read().split('\n'):
                        if tournament:
                            valid_tournaments.add(character)
                    
            elif prefix == '-l':
                limit = int(suffix)
                
        for player in players:
            print('\nDownloading VODs for %s\n' % player)

            matches = load_player(player)
            n_downloaded = 0
            for match in matches:
                
                match_characters = set([character for character_list in match['characters'].values() for character in character_list])
                
                if (not valid_characters or all((character in match_characters) for character in valid_characters)) and (not valid_tournaments or tournament in valid_tournaments):
                        
                    downloaded = download_player_match(player, match)
                    if downloaded:
                        n_downloaded += 1
                        if n_downloaded >= limit:
                            print('Reached limit of %d' % limit)
                            break

            print('\nFinished')
            print('Videos written to %s' % ('./output/%s/' % player))
            
            