from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from unidecode import unidecode
from datetime import datetime
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Category(models.Model):
    """文章分类"""
    name = models.CharField('分类名', max_length=30, unique=True)
    slug = models.SlugField('slug', max_length=40)
    parent_category = models.ForeignKey('self', verbose_name="父级分类", blank=True, null=True, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('blog:category_detail', args=[self.id])

    def has_child(self):
        if self.category_set.all().count() > 0:
            return True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            # Newly created object, so set slug
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = "分类"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """文章标签"""
    name = models.CharField('标签名', max_length=30, unique=True)
    slug = models.SlugField('slug', max_length=40)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            # Newly created object, so set slug
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:tag_detail', args=[self.id])

    def get_article_count(self):
        return Article.objects.filter(tags__id=self.id).count()

    class Meta:
        ordering = ['name']
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class Article(models.Model):
    """文章模型"""
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
    title = models.CharField('标题', max_length=200, unique=True)
    slug = models.SlugField('slug', max_length=60, blank=True)
    body = RichTextUploadingField('正文')
    pub_date = models.DateTimeField('发布时间', null=True)
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    mod_date = models.DateTimeField('修改时间', auto_now=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES, default='p')
    views = models.PositiveIntegerField('浏览量', default=0)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', verbose_name='分类', on_delete=models.CASCADE, blank=False, null=False)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)
    users_like = models.ManyToManyField(User,related_name='articles_liked', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            # Newly created object, so set slug
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if self.status == 'd' and self.pub_date is not None:
            self.pub_date = None
            # raise ValidationError('草稿没有发布日期. 发布日期已清空。')
        if self.status == 'p' and self.pub_date is None:
            self.pub_date = datetime.now()

    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[str(self.pk), self.slug])

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    def published(self):
        self.status = 'p'
        self.pub_date = datetime.now()
        self.save(update_fields=['status', 'pub_date'])

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "文章"
        verbose_name_plural = verbose_name
