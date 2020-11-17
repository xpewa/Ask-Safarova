from django import forms

def css_classes(form):
    for field in form:
        if isinstance(field.field.widget, (forms.TextInput, forms.PasswordInput, forms.Textarea, forms.EmailInput)):
            field.field.widget.attrs['class'] = 'form-control'

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=6, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, max_length=40, label='Пароль')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        css_classes(self)

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=20, label='Логин',
                               help_text='Логин меньше 20 символов, и состоит из латинских символов.')
    email = forms.EmailField(label='E-mail')
    nick_name = forms.CharField(max_length=20, label='Никнейм',
                                help_text='Никнейм меньше 20 символов.')
    password = forms.CharField(widget=forms.PasswordInput, max_length=40, min_length=6, label='Пароль',
                               help_text='Пароль не меньше 6 символов.')
    repeat_password = forms.CharField(widget=forms.PasswordInput, max_length=40, min_length=6, label='Повторите пароль')
    avatar = forms.ImageField(label='Аватар', required=False)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        css_classes(self)

class SettingsForm(forms.Form):
    username = forms.CharField(max_length=20, label='Логин',
                               help_text='Логин меньше 20 символов, и состоит из латинских символов.')
    email = forms.EmailField(label='E-mail')
    nick_name = forms.CharField(max_length=20, label='Никнейм',
                                help_text='Никнейм меньше 20 символов.')
    avatar = forms.ImageField(widget=forms.FileInput, label='Аватар', required=False)

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        css_classes(self)

class AskForm(forms.Form):
    title = forms.CharField(label='Заголовок')
    text = forms.CharField(widget=forms.Textarea, label='Текст')
    tags = forms.CharField(label='Теги')

    def __init__(self, *args, **kwargs):
        super(AskForm, self).__init__(*args, **kwargs)
        css_classes(self)