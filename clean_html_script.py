from bs4 import BeautifulSoup
import os

def get_lyrics(soup_obj):
    '''
    Input: The soup object
    Output: The artist name from the soup object
    '''
    try:
        lyrics_list = soup_obj.find('lyrics').text.split('\n')
    except AttributeError:
        lyrics_list = ['','']
        print 'Did not get lyrics for {}'.format(filename)
    return lyrics_list


def get_artist_name(soup_obj):
    '''
    Input: The soup object
    Output: The artist name from the soup object
    '''
    #try to account for pages that are not songs
    try:
        artist = soup_obj.find_all('span', {'itemprop':'title'})[2].text
    except IndexError:
        artist = 'None'
    return artist

def get_date_published(soup_obj):
    '''
    Input: The soup object
    Output: Return the release date for the soup object
    '''
    #gets release_date
    date_published = soup_obj.find_all('span', {"class":"song_info-info song_info-info--text_only"})[-1].text
    if not date_published:
        return 'None'
    return date_published

def get_songname(soup_obj):
    '''
    Input: The soup object
    Output: Returns the song name from the soup object
    '''
    #this pulls the song and accept pages that are not actually songs - such as album page
    try:
        song_name = soup_obj.find_all('span', {'itemprop':'title'})[-1].text
    except IndexError:
        song_name = 'None'
    return song_name


def clean_html_page(filename):
    '''
    This function is parse the html file

    Input: The html file name
    Output: It returns atrist name, date_published, song_name, lyrics
    '''

    #open the html response file and parse out the lyrics
    song = open('songs/' + filename).read().decode('utf-8', 'replace')
    soup = BeautifulSoup(song, 'html.parser')

    #getting the list for all the lyrics
    lyrics_list = get_lyrics(soup)

    #need to filter out the [] lines that dictates [verse], [hook], [offset]
    no_bracket_lyrics = []
    for line in lyrics_list:
        if line.startswith('[')==False:
            no_bracket_lyrics.append(line)
    # Joining the list of lyrics into a string
    no_bracket_lyrics_join = ' '.join(no_bracket_lyrics)

    #gettting the published date of the song
    date_published = get_date_published(soup)

    #this pulls the song and accept pages that are not actually songs - such as album page
    song_name = get_songname(soup)

    #this is to get the artist's name
    artist = get_artist_name(soup)

    #need to account for unicode name
    odd_names = ['beyonc']

    #need to acccount for odd names
    for odd_name in odd_names:
        if odd_name in artist.lower():
            artist = odd_name

    return artist, date_published, song_name, no_bracket_lyrics_join

if __name__ == '__main__':
    directory = raw_input('Enter directory name: usually it is usually /home/ec2-user/songs')

    start_num = 1
    with open ('output/output.txt', 'w') as f:
        f.write('artist;;;date_published;;;song_name;;;page;;;full_lyrics\n')

    for page in os.listdir(directory)[1:]:
        artist, date_published, song_name, lyrics = clean_html_page(page)
        with open ('output/output.txt', 'a') as f:
            try:
                f.write(artist + ';;;'  + date_published + ';;;' + song_name + ';;;' + str(page) + ';;;' + lyrics + '\n')
                print 'I wrote this song {}, song {}'.format(song_name, start_num)
            except UnicodeEncodeError:
                print "UnicodeEncodeError for song {}".format(start_num)
            start_num += 1
