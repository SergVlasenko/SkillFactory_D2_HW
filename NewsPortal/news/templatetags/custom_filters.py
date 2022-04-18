from django import template

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
