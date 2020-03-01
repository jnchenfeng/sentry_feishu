# coding: utf-8

from django import forms


class FeiShuOptionsForm(forms.Form):
    access_token = forms.CharField(
        max_length=255,
        help_text='Feishu robot access_token'
    )
