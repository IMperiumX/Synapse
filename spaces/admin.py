# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Space, SpacePermission


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'knowledge_base',
        'name',
        'description',
        'parent_space',
        'created_at',
        'updated_at',
        'is_public',
    )
    list_filter = (
        'knowledge_base',
        'parent_space',
        'created_at',
        'updated_at',
        'is_public',
    )
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(SpacePermission)
class SpacePermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'space', 'user', 'group', 'permission_level')
    list_filter = ('space', 'user', 'group')
