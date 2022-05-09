from django.urls import path
from .views import NewsList, PostDetail, NewsCreate, NewsUpdate, NewsDelete, ArticleCreate, ArticleUpdate, \
    ArticleDelete, SearchList, UserUpdateView, upgrade_me, CategoryDetailView, subscribe_me, unsubscribe_me

urlpatterns = [
    path('news/', NewsList.as_view(), name='news_list'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('news/search', SearchList.as_view(), name='found_list'),
    path('user', UserUpdateView.as_view(), name='user_update'),
    path('upgrade/', upgrade_me, name='upgrade'),

    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('subscribe/<int:cat_id>', subscribe_me, name='subscribe'),
    path('unsubscribe/<int:cat_id>', unsubscribe_me, name='unsubscribe'),
]
