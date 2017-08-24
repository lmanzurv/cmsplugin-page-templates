# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.loaders.cached import Loader as BaseLoader
from cms.cache import _get_cache_version, invalidate_cms_page_cache

class Loader(BaseLoader):
    """
    Wrapper class that takes a list of template loaders as an argument and attempts
    to load templates from them in order, caching the result.
    """

    def __init__(self, engine, loaders):
        self.cached_templates = {}
        super(Loader, self).__init__(engine, loaders)

    def cache_key(self, template_name, template_dirs, skip=None):
        key = super(Loader, self).cache_key(template_name, template_dirs, skip)
        if template_name.startswith(settings.PAGE_TEMP_MEMCACHED):
            new_key = key + '-' + str(_get_cache_version())
            if key in self.cached_templates:
                old_key = self.cached_templates[key]
                if old_key != new_key:
                    del self.get_template_cache[old_key]

            self.cached_templates[key] = new_key
            key = new_key
        return key

    def reset(self):
        'Empty the template cache.'
        invalidate_cms_page_cache()
        self.cached_templates.clear()
        super(Loader, self).reset()
