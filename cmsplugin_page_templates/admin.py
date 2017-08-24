# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import PageTemplate
from .forms import PageTemplateForm

class PageTemplateAdmin(admin.ModelAdmin):
    form = PageTemplateForm
    list_display = ('name', 'site_name', 'html_name', 'enabled')
    list_filter = ('name', 'site__name', 'enabled')
    ordering = ('name',)

    def site_name(self, obj):
        return obj.site.name

    def html_name(self, obj):
        return obj.get_template_html_name()

admin.site.register(PageTemplate, PageTemplateAdmin)
