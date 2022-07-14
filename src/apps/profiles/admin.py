from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet

from profiles.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'deposit', 'get_role')
    list_filter = ('groups', )
    search_fields = ('username', )

    def get_queryset(self, request: WSGIRequest) -> QuerySet:
        qs = super().get_queryset(request)
        return qs.prefetch_related('groups')
