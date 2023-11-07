from datetime import datetime, timedelta
from pytz import timezone

tz = timezone('Asia/Kolkata')


def QuiteTime():
    start = datetime.now(tz).replace(hour=20, minute=0, second=0)
    print(start)
    mid = datetime.now(tz).replace(hour=7, minute=0, second=0)
    end = datetime.now(tz).replace(hour=7, minute=0, second=0) + timedelta(days=1)
    print(end)
    if datetime.now(tz) >= start:
        print(end)
        return end, True
    elif datetime.now(tz) <= mid:
        print(mid)
        return mid, True
    else:
        print(datetime.now(tz))
        return datetime.now(tz), False


# quite = QuiteTime()
# print(quite[1])
