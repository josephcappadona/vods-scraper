

valid_prefixes = set(['-p', '-c', '-t'])

def parse_args(args):
    
    arg_tuples = zip(argv[1:-1:2], argv[2::2])
    if any(prefix not in valid_prefixes for prefix, _ in arg_tuples):
        raise ValueError # illegal argument format

    players = []
    valid_characters = set()
    valid_tournaments = set()
    for i, (prefix, suffix) in enumerate(parsed_args):
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
    return players, valid_characters, valid_touraments, limit


def create_handle(players, characters, tournament, limit):
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


