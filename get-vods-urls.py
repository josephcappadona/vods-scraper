from sys import argv
from requests import get
from bs4 import BeautifulSoup

player = argv[1]


def get_player_page(player, page=0):
    vods_player_base_url = "https://vods.co/melee/player/"
    req = get(vods_player_base_url + player + '?page=' + str(page))
    if vods_req.status_code != 200:
        error = ValueError()
        error.args += ('Could not retrieve player page: {}'.format(player),)
        raise error
    return req.text

def get_match_elements(html):
    player_soup = BeautifulSoup(player_text, "html5lib")
    tds = vods_player_soup.find_all('td', {'class': 'views-field'})

vods_match_urls = []
player_text = get_player_page('Armada')

while len(tds) > 0:
    for td in tds:
        a = td.find('a')
        if a and a.has_attr('href'):
            vods_match_urls += [a.get('href')]





