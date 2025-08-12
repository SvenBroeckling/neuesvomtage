#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.contrib import admin

from base.models import Category, Feed, Entry, TopWord, TopWordLemma, TopWordLemmaWord


class FeedAdmin(admin.ModelAdmin):
    list_editable = ('sort', 'category', 'include_in_quiz', 'has_adblock_block', 'has_paywall', 'supports_lsr')
    list_display = (
        'title', 'category', 'sort',
        'include_in_quiz', 'last_update_at', 'last_update_status',
        'supports_lsr', 'has_adblock_block', 'has_paywall')
    list_filter = ('category', 'last_update_status')


class CategoryAdmin(admin.ModelAdmin):
    list_editable = ('sort',)
    list_display = ('name', 'sort')


class TopWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'count')


class TopWordLemmaWordInline(admin.TabularInline):
    model = TopWordLemmaWord


class TopWordLemmaAdmin(admin.ModelAdmin):
    inlines = [TopWordLemmaWordInline]
    list_display = 'lemma', 'words_string'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(TopWordLemma, TopWordLemmaAdmin)
admin.site.register(TopWord, TopWordAdmin)
admin.site.register(Entry)
