from datetime import datetime
import logging
import sys

a = None
b = None

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

def init(level=logging.INFO):
    logging.basicConfig(stream=sys.stdout,
                    filemode="w",
                    format=Log_Format,
                    level=level)
    # pass
log = logging.getLogger()

def start(method):
    global a
    a = datetime.now()
    log.info(('{0} started at {1}'.format(method, a)).encode('utf-8', errors='ignore'))


def stop(method):
    global b
    b = datetime.now()
    log.info(('{0} ended at: {1}'.format(method, b)).encode('utf-8', errors='ignore'))
    log.info(('{0} took: {1}'.format(method, b - a)).encode('utf-8', errors='ignore'))


def info(message):
    log.info(message.encode('utf-8', errors='ignore'))


def error(message):
    log.error(message.encode('utf-8', errors='ignore'))
