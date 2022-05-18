"""Crawler for Elsevier that searches for the metrics of the
documents that contains the keywords and searches the complete
document accordingly"""


# Used reference is https://dev.elsevier.com/tecdoc_sdsearch_migration.html

# All APIS: https://dev.elsevier.com/documentation/SUSHICOP5.wadl
# How to search: https://dev.elsevier.com/sd_article_meta_tips.html
# Search for Metadata: https://dev.elsevier.com/documentation/ArticleMetadataAPI.wadl
# Abstract Retrieval : https://dev.elsevier.com/documentation/AbstractRetrievalAPI.wadl
# Full article Retrieval: https://dev.elsevier.com/documentation/ArticleRetrievalAPI.wadl

import json
import logging
import math
import os
import sys
import uuid
import requests

from utils.metric_feed import MetricFeed
from ratelimit import limits, sleep_and_retry

import config

# 1 call per second
CALLS = 1
ONE_SECOND = 1

log = logging.getLogger(__name__)


@sleep_and_retry
@limits(calls=CALLS, period=ONE_SECOND)
def callElsevierAPI(url):
    headers = {'X-ELS-APIkey': get_client(), 'Accept': 'application/json'}
    print(url)
    print(headers)

    tries = 5
    for _ in range(tries):
        res = requests.get(url, headers=headers)
        if res.status_code == 429:  # overused API
            log.info('Over used API, sleep for 1 min and retry')
            log.info(res.headers)
            # time.sleep(60)  # sleep for 5 seconds
            # continue
            sys.exit(-1)
        else:
            if res.status_code != 200:
                raise Exception('API response: {}'.format(res.status_code))
            else:
                print(res.status_code)
        return res
    log.info('Failed 5 times, I am exiting ... ')
    sys.exit(-1)


@sleep_and_retry
@limits(calls=CALLS, period=ONE_SECOND)
def callElsevierAPI_put(url, params):
    headers = {'X-ELS-APIkey': get_client(), 'Accept': 'application/json'}
    print(url)
    print(headers)

    tries = 5
    for _ in range(tries):
        res = requests.put(url, json=params, headers=headers)
        if res.status_code == 429:  # overused API
            log.info('Over used API, sleep for 1 min and retry')
            log.info(res.headers)
            # time.sleep(60)  # sleep for 5 seconds
            # continue
            sys.exit(-1)
        else:
            if res.status_code != 200:
                raise Exception('API response: {}'.format(res.status_code))
            else:
                print(res.status_code)
        return res
    log.info('Failed 5 times, I am exiting ... ')
    sys.exit(-1)


def get_client():
    # Get configuration
    con_file = open("elsevier_config.json")
    config = json.load(con_file)
    con_file.close()
    return config['apikey']


def get_full_text(doi):
    full_text = None

    base_url = 'https://api.elsevier.com/content/article/doi/{}'.format(doi)
    try:
        res = callElsevierAPI(base_url)
        res_dict = res.json()
        full_text = res_dict['full-text-retrieval-response']['originalText']
    except Exception as e:
        log.error('Cannot fetch full-txt for doi {}. Exception {}'.format(doi, e))

    return full_text


class ElsCrawler:

    def __init__(self, keyword):
        self.keyword = keyword

        # for some reason, we couldn't use wild cards with elsevier
        if keyword == 'biodivers*':
            self.keyword = 'biodiversity'
        elif keyword == '*omic':
            self.keyword = 'taxonomic diversity OR \" genomic diversity\"'

    def metric_search(self):
        # This code is based on this article https://dev.elsevier.com/tecdoc_sdsearch_migration.html
        base_url = 'https://api.elsevier.com/content/search/sciencedirect'

        s = 0  # start of the search
        p = 100  # number of results per page

        #  Begin exhaustive search
        count = 1

        while True:
            page_length = p

            params = {'qs': self.keyword, 'date': config.Year_Range, 'start': s, 'count': p}

            # add pagination params valid offset 1-6000
            params.update({'display': {'offset': s, 'show': p}})

            if config.OPENACCESS:
                params.update({'filters': {'openAccess': True}})

            res = callElsevierAPI_put(base_url, params)

            d_elsevier = res.json()
            result = d_elsevier['results']
            total = d_elsevier['resultsFound']
            if total == 0:
                break
            max_call = math.ceil(int(total) / p)

            if s == 0:
                log.info('{}, {}, openAccess={}'.format(total, self.keyword, config.OPENACCESS))

            #  Get the pointing values for every page for deeper query
            s = s + page_length

            for item in result:
                try:
                    doi = item['doi']
                    MetricFeed().write_metrics(config.API, self.keyword.replace('*', ''), doi)
                except KeyError:  # skip empty dois
                    continue

            if count >= max_call:
                break
            elif s > 6000: # s cannot exceed 6000, hard limit by Elsevier (see: documentation)
                break

            count = count + 1

    @staticmethod
    def get_full_articles():
        target = 'Elsevier'
        unique_dois_path = os.path.join(os.path.realpath('.'), 'Data', 'DOIs', '{}_unique_DOIs.txt'.format(target))
        proccessed_DOIs_path = os.path.join(os.path.realpath('.'), 'Data', 'Processed_{}_DOIs.txt'.format(target))
        txts_path = os.path.join(os.path.realpath('.'), 'Data', '{}_full_txt'.format(target))

        if not os.path.exists(txts_path):
            os.makedirs(txts_path)

        # load unique DOIs to be downloaded from elsevier
        with open(unique_dois_path, 'r') as file:
            unique_dois = file.read().splitlines()

        # load processed to be excluded
        processed_dois = []
        if os.path.exists(proccessed_DOIs_path):
            with open(proccessed_DOIs_path, 'r') as file:
                processed_dois = file.read().splitlines()

        remaining_dois = [i for i in unique_dois if i not in processed_dois]
        for i, doi in enumerate(remaining_dois):
            # get url to download
            res = get_full_text(doi)
            if res:
                # save obtained txt
                unique_filename = uuid.uuid4().hex
                txt_file_path = os.path.join(txts_path, '{}.txt'.format(unique_filename))
                with open(txt_file_path, 'w', encoding='utf-8', errors='ignore') as file:
                    file.write(res)

                # add current doi to processed springer
                with open(proccessed_DOIs_path, 'a') as file:
                    file.write(doi + '\n')
                log.info("Success: DOI:{} downloaded at {}".format(doi, unique_filename))


            else:
                log.info("No full-txt for DOI:{}".format(doi))
