
valid_prefixes = set(['-p', '-c', '-t'])

def parse_args(args):
    
    arg_tuples = list(zip(args[1:-1:2], args[2::2]))
    if any(prefix not in valid_prefixes for prefix, _ in arg_tuples):
        raise ValueError # illegal argument format

    players = []
    characters = []
    tournament = ''
    for i, (prefix, suffix) in enumerate(arg_tuples):
        ind = 2 + i*2
        
        if prefix == '-p':
            players.extend(suffix.split(','))
           
        elif prefix == '-c':
            characters.extend(suffix.split(','))
        
        elif prefix == '-t':
            tournament = suffix

    return players, characters, tournament


def create_handle(players, characters, tournament):
    strs = []
    if players:
        players_str = '_'.join(players)
        strs.append(players_str)
    if characters:
        characters_str = '_'.join(characters) if characters else ''
        strs.append(characters_str)
    if tournament:
        strs.append(tournament)

    # if no args specified, we are pulling all Melee matches
    if not strs:
        strs.append('Melee')

    return '-'.join(strs)


def is_valid_match(match, valid_characters, valid_tournaments):
    
    match_characters = set([character for character_list in match['characters'].values() for character in character_list])

    characters_are_valid = not valid_characters or all((character in match_characters) for character in valid_characters)
    tournaments_are_valid = not valid_tournaments or tournament in valid_tournaments

    return characters_are_valid and tournaments_are_valid


