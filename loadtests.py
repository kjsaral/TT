#!/usr/bin/env python
import sys
import requests
from BeautifulSoup import BeautifulSoup


def get_participant_links(content):
    soup = BeautifulSoup(content)
    links = soup.findAll('a', {'class': 'participant-link'})
    return [link['href'] for link in links]


def main():
    NR = int(sys.argv[1])
    URL = sys.argv[2]
    for x in range(NR):
        print "Starting session %s, %s" % (str(x+1), URL)
        response = requests.get(URL)
        for i, link in enumerate(get_participant_links(response.content)):
            print "Starting participant %s, %s" % (str(i+1), link)
            requests.get(link)


if __name__ == '__main__':
    main()
