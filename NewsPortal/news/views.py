from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


# Create your views here.
class NewsList(ListView):
    model = Post
    ordering = '-id'
    template_name = 'news.html'
    context_object_name = 'all_news'


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post_detail'
