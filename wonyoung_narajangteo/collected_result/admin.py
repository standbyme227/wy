from django.contrib import admin
# Register your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe

from collected_result.models import Keyword, DailyKeywordResult, Announcement


class KeywordAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", "is_active"
    ]


class DailyKeywordResultAdmin(admin.ModelAdmin):
    list_display = [
        "id", "keyword", "announcement_cnt", "is_active",
        # "announcements"
    ]

    # def announcements(self, obj):
    #     base_url = reverse('admin:announcement')
    #     return mark_safe(u'<a href="%s?dk_result_id__exact=%d">Announcement</a>' % (
    #         base_url, obj.id))


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        "id", "title", "link", "date_text", "is_active"
    ]


admin.site.register(Keyword, KeywordAdmin)
admin.site.register(DailyKeywordResult, DailyKeywordResultAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
