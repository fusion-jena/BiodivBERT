"""Crawler for Springer that searches for the metrics of the
documents that contains the keywords and extracts the pdf,
finally generating a .txt file accordingly"""
import json
import logging
import os
import requests
from utils.metric_feed import MetricFeed
from ratelimit import limits, sleep_and_retry
import config
import uuid

# 150 calls per minute
CALLS = 150
ONE_MINUTE = 60

log = logging.getLogger(__name__)


def get_client():
    # Get configuration
    con_file = open("springer_config.json")
    config = json.load(con_file)
    con_file.close()
    return config['apikey']


@sleep_and_retry
@limits(calls=CALLS, period=ONE_MINUTE)
def callSpringerAPI(url):
    res = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'})
    if res.status_code != 200:
        raise Exception('API response: {}'.format(res.status_code))
    else:
        print(res.status_code)
    return res


@sleep_and_retry
@limits(calls=CALLS, period=ONE_MINUTE)
def getDocFromSpringer(url):
    headers = {
        "User-Agent": "PostmanRuntime/7.28.1",
        "Accept": "*/*",
        "Cache-Control": "no-cache",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "cache-control": "no-cache"}

    res = ""
    try:
        res = requests.get(url, stream=True, headers=headers)
        if res.status_code != 200:
            raise Exception('API response: {}'.format(res.status_code))
        else:
            print(res.status_code)
    except Exception as ex:
        print(ex)
    return res


class SpringCrawler:

    def __init__(self, keyword, years):
        self.keyword = keyword

        # how to add constraint: https://dev.springernature.com/adding-constraints
        year_query = ''
        for year in years:
            year_query += 'year: {}'.format(year)
            if year != years[-1]:
                year_query += ' OR '

        if keyword == '*omic diversity':
            keyword = '("taxonomic diversity" OR "genomic diversity")'
            self.query = '{} {}'.format(keyword, year_query)
        else:
            # this query uses one keyword and ORing the range of the selected years
            self.query = '"{}" {}'.format(keyword, year_query)

        if config.OPENACCESS:
            self.query = 'openaccess:true ' + self.query

    def metric_search(self):
        """Performs an iterative search until the resources are exhausted"""
        # I found the documentation uses that and I use that too

        # this code is based on https://dev.springernature.com/querystring-parameters

        base_url_springer = 'https://api.springernature.com/meta/v2/json'
        # base_url_springer = 'http://api.springernature.com/metadata/json'
        s = 1  # start of the search default and the minmum is 1
        p = 50  # number of results per page (default is 10 and this is the maximum)

        #  Begin exhaustive search
        while True:

            records_displayed = 0  # number of results that are actually available (cannot be more than page_length)
            params = {"q": self.query, "api_key": get_client(), "s": s, 'p': p}
            res = callSpringerAPI(base_url_springer + '?' + '&'.join(['{}={}'.format(k, v) for k, v in params.items()]))

            d_springer = res.json()
            result = d_springer['result']

            if s == 1:
                log.info('{}, {}'.format(result[0]['total'], self.query))

            # log.info('Starting from: {}'.format(s))

            #  Get the pointing values for every page for deeper query
            for i, dic in enumerate(result):
                page_length = int(dic['pageLength'])
                records_displayed = int(dic['recordsDisplayed'])
                s = s + page_length

            #  Search and store the URLs for PDFs for each documents
            for record in d_springer['records']:
                for url in record['url']:
                    if url['format'] != 'pdf':
                        continue
                    MetricFeed().write_metrics(config.API, self.keyword.replace('*', ''),
                                               record['doi'] + '|' + url['value'])

            if records_displayed < page_length:
                break

    @staticmethod
    def get_full_articles():
        target = 'Springer'
        target_dir = os.path.join(os.path.realpath('.'), 'Data', target)
        unique_dois_path = os.path.join(os.path.realpath('.'), 'Data', 'DOIs', '{}_unique_DOIs.txt'.format(target))
        proccessed_DOIs_path = os.path.join(os.path.realpath('.'), 'Data', 'Processed_Springer_DOIs.txt')
        PDFs_path = os.path.join(os.path.realpath('.'), 'Data', 'Springer_PDFs')

        if not os.path.exists(PDFs_path):
            os.makedirs(PDFs_path)

        # load DOIs and PDF URL to download
        my_dict = {}
        for filename in os.listdir(target_dir):
            with open(os.path.join(target_dir, filename), 'r', encoding='utf-8', errors='igonre') as file:
                lines = file.read().splitlines()
            for l in lines:
                parts = l.split('|')
                if len(parts) >= 2:
                    doi = parts[0]
                    url = parts[1]
                    my_dict.update({doi: url})

        # load unique DOIs
        with open(unique_dois_path, 'r') as file:
            unique_dois = file.read().splitlines()

        # load processed to be excluded
        processed_dois = []
        if os.path.exists(proccessed_DOIs_path):
            with open(proccessed_DOIs_path, 'r') as file:
                processed_dois = file.read().splitlines()

        remaining_dois = [i for i in unique_dois if i not in processed_dois]
        for i, doi in enumerate(remaining_dois):
            # this logic to prevent re-processing dois over multiple runs for any reason

            if i % 1000 == 0:
                log.info("downloaded {} / {}".format(i, len(remaining_dois)))

            # get url to download
            url = my_dict[doi]
            res = getDocFromSpringer(url)
            unique_filename = uuid.uuid4().hex
            download_filename = os.path.join(PDFs_path, '{}.pdf'.format(unique_filename))
            if res:
                with open(download_filename, 'wb') as outfile:
                    outfile.write(res.content)

                # add current doi to processed springer
                with open(proccessed_DOIs_path, 'a') as file:
                    file.write(doi + '\n')
                log.info("Success: DOI:{} downloaded at {}".format(doi, unique_filename))

            else:
                log.info("No PDF for DOI:{}".format(doi))
