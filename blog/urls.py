from django.urls import path, re_path
from . import views


# namespace
app_name = 'blog'

urlpatterns = [
    # 所有文章列表 - 不需登录
    path('', views.ArticleListView.as_view(), name='article_list'),
    # 展示文章详情 - 登录/未登录均可
    re_path(r'^article/(?P<pk>\d+)/(?P<slug1>[-\w]+)/$', views.ArticleDetailView.as_view(), name='article_detail'),
    # 草稿箱 - 需要登录
    path('draft/', views.ArticleDraftListView.as_view(), name='article_draft_list'),
    # 已发表文章列表(含编辑) - 需要登录
    path('admin/', views.PublishedArticleListView.as_view(), name='published_article_list'),
    # 更新文章- 需要登录
    re_path(r'^article/(?P<pk>\d+)/(?P<slug1>[-\w]+)/update/$', views.ArticleUpdateView.as_view(), name='article_update'),
    # 创建文章 - 需要登录
    re_path(r'^article/create/$', views.ArticleCreateView.as_view(), name='article_create'),
    # 发表文章 - 需要登录
    re_path(r'^article/(?P<pk>\d+)/(?P<slug1>[-\w]+)/publish/$', views.article_publish, name='article_publish'),
    # 删除文章 - 需要登录
    re_path(r'^article/(?P<pk>\d+)/(?P<slug1>[-\w]+)/delete$', views.ArticleDeleteView.as_view(), name='article_delete'),
    # 展示类别列表
    re_path(r'^category/$', views.CategoryListView.as_view(), name='category_list'),
    # 展示类别详情
    re_path(r'^category/(?P<pk>\d+)/$', views.CategoryDetailView.as_view(), name='category_detail'),
    # 展示Tag详情
    re_path(r'^tags/(?P<pk>\d+)/$', views.TagDetailView.as_view(), name='tag_detail'),
    # path('tags/<slug>/', views.tag_detail, name='tag_detail'),
    # 搜索文章
    re_path(r'^search/$', views.article_search, name='article_search'),
    # 创建类别详情
    re_path(r'^category/create/$', views.CategoryCreateView.as_view(), name='category_create'),
    # 创建Tag详情
    re_path(r'^tags/create/$', views.TagCreateView.as_view(), name='tag_create'),
    # 展示Tag列表
    re_path(r'^tags/$', views.TagListView.as_view(), name='tag_list'),
    # 点赞
    re_path(r'^article/like/$', views.article_like, name='article_like'),
]

