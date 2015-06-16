# -*- coding: utf-8

# django packages
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User

# app packages
from .models import SoUser


class UserForm(forms.ModelForm):

    nickname = forms.CharField(max_length=255, required=True)
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['nickname'].label = u'昵称'
        self.fields['email'].label = u'电子邮箱'        

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError(u"此邮箱已使用")
        return email
        
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.username = self.cleaned_data['email']

        if commit:
            user.save()
            souser = SoUser(user = user, nickname = self.cleaned_data['nickname'])
            souser.save()
        
        return user
        
    class Meta:
        model = User
        fields = ('email', 'nickname', 'password')
        widgets = {
            'password': forms.PasswordInput()
        }

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            auth_login(request, user)
            return redirect(reverse('after_login'))
    else:
        form = UserForm()
    return render(request, 'souser/register.html', {
        'form': form
    })

class UserAuthenticationForm(AuthenticationForm):

    username = forms.CharField(max_length=255, label=u'邮箱')

    error_messages = {
        'invalid_login': _(u'请输入正确的邮箱地址和密码'),
        'inactive': _(u'此用户未激活')
    }

def login(request):
    if request.method == 'POST':
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            auth_login(request, user)
            return redirect(reverse('after_login')) 
    else:
        form = UserAuthenticationForm()

    return render(request, 'souser/login.html', {
        'form': form
    })


def after_login(request):

    if request.method == 'POST':
        auth_logout(request)
        return redirect(reverse('login'))
        
    return render(request, 'souser/after_login.html')
