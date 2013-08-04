#-*- coding:utf-8 -*-
'''
Created on 2013-8-3

@author: Administrator
'''
from django.template import Template,Context,RequestContext
from django.http import HttpResponse,Http404,HttpResponseRedirect
import datetime

from django.shortcuts import render_to_response
from DBlog.models import Blog,Tag,Author
from DBlog.forms import BlogForm,TagForm

def current_time(request):
    current_date = datetime.datetime.now()
    t=Template("<html><body>it is now {{current_date}}</body></html>")
    htm=t.render(RequestContext(request,locals()))
    return HttpResponse(htm)

def blog_list(request):
    '''list'''
    blogs=Blog.objects.all()
    return render_to_response('myblog.html',locals())

def getBlogById(request,id=''):
    try:
        blog=Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        raise Http404
    return render_to_response('archive.html',locals())

def blog_filter(request,id=''):
    tags = Tag.objects.all()
    tag = Tag.objects.get(id=id)
    blogs = tag.blog_set.all()
    return render_to_response('blog_filter.html',locals())

def blog_add(request):
    if request.method=="POST":
        form=BlogForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            title=cd['caption']
            content=cd['content']
            author = Author.objects.get(id=1)
            blog = Blog(caption=title, author=author, content=content)
            blog.save()
            #保存成功跳转到新增页面
            id = Blog.objects.order_by('-publish_time')[0].id
            return HttpResponseRedirect('/DBlog/archive/%s' % id)
    else:
        form=BlogForm()
    return render_to_response('blog_add.html',{'form': form}, context_instance=RequestContext(request))

def blog_delete(request,id=''):
    try:
        blog=Blog.objects.get(id=id)        
    except Blog.DoesNotExist:
        raise Http404
    #删除成功跳转到新增页面
    if blog:
        blog.delete()
        return HttpResponseRedirect('/DBlog/list/')
    blogs=Blog.objects.all()
    return render_to_response('myblog.html',locals())

def blog_edit(request,id=''):
    id = id
    if request.method == 'POST':
        form = BlogForm(request.POST)
        tag = TagForm(request.POST)
        if form.is_valid() and tag.is_valid():
            cd = form.cleaned_data
            cdtag = tag.cleaned_data
            tagname = cdtag['tag_name']
            tagnamelist = tagname.split()
            for taglist in tagnamelist:
                Tag.objects.get_or_create(tag_name=taglist.strip())
            title = cd['caption']
            content = cd['content']
            blog = Blog.objects.get(id=id)
            if blog:
                blog.caption = title
                blog.content = content
                blog.save()
                for taglist in tagnamelist:
                    blog.tags.add(Tag.objects.get(tag_name=taglist.strip()))
                    blog.save()
                tags = blog.tags.all()
                for tagname in tags:
                    tagname = unicode(str(tagname), "utf-8")
                    if tagname not in tagnamelist:
                        notag = blog.tags.get(tag_name=tagname)
                        blog.tags.remove(notag)
            else:
                blog = Blog(caption=blog.caption, content=blog.content)
                blog.save()
            return HttpResponseRedirect('/DBlog/archive/%s' % id)
    else:
        try:
            blog = Blog.objects.get(id=id)
        except Exception:
            raise Http404
        form = BlogForm(initial={'caption': blog.caption, 'content': blog.content}, auto_id=False)
        tags = blog.tags.all()
        if tags:
            taginit = ''
            for x in tags:
                taginit += str(x) + ' '
            tag = TagForm(initial={'tag_name': taginit})
        else:
            tag = TagForm()
    return render_to_response('blog_add.html',
        {'blog': blog, 'form': form, 'id': id, 'tag': tag},
        context_instance=RequestContext(request))
    