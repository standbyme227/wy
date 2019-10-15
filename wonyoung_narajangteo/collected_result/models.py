from django.db import models

from django.template.defaultfilters import escape


# TODO 공고일 (개찰일) 마감일을 date롤 넣어서 처리
# 시간이 지난건 False


# Create your models here.
from django.urls import reverse


class Keyword(models.Model):
    name = models.CharField(verbose_name="키워드명", max_length=100, unique=True)
    # link = models.TextField(verbose_name="검색링크", blank=True)
    is_active = models.BooleanField(default=True)

    created = models.DateField("생성 날짜", auto_now_add=True)
    updated = models.DateField("수정 날짜", auto_now=True)

    def __str__(self):
        return f"{self.name}"


class DailyKeywordResult(models.Model):
    keyword = models.ForeignKey(Keyword, verbose_name="키워드", on_delete=models.CASCADE)
    announcement_cnt = models.IntegerField("공고 개수", default=0)
    is_active = models.BooleanField(default=True)

    created = models.DateField("생성 날짜", auto_now_add=True)
    updated = models.DateField("수정 날짜", auto_now=True)

    def __str__(self):
        return f"{self.created}, {self.keyword}"

    # def announce_link(self):
    #     return '<a href="%s">%s</a>' % (reverse("admin:announcement", args=(self.user.id,)), escape(self.user))
    #
    # announce_link.allow_tags = True
    # announce_link.short_description = "User"

class Announcement(models.Model):
    dk_result = models.ForeignKey(DailyKeywordResult, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="공고명", max_length=150)
    link = models.CharField(verbose_name='공고링크', max_length=200)

    date_text = models.CharField("공고일(마감일)", max_length=100)

    # announce_date = models.DateField(verbose_name="공고일")
    # wicket_date = models.DateField(verbose_name="개찰일")
    # expired_date = models.DateField(verbose_name="마감일")

    is_active = models.BooleanField(default=True)

    created = models.DateField("생성 날짜", auto_now_add=True)
    updated = models.DateField("수정 날짜", auto_now=True)
