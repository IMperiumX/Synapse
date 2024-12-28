# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import KnowledgeBase


@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'owner',
        'created_at',
        'updated_at',
        'is_public',
    )
    list_filter = ('owner', 'created_at', 'updated_at', 'is_public')
    search_fields = ('name',)
    date_hierarchy = 'created_at'
