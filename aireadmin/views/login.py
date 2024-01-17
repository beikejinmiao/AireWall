#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from aireadmin import models, forms

login_html = 'aireadmin/login.html'
index_html = 'aireadmin/index.html'
document_html = 'aireadmin/document.html'


def index(request, html=index_html):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    username = request.session['username']
    try:
        user_key = models.APIKey.objects.get(username=username)
    except:
        username += '(用户异常)'
        apikey = ''
    else:
        apikey = user_key.apikey
    return render(request, html, {'username': username, 'apikey': apikey})


def document(request):
    return index(request, html=document_html)


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(username=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['userid'] = user.id
                    request.session['username'] = user.username
                    return redirect('/index/')
                else:
                    message = '用户或者密码错误！'
                    return render(request, login_html, locals())
            except :
                message = '用户或者密码错误！'
                return render(request, login_html, locals())
        else:
            return render(request, login_html, locals())

    login_form = forms.UserForm()
    return render(request, login_html, locals())


def register(request):
    pass
    return render(request, 'aireadmin/register.html')


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")


