# -*- coding: utf-8 -*-
from cms.constants import TEMPLATE_INHERITANCE_MAGIC
from cms.models.pagemodel import Page
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PageTemplate
from .constants import TEMPLATE_DIR
import os

@receiver(post_save, sender=PageTemplate)
def generate_template(sender, instance, created, **kwargs):
    _create_template_file(instance, created)

def _create_template_file(page_template, new):
    template_name = page_template.get_template_html_name()
    filename = os.path.join(TEMPLATE_DIR, template_name)

    if (not new or not page_template.enabled) and os.path.exists(filename):
        os.remove(filename)

    if page_template.enabled:
        f = open(filename, 'w+')
        f.write(page_template.template)
        f.close()
    else:
        Page.objects.filter(template=template_name).update(template=TEMPLATE_INHERITANCE_MAGIC)


@receiver(post_delete, sender=PageTemplate)
def remove_template(sender, instance, **kwargs):
    template_name = instance.get_template_html_name()
    Page.objects.filter(template=template_name).update(template=TEMPLATE_INHERITANCE_MAGIC)

    filename = os.path.join(TEMPLATE_DIR, template_name)
    if os.path.exists(filename):
        os.remove(filename)
