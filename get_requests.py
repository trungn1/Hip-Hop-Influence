import requests
from bs4 import BeautifulSoup


if __name__ == "__main__":
    #initialize an empty
    final_list = []

    # to get the links of the text file
    file_name = raw_input('File_name')

    with open(file_name, 'r') as final:
        for link in final:
            final_list.append(link.strip())
    # counter variable to keep track of how many songs have been scraped
    counter = 1

    # go through the list of songs url to get the request and write the link
    start_pos = int(raw_input('Which song should we start with? (string)'))
    for link in final_list[start_pos:]:
        file_name = link.split('/')[-1]
        r = requests.get(link).content
        with open('songs/{}.html'.format(file_name), 'w') as f:
            f.write(str(r))
        print "I printed out {}, song #{}".format(file_name, counter)
        counter += 1
