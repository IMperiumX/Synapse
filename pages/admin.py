# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Page, PageVersion, Attachment, PagePermission


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'space',
        'title',
        'content',
        'slug',
        'created_at',
        'updated_at',
        'created_by',
        'last_modified_by',
        'is_public',
    )
    list_filter = (
        'space',
        'created_at',
        'updated_at',
        'created_by',
        'last_modified_by',
        'is_public',
    )
    search_fields = ('slug',)
    date_hierarchy = 'created_at'


@admin.register(PageVersion)
class PageVersionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'page',
        'content',
        'version_number',
        'created_at',
        'created_by',
    )
    list_filter = ('page', 'created_at', 'created_by')
    date_hierarchy = 'created_at'


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'page', 'file', 'uploaded_by', 'uploaded_at')
    list_filter = ('page', 'uploaded_by', 'uploaded_at')


@admin.register(PagePermission)
class PagePermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'page', 'user', 'group', 'permission_level')
    list_filter = ('page', 'user', 'group')
