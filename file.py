import datetime

import schedule


def job():
    now = datetime.datetime.now()
    hour = datetime.datetime.timetuple(now)[3]
    for i in hour:
        print('Ку')
    i += 1


schedule.every().hour.do(job)

while True:
    schedule.run_pending()
