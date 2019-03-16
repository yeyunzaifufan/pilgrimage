from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models import CASCADE


class CateGory(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    ]
    name = models.CharField(verbose_name='名称', max_length=50)
    status = models.PositiveIntegerField(verbose_name='状态', default=STATUS_NORMAL, choices=STATUS_ITEMS)
    is_nav = models.BooleanField(verbose_name='是否为导航', default=False)
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=CASCADE, db_index=True, db_constraint=False)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = '分类'


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    ]
    name = models.CharField(verbose_name='名称', max_length=50)
    status = models.PositiveIntegerField(verbose_name='状态', default=STATUS_NORMAL, choices=STATUS_ITEMS)
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=CASCADE, db_index=True, db_constraint=False)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = '标签'


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = [
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    ]
    title = models.CharField(verbose_name='标题', max_length=255)
    desc = models.CharField(verbose_name='摘要', max_length=1024, blank=True)
    content = models.TextField(verbose_name='正文', help_text='正文必须为MarkDown格式')
    status = models.PositiveIntegerField(verbose_name='状态', default=STATUS_NORMAL, choices=STATUS_ITEMS)
    category = models.ForeignKey(CateGory, verbose_name='分类', on_delete=CASCADE)
    tag = models.ForeignKey(Tag, verbose_name='标签', on_delete=CASCADE)
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=CASCADE, db_index=True, db_constraint=False)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']
