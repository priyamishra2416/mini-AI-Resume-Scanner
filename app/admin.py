from django.contrib import admin
from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'role',
        'score',
        'uploaded_at'
    )

    search_fields = (
        'name',
        'role'
    )

    list_filter = (
        'role',
        'uploaded_at'
    )