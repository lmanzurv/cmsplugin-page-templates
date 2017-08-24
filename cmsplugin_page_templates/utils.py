# -*- coding: utf-8 -*-
def get_name_from_filename(filename):
    template_name = ''
    if filename.startswith('custom-template') and filename.endswith('.html'):
        template_name = filename.split('_')[1].replace('-', ' ')
    return template_name

def get_cms_templates_list():
    from django.conf import settings
    import copy
    templates = copy.deepcopy(settings.BASE_CMS_TEMPLATES)

    # Fetch the templates list from the cache first
    from django.contrib.sites.models import Site
    from django.core.cache import cache
    from cms.cache import _get_cache_version
    from cms.utils import get_cms_setting

    site_id = Site.objects.get_current().pk
    version = _get_cache_version()
    custom_templates = cache.get('templ:%s' % (site_id), version=version)

    if custom_templates is None:
        custom_templates = dict()
        try:
            from .models import PageTemplate
            from django.contrib.sites.models import Site

            for template in PageTemplate.objects.only('id', 'name', 'site_id').filter(site_id=site_id, enabled=True):
                custom_templates[template.get_template_html_name()] = template.name.title()
        except:
            from .constants import TEMPLATE_DIR
            import os, warnings

            warnings.warn('Getting templates by looking in the template directory')

            for template in os.listdir(TEMPLATE_DIR):
                template_name = get_name_from_filename(template)
                if template_name:
                    custom_templates[template] = template_name.title()

        cache.set('templ:%s' % (site_id), custom_templates, get_cms_setting('CACHE_DURATIONS')['menus'], version=version)

    if not isinstance(custom_templates, long):
        templates.update(custom_templates)
    return templates
