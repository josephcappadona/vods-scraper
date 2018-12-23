from sys import argv
from requests import get
from bs4 import BeautifulSoup
from pprint import pprint
import os, pickle

def get_page_html(url):
    req = get(url)
    if req.status_code != 200:
        raise ValueError
    return req.text

def get_player_page(player, page=0):
    vods_player_base_url = "https://vods.co/melee/player/"
    vods_player_url = vods_player_base_url + player + '?page=' + str(page)
    try:
        return get_page_html(vods_player_url)
    except ValueError as e:
        e.args += ('Could not retrieve player page: {}'.format(player),)
        raise error

def get_page_matches(player_page_html):
    matches = []
    vods_player_soup = BeautifulSoup(player_page_html, 'html5lib')
    
    match_tables = vods_player_soup.find_all('table', {'class': 'views-table'})
    for match_table in match_tables:
        date = match_table.caption.text
        
        match_rows = match_table.tbody.find_all('tr')
        for match_row in match_rows:
            
            event = match_row.find('td', {'class': 'views-field-field-event-instance'}).text.strip()
            players = [player.text for player in match_row.find('a').find_all('b')]
            characters = extract_characters(match_row)
            match_format = match_row.find('td', {'class': 'views-field-field-match-format'}).text.strip()
            event_round = match_row.find('td', {'class': 'views-field-field-event-round'}).text.strip()
            
            vod_url = match_row.find('a')['href']
            youtube_url = extract_youtube_url(vod_url)
            
            match = { 'date': date,
                      'event': event,
                      'vod_url': vod_url,
                      'youtube_url': youtube_url,
                      'players': players,
                      'characters': characters,
                      'match_format': match_format,
                      'event_round': event_round }
            matches.append(match)
            pprint(match); print('')
            
    return matches

def extract_characters(match_row):
    chars = {}
    versus_tags = match_row.find('a').find_all()[1:]
    for tag in versus_tags:
        if tag.name == 'b':
            player = None
            player = tag.text.strip()
            print('player: %s' % player)
            chars[player] = []
        elif tag.name == 'img':
            char = parse_character(tag['src'])
            print('char: %s' % char)
            chars[player].append(char)
    return chars

def parse_character(filename):
    return filename.split('/')[-1].split('-')[-1].split('.')[0]

def extract_youtube_url(vods_match_url):
    
    vods_match_html = get_page_html(vods_match_url)
    vods_match_soup = BeautifulSoup(vods_match_html, 'html5lib')
    
    video_div = vods_match_soup.find('iframe', {'id': 'g1-video'})
    if video_div and video_div.has_attr('src'):
        exit
        youtube_url = video_div.get('src').strip('/')
        
        if 'embed/' in youtube_url:
            youtube_url = convert_embed_url_to_watch_url(youtube_url)
        return youtube_url
    
    else:
        return None

def convert_embed_url_to_watch_url(embed_url):
    args_start_index = embed_url.index('?')
    return embed_url[:args_start_index].replace('embed/', 'watch?v=')

def get_player_matches(player):
    player_matches = []
    page = 0
    while True:
        player_page_html = get_player_page(player, page=page)
        page_matches = get_page_matches(player_page_html)
        if page_matches:
            player_matches += page_matches
        else:
            break
        page += 1

    return player_matches


if __name__ == '__main__':
    if len(argv) != 3:
        print('Usage:  python get_vods_url.py [-p PLAYER | -f players.txt]')
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
                        
        os.makedirs('output', exist_ok=True)
        for player in players:
            print('\n\nGetting VODs for %s\n' % player)

            matches = get_player_matches(player)
            print('\nFinished')

            outfile_path = 'output/%s.pkl' % player
            pickle.dump(matches, open(outfile_path, 'wb+'))
            print('Match info written to %s\n\n' % outfile_path)
            
            