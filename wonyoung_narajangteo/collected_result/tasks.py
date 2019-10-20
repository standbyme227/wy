from celery.schedules import crontab
from config.celery import app

app.conf.beat_schedule = {
    'add-every-10-sec': {
        'task': 'collected_result.tasks.get_announcement',
        # 'schedule': 10.0,
        'schedule': crontab(hour=16, minute=32, day_of_week="0,1,2,3,4,5"),
    },
}


@app.task
def get_announcement():
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.support.ui import Select
    from collected_result.models import Keyword, DailyKeywordResult, Announcement
    from datetime import datetime
    from datetime import timedelta

    # driver = webdriver.Chrome('/Users/shsf/Projects/chromedriver')
    driver = webdriver.PhantomJS('/usr/local/bin/phantomjs')  # 맥 OS
    driver.implicitly_wait(5)

    driver.get("http://www.g2b.go.kr:8101/ep/tbid/tbidFwd.do")

    recordcountperpage = driver.find_element_by_name('recordCountPerPage')
    selector = Select(recordcountperpage)
    selector.select_by_value('100')

    # 입찰마감건 제외
    driver.find_element_by_xpath('//*[@id="exceptEnd"]').send_keys("Y")

    # 날짜
    # datetime = 0이 월요일
    now = datetime.today() + 1

    if now.weekday() == 0 or now.weekday() == 7:
        to_date_data = now - timedelta(2) - timedelta(hours=2) - timedelta(minutes=32)
        to_date = f'{to_date_data.year}/{to_date_data.month}/{to_date_data.day}'
        # to_date = f'{now.year}/{now.month}/{now.day}'
        from_date_data = now - timedelta(3) - timedelta(hours=2) - timedelta(minutes=32)
        # from_date_data = now - timedelta(3)
        from_date = f'{from_date_data.year}/{from_date_data.month}/{from_date_data.day}'

    else:
        # to_date_data = now - timedelta(hours=5) - timedelta(minutes=30)
        # to_date = f'{to_date_data.year}/{to_date_data.month}/{to_date_data.day}'
        to_date = f'{now.year}/{now.month}/{now.day}'
        # from_date_data = now - timedelta(1) - timedelta(hours=5) - timedelta(minutes=30)
        from_date_data = now - timedelta(1)
        from_date = f'{from_date_data.year}/{from_date_data.month}/{from_date_data.day}'

    # 키워드
    keywords = Keyword.objects.filter(is_active=True)
    for keyword in keywords:
        dk_result = DailyKeywordResult.objects.create(keyword=keyword, )
        driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[3]/form/table/tbody/tr[4]/td/div/div[4]/div[1]/input[1]'
        ).send_keys(from_date)
        driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div[3]/form/table/tbody/tr[4]/td/div/div[4]/div[1]/input[2]'
        ).send_keys(to_date)

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
            try:
                job = table.find('td').get_text()
            except AttributeError:
                continue
            # 공고명
            title_a = table.find(class_='tl')
            try:
                title = title_a.get_text()
            except AttributeError:
                continue

            try:
                title_link = title_a.find('a').get('href')
            except AttributeError:
                continue

            # 공고일 / 마감일
            try:
                date_text = table.find(class_='tc').get_text()
            except AttributeError:
                continue

            # 공고일이 from_date보다 작으면 continue(저장 X)
            convert_date = datetime.strptime(date_text[:16], '%Y/%m/%d %H:%M')

            if convert_date < from_date_data:
                continue
            try:
                a = Announcement.objects.filter(dk_result=dk_result, job=job, title=title, date_text=date_text)
            except TypeError:
                continue

            if not a:
                announcement, created = Announcement.objects.get_or_create(
                    dk_result=dk_result, title=title, link=title_link, date_text=date_text, job=job,
                )
                if not created:
                    continue
                dk_result.announcement_cnt += 1
                dk_result.save()
            else:
                continue
        driver.back()
