# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig

class PageTemplatesConfig(AppConfig):
    name = 'cmsplugin_page_templates'
    verbose_name = 'Page Templates'

    def ready(self):
        from cmsplugin_page_templates import signals
        try:
            from .models import PageTemplate
            templates = PageTemplate.objects.all()
            for template in templates:
                signals._create_template_file(template, False)
        except:
            # Initial migration hasn't happened. Ignore
            pass
