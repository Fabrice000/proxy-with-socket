
import logging
import threading
from time import localtime, strftime


def log(self, log_level, client, msg):

    """ Log the messages to appropriate place """
    LoggerDict = {
    'CurrentTime' : strftime("%a, %d %b %Y %X", localtime()),
    'ThreadName' : threading.currentThread().getName()
    }
    if client == -1: # Main Thread
        formatedMSG = msg
    else: # Child threads or Request Threads
        formatedMSG = '{0}:{1} {2}'.format(client[0], client[1], msg)
    logging.debug('%s', colorizeLog(config['COLORED_LOGGING'],
    log_level, formatedMSG), extra=LoggerDict)