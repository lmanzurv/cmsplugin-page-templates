# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from django.template import Template
from django.utils.translation import ugettext_lazy as _
from cms.cache import invalidate_cms_page_cache

class PageTemplate(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='site_templates', db_index=True)
    name = models.CharField(max_length=255, verbose_name=_('Name'), db_index=True)
    template = models.TextField(verbose_name=_('HTML Template'), help_text=_('The template has to be compatible with Django\'s templating engine'))
    enabled = models.BooleanField(verbose_name=_('Enabled'), default=True)

    class Meta:
        verbose_name = _('Page Template')
        verbose_name_plural = _('Page Templates')
        unique_together = ('site', 'name')
        ordering = ('name',)

    def clean(self, *args, **kwargs):
        try:
            Template(self.template)
        except:
            raise ValidationError(_('Invalid HTML template format'), code='invalid')

    def save(self, *args, **kwargs):
        super(PageTemplate, self).save(*args, **kwargs)
        invalidate_cms_page_cache()

    def delete(self, *args, **kwargs):
        super(PageTemplate, self).delete(*args, **kwargs)
        invalidate_cms_page_cache()

    def get_template_html_name(self):
        return 'custom-template_%s_%s_%s.html' % (self.name.lower().replace(' ', '-'), self.pk, self.site.pk)

    def __unicode__(self):
        return self.name
