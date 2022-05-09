from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post, Category, PostCategory


#Отправка уведомлений подписчикам (по категори поста) при создании нового поста
@receiver(m2m_changed, sender=PostCategory)
def notify_new_post(sender, instance, **kwargs):
    subscribers_list = []
    # получаем категорИИ нового поста
    categories_current_post = instance.postCategory.all()

    #проходим все категории поста и всех подписчиков добавляем в список для отправки
    for category in categories_current_post:
        for user in category.subscribers.all():
            subscribers_list.append(user)

    #обработка отправки писем подписчикам в цикле для скрытия адреса получателя от других подписчиков
    for i in subscribers_list:
        user = i.username
        e_mail = i.email

        html_content = render_to_string('new_post_email.html',
                                        {'post': instance, }
                                        )
        msg = EmailMultiAlternatives(
            subject=f'Новый пост: {instance.title}',
            body=instance.text,
            from_email='79607725595@yandex.ru',
            to=[e_mail],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()
