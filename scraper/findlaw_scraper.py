import requests
from bs4 import BeautifulSoup
import csv
import sys
import time
import random

def build_summary_urls(year_month, pg_num):
    '''
    Returns the full url with params for month, year, and page.

    Inputs:

        year_month - year and month of the court cases

        pg_num - page number aka pagination

    Outputs:

        full_url - full url string to access each case summary page by month, year, and pagination
    '''
    prefix = "http://caselaw.findlaw.com/summary/court/us-supreme-court/"

    param_str = "/?query=filters&court=us-supreme-court&dateFormat=yyyyMM&pubDate="

    full_url = prefix + str(year_month) + param_str + str(year_month) + '&pgnum=' + str(pg_num)

    return full_url


def get_summary_links(year):
    print
    print "Getting Summary Links ..."
    print

    year_month_start = int(year) * 100 + 01
    year_month_end = int(year) * 100 + 13

    # import ipdb; ipdb.set_trace()


    summary_links = []

    while year_month_start < year_month_end:


        pg_num = 1
        found_links = [None]

        while len(found_links) > 0:

            summary_resp = requests.get(build_summary_urls(year_month_start, pg_num))

            summary_soup = BeautifulSoup(summary_resp.content, 'lxml')

            page_links = summary_soup.findAll('a')

            found_links = [link['href'] for link in page_links if link.parent.parent.name == 'td']

            summary_links += found_links

            print "Cases Found for %s-%s: %d" %( str(year_month_start)[-2:], str(year_month_start)[:-2], len(found_links))
            print

            pg_num += 1

        year_month_start += 1


    #
    # print "::Case Summary Links::"

    # for link in summary_links:
    #     print link
    #
    # print
    # print "================"
    # print

    print "Summary Links DOWNLOADED"
    print

    return summary_links


def scrape_summaries(year):
    summary_links = get_summary_links(year)

    print "Scraping Summaries for %s ..." %year
    print

    summaries = []

    for link in summary_links:

        print "Downloading Summary #%d From %s" %((len(summaries) +1), year)

        resp = requests.get(link)
        soup = BeautifulSoup(resp.content, 'lxml')

        # heading = soup.get('#leftcol-module > div > div > div.baseIncluder.section.summary_content > div.caselawcontent.searchable-content > center > h3')

        heading = soup.find('h3').text.encode("UTF-8")

        docket_no = heading.split(',').pop().strip()

        # body = soup.get('#leftcol-module > div > div > div.baseIncluder.section.summary_content > div.caselawcontent.searchable-content > p')

        body = soup.findAll('p')[-1].text.encode("UTF-8")

        # print "%s - %s" %(heading, docket_no)
        # print '============================='
        # print body

        summaries.append([heading, docket_no, body])

        print "Preparing Docket No.%s for CSV" %docket_no
        print

        time.sleep(random.choice(xrange(3,7)))

    file_name = '../data/' + year + '_findlaw_summaries.csv'

    with open(file_name, 'wb') as csvfile:
        summary_writer = csv.writer(csvfile, delimiter='|')
        summary_writer.writerows(summaries)

    print "DONE Scraping Findlaw USSC Year:", sys.argv[1]

if __name__ == '__main__':
    # scrape_summaries('2015')
    scrape_summaries(sys.argv[1])
