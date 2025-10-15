import re
from django import forms
from .models import Post, User, Message
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content", "image"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "Напиши что-нибудь..."}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })
        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "bio", "avatar"]
        
class SignupForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'})
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Аватар"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'avatar')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                self.add_error('password2', "Пароли не совпадают")
            if len(password1) < 8:
                self.add_error('password1', "Пароль должен содержать минимум 8 символов")
            if not re.search(r'[A-Z]', password1):
                self.add_error('password1', "Пароль должен содержать хотя бы одну заглавную букву (A-Z)\n")
            if not re.search(r'[a-z]', password1):
                self.add_error('password1', "Пароль должен содержать хотя бы одну строчную букву (a-z)")
            if not re.search(r'\d', password1):
                self.add_error('password1', "Пароль должен содержать хотя бы одну цифру (0-9)")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
class MessageForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'placeholder':'Введите сообщение...'}), label='')
    
    class Meta:
        model = Message
        fields = ['content']