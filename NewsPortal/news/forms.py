from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm


from .models import Post


class NewsForm(forms.ModelForm):
    title = forms.CharField(max_length=128)

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'text',
            'postCategory',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        if text is None:
            raise ValidationError('Текст не должен быть пустым')

        return cleaned_data


#Форма для редактирования профиля пользователя
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        #fields = '__all__'
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


#Скрипт для кастомизации формы SignupForm из пакета allauth
#Автоматическое добавление нового пользователя в группу 'commom'
class CommonSignUpForm(SignupForm):

    def save(self, request):
        user = super(CommonSignUpForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
