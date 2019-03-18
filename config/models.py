from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models import CASCADE
from django.template.loader import render_to_string


class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    ]
    title = models.CharField(verbose_name='标题', max_length=50)
    href = models.URLField(verbose_name='链接')
    status = models.PositiveIntegerField(verbose_name='状态', default=STATUS_NORMAL, choices=STATUS_ITEMS)
    weight = models.PositiveIntegerField(verbose_name='权重', default=1,
                                         choices=zip(range(1, 6), (1, 6)), help_text='权重高展示顺序靠前')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=CASCADE, db_index=True, db_constraint=False)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = '友链'


class SideBar(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL, '展示'),
        (STATUS_DELETE, '隐藏'),
    ]

    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT = 3
    DISPLAY_COMMENT = 4
    SIDE_TYPE = [
        (DISPLAY_HTML, 'HTML'),
        (DISPLAY_LATEST, '最新文章'),
        (DISPLAY_HOT, '最热文章'),
        (DISPLAY_COMMENT, '最近评论'),
    ]
    title = models.CharField(verbose_name='标题', max_length=50)
    display_type = models.PositiveIntegerField(verbose_name='展示类型', default=1, choices=SIDE_TYPE)
    content = models.CharField(verbose_name='内容', max_length=500, blank=True, help_text='如果设置的不是HTML，可为空')
    status = models.PositiveIntegerField(verbose_name='状态', default=STATUS_NORMAL, choices=STATUS_ITEMS)
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=CASCADE, db_index=True, db_constraint=False)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = '侧边栏'

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)

    @property
    def content_html(self):
        from blog.models import Post
        from comment.models import Comment

        result = ''
        if self.display_type == self.DISPLAY_HTML:
            result = self.content
        elif self.display_type == self.DISPLAY_LATEST:
            context = {
                'posts': Post.latest_posts()
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_HOT:
            context = {
                'posts': Post.hot_posts()
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_COMMENT:
            context = {
                'comments': Comment.objects.filter(status=Comment.STATUS_NORMAL)
            }
            result = render_to_string('config/blocks/sidebar_comments.html', context)
        return result
