# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import EditSession


@admin.register(EditSession)
class EditSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'page', 'user', 'started_at', 'last_seen')
    list_filter = ('page', 'user', 'started_at', 'last_seen')
