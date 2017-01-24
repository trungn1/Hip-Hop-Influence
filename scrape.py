import requests
from bs4 import BeautifulSoup
import re


def create_artist_list(text_file):
    '''
    Input: A string txt file with a list of all the artists from wikipedia genre, artistname, it pulls out the artist
    Output: Nothing, it pulls out the artist names and writes into a file
    '''
    artists = []
    with open(text_file) as f:
        for line in f:
            artists.append(line.split(', ')[1].strip())

    #writing the artist
    with open ('data/artist_list.txt', 'w') as output:
        for artist in artists:
            output.write(artist+"\n")

def get_list(filename):
    '''
    Input: A string txt file with a list of all the artists or songs
    Output: Returns sorted set list of all the aritsts
    '''
    artist_list = []
    with open(filename, 'r') as f:
        for artist in f:
            artist_list.append(artist.strip())

    return sorted(set(artist_list))


def get_artist_pages(artist_list):
    '''
    Input: A list of all the artists
    Output: Nothing, it writes out a file with all the links of the artists' genius proposed page
    '''
    for artist in artist_list:
        link = 'https://genius.com/artists/{}'.format(artist)
        print 'added{}'.format(artist)
        with open('data/artist_page_links.txt', 'a') as f:
                f.write(link + '\n')

    # # initialize an emtpy links
    # artists_links = []
    # for artist in artist_list:
    #
    #     first_letter = artist[0]
    #
    #     if first_letter.isdigit():
    #         r1 = requests.get("https://genius.com/artists-index/0").content
    #     else:
    #         r1 = requests.get("https://genius.com/artists-index/" + first_letter.lower()).content
    #
    #     soup1 = BeautifulSoup(r1, "html.parser")
    #
    #     artists_pages = soup1.find_all("li")
    #
    #     for page in artists_pages:
    #         if page.text.strip() == artist:
    #             print 'It worked for {}'.format(artist)
    #             link = 'https://genius.com/artists/{}'.format(artist)
    #             artists_links.append(link)
    #             with open('data/artist_page_links.txt', 'a') as f:
    #                     f.write(link + '\n')
    #         else:
    #             print 'It did not work for {},{}'.format(artist)

                # code not necessary
                # try:
                #     link = page['href']
                #     artists_links.append(link)
                #     with open('data/artist_page_links.txt', 'a') as f:
                #             f.write(link + '\n')
                #     print 'It worked for {}'.format(artist)
                # except KeyError:
                #     print 'KeyError for {}'.format(artist)
                #     continue
    # return artists_links`


#get artist songs
def get_artist_songs(artist_links):
    '''
    Input: A list of all the artist page links
    Output: Nothing, it writes out a file with all the links of the artist's genius page
    '''
    artist_songs_dict = {}
    # import pdb; pdb.set_trace()
    for link in artist_links:
        artist = link.split('/')[-1]
        r2 = requests.get(link).content
        soup2 = BeautifulSoup(r2, "html.parser")

        # This try and except is to account for artist with less than 20 songs
        try:
            all_songs_link = soup2.findAll('a', href=re.compile('^/artists/song?'))[0]['href']
        except IndexError:
            print 'Failed for this link {}'.format(link)
            continue

        r3 = requests.get("https://genius.com" + all_songs_link).content
        soup3 = BeautifulSoup(r3, "html.parser")

        songs_links_list = []
        songs_index_page = 1

        # This try and except is to account for artist with less than 20 songs
        try:
            songs_end_page = soup3.findAll("div", {"class": "pagination"})[0].text.split()[-3]
        except IndexError:
            print 'This link failed {}'.format(artist)
            continue

        while songs_index_page <= int(songs_end_page):
            r4 = requests.get("https://genius.com" + all_songs_link + '&page=' + str(songs_index_page)).content
            soup4 = BeautifulSoup(r4, "html.parser")
            stuff = soup4.find_all('li')

            for item in stuff:
                if item.has_attr('data-id'):
                    #commenting this out
                    # songs_links_list.append(item.a['href'])
                    with open('data/song_url.txt','a') as f:
                        f.write(item.a['href']+'\n')
                    print "wrote song {}".format(item.a['href'])
            songs_index_page += 1
        artist_songs_dict[artist] = songs_links_list

    # try to write as dictionary
    # return artist_songs_dict
def filter_song_url(filename):
    '''
    Input: Filename
    Output: Writes to new file and returns a list of links
            Removes: 'instrumental' , 'remix', 'rmx' , 'annotated',
            'interlude' 'excerpt', 'freestyle', 'cover', 'mixtape'
    '''
    filter_word = ['instrumental' , 'remix', 'rmx' , 'annotated',\
        'interlude' 'excerpt', 'freestyle', 'cover', 'mixtape']
    song_links = set()
    with open(filename, 'r') as urls:
        for url in urls:
            #cleaning out the duplicate and filler words
            for word in filter_word:
                if word in url.strip().lower():
                    continue
                else:
                    song_links.add(url.strip())

    with open('data/final_song_links.txt', 'w') as final:
        for link in song_links:
            final.write(link +'\n')
    return song_links

#this one should work
def get_song_lyrics(links):
    '''
    Input: A list of all the artist
    Output: Nothing, it writes out a file with all the links of the artist's genius page
    '''
    #changed this to iterkeys
    x=1
    for link in links:
        file_name = link.split('/')[-1]
        r = requests.get(link).content
        soup = BeautifulSoup(r, "html.parser")
        with open('songs/{}.html'.format(file_name), 'w') as f:
            f.write(str(soup))
        x += 1
        print "I printed out{}, song #{}".format(file_name, x)

if __name__ == "__main__":
    #opens the initial list
    # create_artist_list('data/ArtistsListCollab.txt')

    #open the artist_list (confirmed to be on genius) - and get artist url
    # artist_list = get_list('data/artist_list.txt')
    # get_artist_pages(artist_list)

    # go to artist url and get song url
    # artist_link = get_list('data/artist_page_links.txt')
    # get_artist_songs(artist_link)

    # go to song url and scrape song lyrics
    final_list = filter_song_url('data/song_url.txt')
    # get_song_lyrics(final_list)
