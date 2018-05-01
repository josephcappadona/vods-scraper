from sys import argv
from requests import get
from bs4 import BeautifulSoup

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

def get_match_hrefs(player_html):
    hrefs = []
    vods_player_soup = BeautifulSoup(player_html, 'html5lib')
    tds = vods_player_soup.find_all('td', {'class': 'views-field'})
    for td in tds:
        a = td.find('a')
        if a and a.has_attr('href'):
            hrefs += [a.get('href')]
    return hrefs

def extract_youtube_url(vods_match_url):
    vods_match_html = get_page_html(vods_match_url)
    vods_match_soup = BeautifulSoup(vods_match_html, 'html5lib')
    video_div = vods_match_soup.find('iframe', {'id': 'g1-video'})
    if video_div and video_div.has_attr('src'):
        return video_div.get('src').strip('/')
    else:
        return None

def convert_embed_url_to_watch_url(embed_url):
    args_start_index = embed_url.index('?')
    return embed_url[:args_start_index].replace('embed/', 'watch?v=')

def get_player_youtube_urls(player):
    vods_match_urls = []
    page = 0
    while True:
        player_text = get_player_page(player, page=page)
        hrefs = get_match_hrefs(player_text)
        if hrefs:
            vods_match_urls += hrefs
        else:
            break
        page += 1

    youtube_match_urls = set()
    for vods_match_url in vods_match_urls:

        youtube_url = extract_youtube_url(vods_match_url)
        if youtube_url:
            if 'embed/' in youtube_url:
                youtube_url = convert_embed_url_to_watch_url(youtube_url)

            if youtube_url not in youtube_match_urls:
                youtube_match_urls.add(youtube_url)
                yield youtube_url


if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage:  python get-vods-url.py PLAYER')
        quit()
    else:
        player = argv[1]
        urls = set()
        for url in get_player_youtube_urls(player):
            print(url)


