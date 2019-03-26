from datetime import datetime, timedelta
import math


def getMinutesToShutdown(timeFromSnips):
    now = datetime.now()

    date = datetime.strptime(timeFromSnips.split(".")[0], "%Y-%m-%d %H:%M:%S")
    minutes =  math.ceil( (date -now)/ timedelta(minutes=1))
    if minutes > 0:
        return minutes
    else:
        return 0
    

if __name__ == "__main__":
    str = "2019-03-25 23:19:17.468730442 +00:00"

    miuntes  = getMinutesToShutdown(str)
    print(miuntes)
