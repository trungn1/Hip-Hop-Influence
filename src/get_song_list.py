import requests
from bs4 import BeautifulSoup



# def get_song_list(filename):
#     with open (filename, 'r') as f:
#         for line in f:
#             "https://genius.com/artists/{}".format(line)


#this is to get the lyrics in each of the song's pages

def get_song_info(song_url):
    '''
    INPUT: String of the song url
    OUTPUT: Return published date
    '''
    r = requests.get(song_url)
    soup = BeautifulSoup(r, 'html.parser')
    # this is to get the released date of the same in each song page
    soup.find_all('span', class_='song_info-info song_info-info--text_only')


if __name__ == '__main__':
    get_song_info('https://genius.com/Migos-bad-and-boujee-lyrics')
