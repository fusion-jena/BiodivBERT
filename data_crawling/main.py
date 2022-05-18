import logging
from APIs.elsevier.elsevier_crawl import ElsCrawler
from APIs.springer.springer_crawl import SpringCrawler
import config

logging.basicConfig(filename='{}.log'.format(config.API), filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',)
logging.root.setLevel(logging.INFO)
logging.basicConfig()
logging.getLogger("pdfminer").setLevel(logging.WARNING)
logging.getLogger("elsapy").setLevel(logging.WARNING)

log = logging.getLogger(__name__)


def main():
    if config.Metric:
        for keyword in config.keywords:
            try:
                if config.API == "Springer":
                    my_crawler = SpringCrawler(keyword=keyword, years=config.years)
                else:
                    my_crawler = ElsCrawler(keyword=keyword)

                my_crawler.metric_search()
            except Exception as e:
                log.error('keyword:{} exception: {}'.format(keyword, str(e)))
                log.exception(e)
                continue

    elif config.Full:
        if config.API == "Springer":
            SpringCrawler.get_full_articles()
        else:
            ElsCrawler.get_full_articles()


if __name__ == '__main__':
    main()
