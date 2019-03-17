from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from blog.models import Tag, Post, CateGory
from config.models import SideBar


def post_list(request, category_id=None, tag_id=None):
    # content = 'post_list category_id={category_id}, tag_id={tag_id}'.format(category_id=category_id, tag_id=tag_id)
    # return HttpResponse(content)
    # return render(request, 'blog/list.html', context={'name': 'post_list'})
    category = None
    tag = None
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()
    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SideBar.get_all()
    }
    context.update(CateGory.get_navs())
    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
    # return HttpResponse('detail')
    # return render(request, 'blog/detail.html', context={'name': 'post_detail'})
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        post = None
    context = {
        'post': post,
        'sidebars': SideBar.get_all()
    }
    context.update(CateGory.get_navs())
    return render(request, 'blog/detail.html', context=context)
