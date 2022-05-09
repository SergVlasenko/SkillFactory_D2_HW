from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.filter()
def censor(value):
    try:
        tmp_str = str(value)
        censor_dict = {
            'Редиска': 'Р......',
            'редиска': 'р......',
        }
        for i, j in censor_dict.items():
            tmp_str = tmp_str.replace(i, j)
        return tmp_str
    except:
        print('Ошибка!')


@register.filter(name='subscribed')
def subscribed(qs, user):
    try:
        qs.get(pk=user.id)
        return True
    except User.DoesNotExist:
        return False


@register.filter(name='by_category')
def by_category(post_cat_list, category_id):
    return post_cat_list.filter(categoryLink=category_id)
