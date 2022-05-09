from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def __str__(self):
        #return '{}'.format(self.authorUser)
        return f'{self.authorUser}'

    def update_rating(self):
        user = self.authorUser
        #определяем список всех постов автора
        post_list = Post.objects.filter(author=self)

        #вытаскиваем из списка постов рейтинг и считаем его сумму
        post_rating_list = post_list.values('rating')
        post_rating = sum(item['rating'] for item in post_rating_list)

        #определяем список со всеми комментариями автора и считаем их рейтинг
        comment_rating_list = Comment.objects.filter(commentUser=user).values('rating')
        comment_rating = 0
        comment_rating += sum(item['rating'] for item in comment_rating_list)

        #определяем рейтинг всех комментариев к статьям автора
        comment_in_post_rating = 0
        for post in post_list:
            comments_in_post = Comment.objects.filter(commentPost=post).values('rating')
            comment_in_post_rating += sum(item['rating'] for item in comments_in_post)

        #Считаем общий рейтинг автора
        self.ratingAuthor = post_rating * 3 + comment_rating + comment_in_post_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    timeAdding = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    postType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:123]}...'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostCategory(models.Model):
    postLink = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryLink = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timeAdding = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

