from django.shortcuts import render, redirect
from django.urls import reverse

from .form import MyUserCreationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F, Q
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from user.models import *
from index.models import *


# Create your views here.
# 用户中心需要登录才可以访问，如未登录，则会跳转至登录页面
@login_required(login_url='/user/login.html')
def homeView(request, page):
    # 获取搜索量前四歌曲
    searches = Dynamic.objects.select_related('song').order_by('-search').all()[:4]
    # 从session中获取用户播放过的歌曲列表
    songs = request.session.get('play_list', [])
    # 分页
    paginator = Paginator(songs, 2)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return render(request, 'home.html', locals())


def loginView(request):
    # 使用制定的表单
    user = MyUserCreationForm()
    if request.method == 'POST':
        if request.POST.get('loginUser', ''):
            u = request.POST.get('loginUser', '')
            p = request.POST.get('password', '')
            if MyUser.objects.filter(Q(mobile=u) | Q(username=u)):
                u1 = MyUser.objects.filter(Q(mobile=u) | Q(username=u)).first()
                if check_password(p, u1.password):
                    login(request, u1)
                    return redirect(reverse('home', kwargs={'page': 1}))
                else:
                    tips = '密码错误'
            else:
                tips = '用户不存在'

        else:
            u = MyUserCreationForm(request.POST)
            if u.is_valid():
                u.save()
                tips = '注册成功'
            else:
                if u.errors.get('username', ''):
                    tips = u.errors.get('username', '注册失败')
                else:
                    tips = u.errors.get('mobile', '注册失败')
    return render(request, 'user.html', locals())


def logoutView(request):
    logout(request)
    return redirect('/')
