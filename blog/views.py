from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Article, Category, Tag
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ArticleForm, CategoryForm, TagForm
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def article_like(request):
    article_id = request.POST.get('id')
    action = request.POST.get('action')
    if article_id and action:
        try:
            article = Article.objects.get(id=article_id)
            if action == 'like':
                article.users_like.add(request.user)
            else:
                article.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'fail'})


@method_decorator(login_required, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/form.html'


@method_decorator(login_required, name='dispatch')
class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'blog/form.html'


# @method_decorator(login_required, name='dispatch')
class TagDetailView(DetailView):
    model = Tag


# @method_decorator(login_required, name='dispatch')
class TagListView(ListView):
    model = Tag


@method_decorator(login_required, name='dispatch')
class CategoryListView(ListView):
    model = Category


@method_decorator(login_required, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.has_child():
            articles = Article.objects.filter()
            categories = self.object.category_set.all()
            for category in categories:
                queryset = Article.objects.filter(category=category.id).order_by('-pub_date')
                articles.union(queryset)
        else:
            articles = Article.objects.filter(category=self.object.id).order_by('-pub_date')

        paginator = Paginator(articles, 3)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        context['page_obj'] = page_obj
        context['paginator'] = paginator
        context['is_paginated'] = True
        return context


@csrf_exempt
def article_search(request):
    q = request.GET.get('q', None)
    if q:
        article_list = Article.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
        context = {'article_list': article_list}
        return render(request, 'blog/article_search.html', context)

    return render(request, 'blog/article_search.html')


class ArticleListView(ListView):
    paginate_by = 3

    def get_queryset(self):
        return Article.objects.filter(status='p').order_by('-pub_date')


@method_decorator(login_required, name='dispatch')
class PublishedArticleListView(ListView):
    template_name = "blog/published_article_list.html"
    paginate_by = 3

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user).filter(status='p').order_by('-pub_date')


@method_decorator(login_required, name='dispatch')
class ArticleDraftListView(ListView):
    template_name = "blog/article_draft_list.html"
    paginate_by = 3

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user).filter(status='d').order_by('-pub_date')


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.viewed()
        return obj


@method_decorator(login_required, name='dispatch')
class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_create_form.html'

    # Associate form.instance.user with self.request.user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_update_form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404()
        return obj


@method_decorator(login_required, name='dispatch')
class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('blog:article_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404()
        return obj


@login_required()
def article_publish(request, pk, slug1):
    article = get_object_or_404(Article, pk=pk, author=request.user)
    article.published()
    return redirect(reverse("blog:article_detail", args=[str(pk), slug1]))
