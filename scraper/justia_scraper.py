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


def get_references(case_a_tags):
    docket_nums = np.empty(len(case_a_tags), dtype='|S100')
    citations = np.empty(len(case_a_tags), dtype= '|S100')

    references = [a.findParent().text.split('\n')[3].lower() for a in case_a_tags]

    for i, r in enumerate(references):
        if 'docket' in r:
            docket_nums[i] = r.split(':')[-1].strip()
        else:
            docket_nums[i] = ''

        if 'citation' in r:
            citations[i] = r.split(':')[-1].strip()
        else:
            citations[i] = ''

    return docket_nums, citations


def get_cases(year):
    print "Getting case links for USSC %s" %year
    print

    resp = requests.get(case_url(year))
    case_links_soup = BeautifulSoup(resp.content, 'lxml')

    case_a_tags = case_links_soup.findAll('a', {'class': 'case-name'})

    case_links = ['https://supreme.justia.com' + a['href'] for a in case_a_tags]

    print "Case Links DOWNLOADED"
    print
    print "Grabbing Docket Numbers"

    docket_nums, citations = get_references(case_a_tags)

    print "Getting cases from %s" %year
    print

    cases = []

    for i, link in enumerate(case_links):

        print "Downloading case #%d" %(len(cases) + 1)

        # docket_no = link.split('/')[-2]

        syllabus_resp = requests.get(link)

        syllabus_soup = BeautifulSoup(syllabus_resp.content, 'lxml')


        # syllabus_div = syllabus_soup.find('div', {'id': 'opinion'})
        #
        # if 'NOTE:Where it is feasible' in syllabus_div.findAll('p')[0].text.encode('ascii', errors='ignore'):
        #     paragraphs = syllabus_div.findAll('p')[1:-1]
        # else:
        #     paragraphs = syllabus_div.findAll('p')[:-1]
        #
        # syllabus_text = '\n'.join([p.text for p in paragraphs]).encode('ascii', errors='ignore')

        try:
            summary = syllabus_soup.find('div', {'class': 'summary-collapsed', 'id': 'summary-text'}).text.encode('ascii', errors='ignore')
        except:
            summary = ''

        '''Find and prepare the opinion'''


        if syllabus_soup.select('#opinion > ul > li:nth-of-type(2) > a'):

            syllabus_div = syllabus_soup.find('div', {'id': 'opinion'})

            if 'NOTE:Where it is feasible' in syllabus_div.findAll('p')[0].text.encode('ascii', errors='ignore'):
                paragraphs = syllabus_div.findAll('p')[1:-1]
            else:
                paragraphs = syllabus_div.findAll('p')[:-1]

            syllabus_text = '\n'.join([p.text for p in paragraphs]).encode('ascii', errors='ignore')

            opinion_href = syllabus_soup.select('#opinion > ul > li:nth-of-type(2) > a')[0]['href']

            opinion_rsp = requests.get(link + opinion_href)

            opinion_soup = BeautifulSoup(opinion_rsp.content, 'lxml')

            opinion_div = opinion_soup.find('div', {'id': "opinion"})

            opinion_paragraphs = syllabus_div.findAll('p')

            if 'disclaimer' in opinion_paragraphs[-1].text.encode('ascii', errors='ignore').lower():
                opinion_paragrphas = opinion_paragraphs[:-2]

            opinion_text = '\n'.join([p.text for p in opinion_paragraphs]).encode('ascii', errors='ignore')

        else:
            '''
            If there is no syllabus, the selected tab in the middle of the page is the opinion.
            Just grab the opinion in this case.
            '''

            opinion_soup = syllabus_soup

            opinion_div = opinion_soup.find('div', {'id': "opinion"})

            opinion_paragraphs = opinion_div.findAll('p')

            if 'disclaimer' in opinion_paragraphs[-1].text.encode('ascii', errors='ignore').lower():
                opinion_paragrphas = opinion_paragraphs[:-2]

            opinion_text = '\n'.join([p.text for p in opinion_paragraphs]).encode('ascii', errors='ignore')

            syllabus_text = ''


        # case_soup.findAll('p', {'link.split('/')[-2]style': 'p-DateCode'})[0].text.encode('ascii', errors='ignore').split('.')[1].strip()

        if docket_nums[i] != '':
            print "Preparing Docket No. %s for CSV ..." %docket_nums[i]
            print

        if citations[i] != '':
            print "Preparing Citation: %s for CSV ..." %citations[i]
            print
    #
        cases.append({"docket_nums": docket_nums[i], "citations": citations[i], "opinions": opinion_text, "syllabuses": syllabus_text, "summaries": summary})

        # time.sleep(random.choice(xrange(7, 10)))

    csv_filename = '../data/' + str(year) + '_justia.csv'

    print "Writing to file ..."
    print

    with open(csv_filename, 'wb') as csvfile:
        # case_writer = csv.writer(csvfile, delimiter='|')
        justia_writer = csv.DictWriter(csvfile, fieldnames = ["docket_nums", "citations", "opinions", "syllabuses", "summaries"], delimiter = '|', extrasaction='ignore')
        justia_writer.writeheader()
        justia_writer.writerows(cases)

    print "DONE Scraping Justia for USSC %s" %year
    print


if __name__ == '__main__':
    # test_csv_filename = 'justia.csv'
    # test_cases = [{"docket_nums": 1, "citations": 'testing', "opinions": 'testing', "syllabuses": 'testing', "summaries": 'summary'}, {"docket_nums": 1, "citations": 'testing', "opinions": 'testing', "syllabuses": 'testing', "summaries": 'summary'}]

    # get_cases(2015)
    get_cases(sys.argv[1])

    # decade = int(sys.argv[1])
    #
    # for year in xrange(decade, (decade + 10)):
    #     get_cases(str(year))
    #     time.sleep(random.choice(xrange(10, 27)))
