#-*- coding:utf-8 -*-
from django.contrib.auth.views import login, logout
from django.conf.urls import patterns, include, url
from DBlog.view import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DBlog.views.home', name='home'),
    #url(r'^DBlog/', include('DBlog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^DBlog/$', current_time),
    url(r'^DBlog/list/$', blog_list, name='bloglist'),
    url(r'^DBlog/archive/(?P<id>\d+)/$', getBlogById, name='detailblog'),
    url(r'^DBlog/static/(?P<path>.*)/$', 'django.views.static.serve',
         {'doucument_root':'static'}),
    url(r'^DBlog/tag/(?P<id>\d+)/$', 'blog_filter', name='filtrblog'),
    url(r'^DBlog/add/$', 'DBlog.view.blog_add', name='addblog'),
    url(r'^DBlog/del/(?P<id>\d+)/$', 'DBlog.view.blog_delete', name='delblog'),
    url(r'^DBlog/edit/(?P<id>\d+)/$', 'DBlog.view.blog_edit', name='updateblog'),
    url(r'^DBlog/comments/', include('django.contrib.comments.urls')),
    url(r'^DBlog/(?P<id>\d+)/commentshow/$', 'blog_show_comment', name='showcomment'),
    
)
