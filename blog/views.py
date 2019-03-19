from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView, DetailView

from blog.models import Tag, Post, CateGory
from config.models import SideBar


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(CateGory.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(CateGory, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        query_set = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return query_set.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        query_set = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return query_set.filter(tag__id=tag_id)


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        query_set = super(SearchView, self).get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return query_set
        return query_set.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        query_set = super(AuthorView, self).get_queryset()
        author_id = self.kwargs.get('owner_id')
        return query_set.filter(owner_id=author_id)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


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
