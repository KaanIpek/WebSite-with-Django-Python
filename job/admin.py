from django.contrib import admin
from .models import Job,Comment
# Register your models here.
admin.site.register(Comment)
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display=["title","author","created_date"]
    list_display_links=["title","author"]
    search_fields=["title","author"]
    list_filter=["created_date"]
    class Meta:
        model = Job
        