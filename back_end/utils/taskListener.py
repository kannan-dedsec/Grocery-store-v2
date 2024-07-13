from celery.schedules import crontab
from datetime import datetime as dt
from utils.JobsPool import celery
from utils import DBUtil,mailUtil
import globalConstants as gc
import time
import os

@celery.task()
def sendMail(type,time):
    emails = DBUtil.getInactiveMails((gc.ONEDAY_IN_MILLIS) if type == "DAY" else (time * 60 * 1000) if type == "MINUTE" else None)
    for email in emails:
        timeline = "24 Hours" if type == "DAY" else f'{time} minute'
        mailUtil.sendEmail(email, gc.SUBJECT, gc.INACTIVITY_NOTIFICATION_TEMPLATE.substitute(timeline= timeline), None)

@celery.task()
def sendMonthlyReport():
    month = dt.now().strftime('%B')
    stats = DBUtil.getMonthlyUserStatistics()
    for email in list(stats.keys()):
        spent = stats[email]["amountSpent"]
        items = stats[email]["itemsBought"]
        totalSpent = stats[email]["totalAmountSpent"]
        totalBought = stats[email]["totalItemBought"]
        mailUtil.sendEmail(email, gc.SUBJECT, gc.REPORT_NOTIFICATION_TEMPLATE.substitute(month=month,spent=spent,items=items,totalSpent=totalSpent,totalBought=totalBought), None)

@celery.task()
def exportCsv(email, storeId, tmp, isAdmin):
    start_time = time.time()
    if isAdmin:
        filePath = DBUtil.exportProductStats(tmp)
    else:
        filePath = DBUtil.exportStoreProductStats(storeId,tmp)

    mailUtil.sendEmail(email, gc.SUBJECT,gc.EXPORT_NOTIFICATION_TEMPLATE.substitute(time=(time.time() - start_time)),filePath)
    os.remove(filePath)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    if(gc.INACTIVITY_EVERYDAY):
        sender.add_periodic_task(crontab(hour=gc.DAILY_REMAINDER_HOUR, minute=gc.DAILY_REMAINDER_HOUR_MINUTE),sendMail.s("DAY",None))
    elif(gc.INACTIVITY_MINUTE):
        sender.add_periodic_task(crontab(minute=f'*/{gc.DAILY_REMAINDER_MINUTE}'), sendMail.s("MINUTE",gc.DAILY_REMAINDER_MINUTE), name='Sending mail')

    if(gc.EVERY_MINUTE_REPORT):
        sender.add_periodic_task(crontab(minute=f'*/{gc.MONTHLY_REMAINDER_MINUTE}'),sendMonthlyReport.s())
    elif(gc.MONTHLY_REPORT):
        sender.add_periodic_task(crontab(0, 0, day_of_month=f'{gc.DAY_OF_THE_MONTH}'), sendMonthlyReport.s())


