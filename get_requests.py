import requests
from bs4 import BeautifulSoup


if __name__ == "__main__":
    final_list = []
    file_name = raw_input('File_name')
    with open(file_name, 'r') as final:
        for link in final:
            final_list.append(link.strip())
    counter = 1
    start_pos = int(raw_input('Which song should we start with? (string)'))
    for link in final_list[start_pos:]:
        file_name = link.split('/')[-1]
        r = requests.get(link).content
        with open('songs/{}.html'.format(file_name), 'w') as f:
            f.write(str(r))
        print "I printed out {}, song #{}".format(file_name, counter)
        counter += 1
