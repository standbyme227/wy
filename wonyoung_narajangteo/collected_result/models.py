from django.db import models


# Create your models here.
class Keyword(models.Model):
    name = models.CharField(verbose_name="키워드명", max_length=100)
    is_active = models.BooleanField(default=True)

    created = models.DateField("생성 날짜", auto_now_add=True)
    updated = models.DateField("수정 날짜", auto_now=True)


class DailyKeyword(models.Model):
    keyword = models.ForeignKey(Keyword, verbose_name="키워드")
    announcement_cnt = models.IntegerField("공고 개수")
    is_active = models.BooleanField(default=True)

    created = models.DateField("생성 날짜", auto_now_add=True)
    updated = models.DateField("수정 날짜", auto_now=True)


class Announcement(models.Model):
    title = models.CharField(verbose_name="공고명", max_length=150)
    link = models.CharField(max_length=200)

    announce_date = models.DateField(verbose_name="공고일")
    wicket_date = models.DateField(verbose_name="개찰일")
    expired_date = models.DateField(verbose_name="마감일")

    is_active = models.BooleanField(default=True)

    created = models.DateField("생성 날짜", auto_now_add=True)
    updated = models.DateField("수정 날짜", auto_now=True)
