
if __name__ == '__main__':
    artist_list = []
    # open the artist list for Wikipedia
    with open( 'classification.txt' ,'r') as f:
        for line in f:
            artist_list.append(line)
    # write the header line
    with open ('artist_classification.txt', 'a') as f:
        f.write('artist_id|classification| artist' + '\n')
    # loop through the artist list and classify based on position
    artist_id = 1
    with open ('artist_classification.txt', 'a') as f:
        geography = 'East-Coast'
        for artist in artist_list:
            # change geography based on separator
            if artist.strip() == 'STOP':
                geography = 'West-Coast'
            elif artist.strip() == '2 Chainz':
                geography = 'Dirty-South'

            # Additional parsing to remove the comments in parentheses()
            if '(' in artist:
                to_add = artist.strip().split('(')
                to_add = ' '.join(to_add[ :-1])
                f.write(str(artist_id) + '|' + geography + '|' + to_add [:-1] + '\n')
            else:
                to_add = artist.strip()
                f.write(str(artist_id) + '|' + geography + '|' + to_add + '\n')
            artist_id += 1
