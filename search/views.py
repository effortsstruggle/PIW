from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse

from index.models import *
from django.db.models import Q, F


# Create your views here.
def searchView(request, page):
    if request.method == 'POST':
        # 得到搜索内容 并存入session
        request.session['kword'] = request.POST.get('kword', '')
        return redirect(reverse('search', kwargs={'page': 1}))
    # get响应
    else:
        # 获取搜索量前四的歌曲
        searches = Dynamic.objects.select_related('song').order_by('-search').all()[:4]
        # 从session中获取搜索内容
        kword = request.session.get('kword')
        # 按照kword获取数据库相关数据
        if kword:
            songs = Song.objects.filter(Q(name__icontains=kword) | Q(singer=kword)).order_by('-release').all()
        else:
            songs = Song.objects.order_by('-release').all()

        # 分页
        paginator = Paginator(songs, 10)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        # 添加歌曲搜索次数
        if kword:
            # 如果存在kword，获取和kword相关的歌曲
            idList = Song.objects.filter(name__icontains=kword).all()
            # 便利这些相关歌曲，并为其中search字段+1
            for i in idList:
                # 判断歌曲id是否存在
                dynamics = Dynamic.objects.filter(song_id=int(i.id))
                if dynamics:
                    dynamics.update(search=F('search')+1)
                # 若歌曲未设置动态信息,则为其创建新的动态信息
                else:
                    dynamic =Dynamic(plays=0,search=1,download=1,song_id=int(i.id))
                    # 保存到数据库中
                    dynamic.save()
        return render(request, 'search.html', locals())
