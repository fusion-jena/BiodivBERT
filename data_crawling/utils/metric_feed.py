"""
Reads and Writes the necessary metrics of the documents
"""
# TODO: Remove duplicate lines of code
import logging
import os
import os.path
import sys
import pandas

import config

filename = 'Metric_Details_{}'.format(config.API)

log = logging.getLogger(__name__)


class MetricFeed:
    if not os.path.exists('Data'):
        os.makedirs('Data')

    def write_metrics(self, dir, filename, *args):
        """This method writes the metrics of the documents to a file
        :param args: data to write to a file"""
        if not os.path.exists(os.path.join(os.getcwd(), 'Data', dir)):
            os.makedirs(os.path.join(os.getcwd(), 'Data', dir))
        if len(args) == 1 and isinstance(args[0], str):
            try:
                completeName = os.path.join(os.getcwd(), 'Data', dir, filename+'.txt')
                text_file = open(completeName, "a+", encoding='utf-8')
                text_file.write(args[0] + '\n')
                text_file.close()
            except OSError:
                log.error("Could not open/read file")
                sys.exit()

        if len(args) == 1 and isinstance(args[0], pandas.DataFrame):
            try:
                completeName = os.path.join(os.getcwd(),'Data', dir, filename+'.csv')
                text_file = open(completeName, "w", encoding='utf-8')
                args[0].to_csv(text_file, columns=['dc:identifier', 'pii', 'dc:title'])
                text_file.close()

            except OSError:
                log.error("Could not open/read file")
                sys.exit()

    @staticmethod
    def get_metrics():
        """Returns the metric data stored in the Metric_Details.csv
        :return: the dataframe of the metrics"""
        try:
            metrics_file = open(os.path.join(os.getcwd(), 'Data', 'Metric_Details_Elsevier.csv'), 'r', encoding='utf-8')

        except OSError:
            log.error("Could not open/read file")
            sys.exit()
        with metrics_file:
            return pandas.read_csv(metrics_file)

    @staticmethod
    def write_data(my_data, save_to):
        """Write the data obtained"""
        try:
            completeName = save_to # save_to expected to have full path
            text_file = open(str(completeName), "w", encoding='utf-8')
            text_file.write(str(my_data))
            text_file.close()
        except OSError:
            log.error("Could not open/read file")
            sys.exit()
