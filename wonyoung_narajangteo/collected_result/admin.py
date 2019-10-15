from django.contrib import admin
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from collected_result.models import Keyword, DailyKeywordResult, Announcement


# Register your models here.


class KeywordAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", "is_active"
    ]


class DailyKeywordResultAdmin(admin.ModelAdmin):
    list_display = [
        "id", "keyword", "announcement_cnt", "is_active", "created",
        "announcements"
    ]

    # def link(self, instance):
    #     url = reverse("admin:dailykeywordresult_changelist", args=(instance.id,))
    #     return mark_safe("<a href='%s'>%s</a>" % (url, unicode(instance)))
    def announcements(self, obj):
        base_url = reverse('admin:collected_result_announcement_changelist')
        return mark_safe(u'<a href="%s?dk_result_id__exact=%d">Daily Announcements</a>' % (
            base_url, obj.id))


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        "id", "title", "show_link", "date_text", "is_active", "dk_result"
    ]

    # list_filter = ("dk_result__id",)
    # def changelist_view(self, request, *args, **kwargs):
    #     self.request = request
    #     dk_result_id = request.query_params.get("dk_result__id")
    #     if dk_result_id:
    #         dk_result = DailyKeywordResult.objects.filter(id=dk_result_id)
    #         dk_result.is_active = False
    #         dk_result.save()
    #     else:
    #         pass
    #
    #     return super().changelist_view(request, *args, **kwargs)
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()

        try:
            dk_result_id = int(request.GET["dk_result_id__exact"][0])
        except MultiValueDictKeyError:
            return queryset
        if dk_result_id:
            dk_result = DailyKeywordResult.objects.filter(id=dk_result_id).first()
            dk_result.is_active = False
            dk_result.save()
            return queryset
        else:
            return queryset

    def show_link(self, obj):
        return format_html('<a href="%s" target="_blank">%s</a>' % (obj.link, obj.link))
    show_link.allow_tags = True

admin.site.register(Keyword, KeywordAdmin)
admin.site.register(DailyKeywordResult, DailyKeywordResultAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
