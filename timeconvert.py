from datetime import datetime, timedelta
import math


def getMinutesToShutdown(timeFromSnips):
    '''
    convert timestamp for execution time to minutes to go
    '''
    now = datetime.now()

    date = datetime.strptime(timeFromSnips.split(".")[0], "%Y-%m-%d %H:%M:%S")
    minutes =  math.ceil( (date -now)/ timedelta(minutes=1))
    if minutes > 0:
        return minutes
    else:
        return 0
