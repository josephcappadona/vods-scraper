
def get_page_url(players, characters, tournament, page):
    url = "https://vods.co/melee"
    
    # append player arg(s)
    if len(players) > 0:
        url += '/player/' + players[0]
    if len(players) > 1:
        url += '/player2/' + players[1]

    # append character arg(s)
    if len(characters) > 0:
        url += '/character/' + characters[0]
    if len(characters) > 1:
        url += '/character2/' + characters[1]

    # append tournament arg
    if tournament:
        tournament = clean_tournament_name(tournament)       
        url += '/event/' + tournament

    # append page number
    url += '?page=' + str(page)

    return url       

def clean_tournament_name(tournament):
    tournament = tournament.lower()
    remove = [':', '\'', '"', '.', '&', 'for ', 'on the ']
    for s in remove:
        tournament = tournament.replace(s, '')
    tournament = tournament.replace(' ', '-')
    return tournament
