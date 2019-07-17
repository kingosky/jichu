from django import forms
from .models import Article, Category, Tag
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['author', 'views', 'slug', 'pub_date', 'users_like', 'create_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': CKEditorUploadingWidget(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'multi-checkbox'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('slug', 'parent_category')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude = ('slug',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
