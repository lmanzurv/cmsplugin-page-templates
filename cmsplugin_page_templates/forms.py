# -*- coding: utf-8 -*-
from django import forms
from .models import PageTemplate
from django_ace_editor.widgets import AceEditorHTML

class PageTemplateForm(forms.ModelForm):
    class Meta:
        model = PageTemplate
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PageTemplateForm, self).__init__(*args, **kwargs)
        self.fields['template'].widget = AceEditorHTML()
