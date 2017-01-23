import pandas as pd

def check_membership(artists_list):
    '''
    Input: List of new artist to check
    Output: None, function will write to output file with new artist
    '''
    #initializing list to check
    to_add = []

    #checking for membership to filter for new artists
    with open ('artists_check.txt', 'r') as f:
        for artist in f:
            if artist.strip().lower() not in artists_list:
                to_add.append(artist)

    to_add = sorted(set(to_add))

    #writing the new artist to a text file
    with open('new_artist.txt','w') as f:
        for new in to_add:
            f.write('hip-hop; {}'.format(new))

if __name__ == '__main__':
    #opening the current artist file
    artists = []
    with open('ArtistsListCollab.txt') as f:
        for line in f:
            artists.append(line.split(', ')[1].strip().lower())

    check_membership(artists)
