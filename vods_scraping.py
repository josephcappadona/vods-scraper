from requests import get
from bs4 import BeautifulSoup
from pprint import pprint


def get_page_html(url):
    req = get(url)
    if req.status_code != 200:
        raise ValueError('Could not retrieve page: {}'.format(url))
    return req.text

def get_page_matches(page_url, limit=None):
    matches = []
    page_html = get_page_html(page_url)
    soup = BeautifulSoup(page_html, 'html5lib')
    
    match_tables = soup.find_all('table', {'class': 'views-table'})
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

            if limit and len(matches) >= limit:
                return matches
            
    return matches

def extract_characters(match_row):
    chars = {}
    versus_tags = match_row.find('a').find_all()[1:]
    for tag in versus_tags:
        if tag.name == 'b':
            player = None
            player = tag.text.strip()
            chars[player] = []
        elif tag.name == 'img':
            char = parse_character(tag['src'])
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


