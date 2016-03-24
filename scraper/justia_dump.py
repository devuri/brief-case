import requests
from bs4 import BeautifulSoup
import csv
import numpy as np
import sys
import time
import random

def case_url(year):
    url_prefix = 'https://supreme.justia.com/cases/federal/us/year/'

    url_suffix = '.html'

    return url_prefix + year + url_suffix


def get_cases(year):
    print "Getting case links for USSC %s" %year
    print

    resp = requests.get(case_url(year))

    case_links_soup = BeautifulSoup(resp.content, 'lxml')

    case_a_tags = case_links_soup.findAll('a', {'class': 'case-name'})

    case_links = ['https://supreme.justia.com' + a['href'] for a in case_a_tags]

    print "Case Links DOWNLOADED"
    print

    cases = []

    for link in case_links:
        print "Grabbing Case %d / %d" % (len(cases)+1, len(case_links))
        print
        resp = requests.get(link)
        cases.append([resp.content])

        csv_filename = '../data/' + str(year) + '_justia_html_dump.csv'

        print "Writing to file ..."
        print


    with open(csv_filename, 'a') as csvfile:
        justia_writer = csv.writer(csvfile, delimiter = '|')
        justia_writer.writerows(cases)

    print "DONE Dumping Justia Case HTMLs for USSC %s" %year
    print

if __name__ == '__main__':
    # get_cases(2015)
    # get_cases(sys.argv[1])
    for i in xrange(10):
        year = int(sys.argv[1])
        get_cases(str(year+i))
