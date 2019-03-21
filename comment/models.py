from django.db import models


# Create your models here.
from django.db.models import CASCADE

from blog.models import Post


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = [
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    ]
    # target = models.ForeignKey(Post, verbose_name='评论目标', on_delete=CASCADE)
    target = models.CharField(verbose_name='评论目标', max_length=100)
    content = models.CharField(verbose_name='内容', max_length=2000)
    nickname = models.CharField(verbose_name='昵称', max_length=50)
    website = models.URLField(verbose_name='网站')
    email = models.EmailField(verbose_name='邮箱')
    status = models.PositiveIntegerField(verbose_name='状态', default=STATUS_NORMAL, choices=STATUS_ITEMS)
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = '评论'

    @classmethod
    def get_by_target(cls, target):
        return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)
