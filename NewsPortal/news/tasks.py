from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
from datetime import timedelta, date
from celery import shared_task

# получаем список с адресами для рассылки
def get_subscribers(category):
    user_emails = []
    for user in category.subscribers.all():
        user_emails.append(user.email)
    return user_emails

# формирование и отправка письма
def send_emails(post_object, *args, **kwargs):
    html = render_to_string(
        kwargs['template'],
        {'category_object': kwargs['category_object'], 'post_object': post_object},
    )
    msg = EmailMultiAlternatives(
        subject=kwargs['email_subject'],
        from_email='test@yandex.ru',
        to=kwargs['user_emails']
    )
    msg.attach_alternative(html, 'text/html')
    msg.send()


# формирование еженедельной рассылки
@shared_task
def notify_subscribers_weekly():
    week = timedelta(days=7)
    posts = Post.objects.all()
    past_week_posts = []
    template = 'weekly_digest.html'
    email_subject = 'Еженедельный дайджест новостей'

    for post in posts:
        time_delta = date.today() - post.timeAdding.date()
        if (time_delta < week):
            past_week_posts.append(post)

    past_week_categories = set()
    for post in past_week_posts:

        for category in post.postCategory.all():
            past_week_categories.add(category)

    user_emails = set()
    for category in past_week_categories:
        get_user_emails = (set(get_subscribers(category)))
        user_emails.update(get_user_emails)

    for user_email in user_emails:
        post_object = []
        category_set = set()

        for post in past_week_posts:
            subscription = post.postCategory.all().values('subscribers').filter(subscribers__email=user_email)

            if subscription.exists():
                post_object.append(post)
                category_set.update(post.postCategory.filter(subscribers__email=user_email))
        print(user_email)
        category_object = list(category_set)
        print(category_object)

        send_emails(
            post_object,
            category_object=category_object,
            email_subject=email_subject,
            template=template,
            user_emails=[user_email, ])


#отправка уведомлений подписчикам категории при добавлении нового поста (вызывается через signals)
@shared_task
def notify_new_post_with_celery(post_pk):
    instance = Post.objects.get(pk=post_pk)
    subscribers_list = []
    # получаем категорИИ нового поста
    categories_current_post = instance.postCategory.all()

    # проходим все категории поста и всех подписчиков добавляем в список для отправки
    for category in categories_current_post:
        for user in category.subscribers.all():
            subscribers_list.append(user)

    # обработка отправки писем подписчикам в цикле для скрытия адреса получателя от других подписчиков
    for i in subscribers_list:
        user = i.username
        e_mail = i.email

        html_content = render_to_string('new_post_email.html',
                                        {'post': instance, }
                                        )
        msg = EmailMultiAlternatives(
            subject=f'Новый пост: {instance.title}',
            body=instance.text,
            from_email='test@yandex.ru',
            to=[e_mail],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()
