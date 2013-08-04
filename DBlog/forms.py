#-*- coding:utf-8 -*-
'''
Created on 2013-8-4

@author: Administrator
'''
from django import forms

class BlogForm(forms.Form):
    caption = forms.CharField(label='title', max_length=100)
    content = forms.CharField(widget=forms.Textarea)

class TagForm(forms.Form):
    tag_name = forms.CharField()


