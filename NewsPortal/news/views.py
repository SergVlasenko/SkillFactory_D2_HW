from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import PostFilter
from .models import Post, Category, PostCategory
from .forms import NewsForm, UserForm


# Представление для вывода всех постов
class NewsList(ListView):
    model = Post
    ordering = '-id'
    template_name = 'news.html'
    context_object_name = 'all_news'
    paginate_by = 10

    # Переопределяем функцию получения списка постов
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации
        # self.request.GET содержит объект QueryDict
        # Сохраняем фильтрацию в объекте класса, чтобы потом добавить в контекст и использовать в шаблоне
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список постов
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации
        context['filterset'] = self.filterset
        return context


# представление для просмотра поста/новости/статьи
class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post_detail'


# представление для создания поста/НОВОСТИ
class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        news_post = form.save(commit=False)
        news_post.postType = 'NW'
        return super().form_valid(form)


# представление для редактирования поста/НОВОСТИ
class NewsUpdate(PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.change_post',)


# представление для удаления поста/НОВОСТИ
class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


# представление для создания поста/СТАТЬИ
class ArticleCreate(PermissionRequiredMixin, CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        news_post = form.save(commit=False)
        news_post.postType = 'AR'
        return super().form_valid(form)


# представление для редактирования поста/СТАТЬИ
class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.change_post',)


# представление для удаления поста/СТАТЬИ
class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


# Представление для страницы с поиском постов
class SearchList(ListView):
    model = Post
    ordering = '-id'
    template_name = 'search.html'
    context_object_name = 'found_news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# представление для редактирования профиля User'а
class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserForm
    template_name = 'profile.html'
    success_url = 'news/'

    def get_object(self, **kwargs):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


# Функция-представление для апгрейда аккаунта до автора
@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/user')


# Представление для получения деталей категории
class CategoryDetailView(DetailView):
    template_name = 'category_detail.html'
    queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_links'] = PostCategory.objects.all()
        return context


# Функция-представление для подписки на категорию
@login_required
def subscribe_me(request, cat_id):
    Category.objects.get(pk=cat_id).subscribers.add(request.user)
    return redirect(f'/categories/{cat_id}/')


# Функция-представление для отписки от категории
@login_required
def unsubscribe_me(request, cat_id):
    Category.objects.get(pk=cat_id).subscribers.remove(request.user)
    return redirect(f'/categories/{cat_id}/')