from __future__ import absolute_import, unicode_literals

import os

from bs4 import BeautifulSoup
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from collected_result.models import Keyword, DailyKeywordResult, Announcement

from datetime import datetime
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=15, minute=52, day_of_week='1-5'),
        get_announcement(),
    )


@app.task
def get_announcement():
    # driver = webdriver.Chrome('/Users/shsf/Projects/chromedriver')
    driver = webdriver.PhantomJS('/usr/local/bin/phantomjs')  # 맥 OS
    driver.get("http://www.g2b.go.kr:8101/ep/tbid/tbidFwd.do")

    recordcountperpage = driver.find_element_by_name('recordCountPerPage')
    selector = Select(recordcountperpage)
    selector.select_by_value('100')

    # 입찰마감건 제외
    driver.find_element_by_xpath('//*[@id="exceptEnd"]').send_keys("Y")

    # 날짜
    now = datetime.today()

    if now.weekday() == 0:
        to_date = f'{now.year}/{now.month}/{now.day}'
        from_date = date.today() - timedelta(3)
    else:
        to_date = f'{now.year}/{now.month}/{now.day}'
        from_date = date.today() - timedelta(1)

    driver.find_element_by_xpath('//*[@id="fromBidDt"]').send_keys(from_date)
    driver.find_element_by_xpath('//*[@id="toBidDt"]').send_keys(to_date)

    # 키워드
    keywords = Keyword.objects.filter(is_active=True).values_list("name", flat=True)
    for keyword in keywords:
        dk_result = DailyKeywordResult.objects.create(keyword=keyword, )

        # 키워드 지정
        driver.find_element_by_xpath('//*[@id="bidNm"]').send_keys(keyword.name)

        # 검색버튼 및 클릭
        search_button = driver.find_element_by_class_name('btn_mdl')
        search_button.click()

        # Soup화
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        table_area = soup.find('tbody').find_all('tr')

        for table in table_area:
            # 공고명
            title = table.find(class_='tl').get_text()

            # 공고일 / 마감일
            date_text = table_area.find(class_='tc').get_text()

            a = Announcement.filter(dk_result=dk_result, title=title, date_text=date_text)
            if not a:
                Announcement.objects.create(dk_result=dk_result, title=title, date_text=date_text)
                dk_result.announcement_cnt += 1
                dk_result.save()
            else:
                continue
        driver.back()

